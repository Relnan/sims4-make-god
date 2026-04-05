import sims4.commands
import mg_config
import mg_logger
import mg_utils
import services
import sims4.resources

def apply_relations(sim_info, set_id, out, force_debug, group_targets=None, _connection=None):
    try:
        first_name = getattr(sim_info, 'first_name', 'Sim')
        out(f"   -> [{first_name}] Berechne Beziehungen & Netzwerk...")

        active_set = mg_config.get("sets", {}).get(str(set_id), {})
        if not active_set: return
        
        tracker = getattr(sim_info, 'relationship_tracker', None)
        if not tracker: return

        # Nutze den injizierten Pool (Haushalt + Mitbewohner + Schluessel) falls vorhanden
        targets = group_targets if group_targets else (list(sim_info.household) if getattr(sim_info, 'household', None) else [sim_info])
        
        skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        f_track = skill_manager.get(16650) if skill_manager else None
        r_track = skill_manager.get(16651) if skill_manager else None

        # --- 1. CONFIGS LADEN ---
        # Alte negative Bereinigung
        remove_negatives_scope = active_set.get("remove_negative_relations", False)
        remove_negatives_household = active_set.get("remove_negative_relations_household", False)
        raw_scope = active_set.get("remove_negative_relations_scope", [])
        scope_keywords = [str(s).lower() for s in raw_scope]
        negative_keywords = ['enemy', 'despised', 'bitter', 'grudge', 'hate', 'furious', 
                             'awkward', 'creepy', 'bad', 'negative', 'divorced', 'breakup', 
                             'cheated', 'resent', 'hurt', 'hostile', 'angry', 'dislike', 
                             'frustrated', 'fear', 'jealous', 'guilt']

        ext_network = active_set.get("harmony_extended_network", {})
        ext_enabled = ext_network.get("enabled", False)
        raw_ext_scope = ext_network.get("scopes", [])
        ext_scope_keywords = [str(s).lower() for s in raw_ext_scope]
        
        is_source_female = getattr(sim_info, 'is_female', False)
        source_key = "source_female" if is_source_female else "source_male"
        source_config = ext_network.get(source_key, {})

        # NEU: Relationship Master System
        rel_sys = mg_config.get("relationship_system", {})
        global_rules = rel_sys.get("global_rules", {})
        allow_downgrade = global_rules.get("allow_downgrade", False)
        allow_incest = global_rules.get("allow_incest", False)
        allow_teen_adult = global_rules.get("allow_teen_adult_romance", False)
        status_defs = rel_sys.get("status_definitions", {})

        # --- ZAEHLER INITIALISIEREN ---
        checked_count = 0
        modified_count = 0

        # --- 2. SINGLE-PASS SCHLEIFE FUER ALLE EXTERNEN BEZIEHUNGEN ---
        for target_id in tuple(tracker.target_sim_gen()):
            if target_id == sim_info.sim_id: continue
            
            checked_count += 1
            target_modified = False
            target_sim_info = None  
            current_bits = tuple(tracker.get_all_bits(target_id))
            
            # --- TEIL A: NEGATIVE BEREINIGUNG ---
            if remove_negatives_scope or remove_negatives_household:
                is_in_neg_scope = False
                
                if remove_negatives_household:
                    if not target_sim_info: target_sim_info = mg_utils.get_sim_by_id(target_id)
                    if target_sim_info and getattr(target_sim_info, 'household_id', None) == getattr(sim_info, 'household_id', None):
                        is_in_neg_scope = True
                
                if not is_in_neg_scope and remove_negatives_scope:
                    for bit in current_bits:
                        b_name = getattr(bit, '__name__', '').lower()
                        if any(kw in b_name for kw in scope_keywords) or 'fear' in b_name or 'jealous' in b_name:
                            is_in_neg_scope = True; break
                
                if is_in_neg_scope:
                    for bit in current_bits:
                        raw_b_name = getattr(bit, '__name__', '')
                        b_name = raw_b_name.lower()
                        
                        if 'compatibility' in b_name: continue

                        if any(kw in b_name for kw in negative_keywords):
                            api_success = False
                            try: 
                                tracker.remove_bit(target_id, bit)
                                api_success = True
                                target_modified = True
                            except: pass
                            
                            if not target_sim_info: target_sim_info = mg_utils.get_sim_by_id(target_id)
                            if target_sim_info:
                                target_tracker = getattr(target_sim_info, 'relationship_tracker', None)
                                if target_tracker:
                                    try: target_tracker.remove_bit(sim_info.sim_id, bit)
                                    except: pass
                            
                            if not api_success:
                                try:
                                    sims4.commands.execute(f"relationship.remove_bit {sim_info.sim_id} {target_id} {raw_b_name}", None)
                                    sims4.commands.execute(f"relationship.remove_bit {target_id} {sim_info.sim_id} {raw_b_name}", None)
                                    target_modified = True
                                except: pass

            # --- TEIL B: ERWEITERTES SOZIALES NETZWERK (MATRIX) ---
            if ext_enabled:
                in_ext_scope = False
                for bit in current_bits:
                    b_name = getattr(bit, '__name__', '').lower()
                    if any(kw in b_name for kw in ext_scope_keywords):
                        in_ext_scope = True; break
                
                if in_ext_scope:
                    if not target_sim_info: target_sim_info = mg_utils.get_sim_by_id(target_id)
                    
                    if target_sim_info:
                        is_target_female = getattr(target_sim_info, 'is_female', False)
                        target_key = "target_female" if is_target_female else "target_male"
                        matrix_values = source_config.get(target_key, {})
                        
                        target_age_norm = str(getattr(target_sim_info, 'age', '')).split('.')[-1].lower().replace('_', '')
                        t_friendship = None
                        t_romance = None
                        
                        for k, v in matrix_values.items():
                            if type(v) is dict and k.lower().replace('_', '') == target_age_norm:
                                t_friendship = v.get("friendship", -999)
                                t_romance = v.get("romance", -999)
                                break
                        else:
                            t_friendship = matrix_values.get("friendship", -999)
                            t_romance = matrix_values.get("romance", -999)
                        
                        if t_friendship == -999: t_friendship = None
                        if t_romance == -999: t_romance = None
                        
                        if t_friendship is not None and f_track:
                            curr_f = tracker.get_relationship_score(target_id, f_track)
                            if allow_downgrade or curr_f < t_friendship:
                                try: 
                                    tracker.set_relationship_score(target_id, t_friendship, f_track)
                                    target_modified = True
                                except: pass
                                
                        if t_romance is not None and r_track:
                            if getattr(sim_info, 'age', 0) >= 8 and getattr(target_sim_info, 'age', 0) >= 8:
                                curr_r = tracker.get_relationship_score(target_id, r_track)
                                if allow_downgrade or curr_r < t_romance:
                                    try: 
                                        tracker.set_relationship_score(target_id, t_romance, r_track)
                                        target_modified = True
                                    except: pass
            
            if target_modified: modified_count += 1

        # --- 3. HAUSHALTSBEZIEHUNGEN FORCIEREN (Neues System) ---
        target_f = active_set.get("harmony_friendship", -999)
        target_r = active_set.get("harmony_romance", -999)
        target_status = active_set.get("target_relationship_status", "")

        for target_sim in targets:
            if target_sim.sim_id == sim_info.sim_id: continue 
            checked_count += 1
            target_modified = False
            
            curr_f = tracker.get_relationship_score(target_sim.sim_id, f_track) if f_track else 0
            curr_r = tracker.get_relationship_score(target_sim.sim_id, r_track) if r_track else 0
            current_bits = tuple(tracker.get_all_bits(target_sim.sim_id))
            
            # --- Alters- und Inzest-Pruefung ---
            is_family = False
            if not allow_incest:
                for bit in current_bits:
                    b_name = getattr(bit, '__name__', '').lower()
                    if any(k in b_name for k in ['family', 'parent', 'sibling', 'grand']):
                        is_family = True; break
                        
            is_teen_adult_conflict = False
            if not allow_teen_adult and target_status in ['woohoo_partner', 'significant_other', 'engaged', 'married']:
                age_self = getattr(sim_info, 'age', 0)
                age_target = getattr(target_sim, 'age', 0)
                if (age_self < 8 and age_target >= 8) or (age_self >= 8 and age_target < 8):
                    is_teen_adult_conflict = True

            # --- Scores setzen (mit Downgrade-Check) ---
            if target_f != -999 and f_track:
                if allow_downgrade or curr_f < target_f:
                    try: 
                        tracker.set_relationship_score(target_sim.sim_id, target_f, f_track)
                        target_modified = True
                    except: pass
                
            if target_r != -999 and r_track and not is_family and not is_teen_adult_conflict:
                if getattr(sim_info, 'age', 0) >= 8 and getattr(target_sim, 'age', 0) >= 8:
                    if allow_downgrade or curr_r < target_r:
                        try: 
                            tracker.set_relationship_score(target_sim.sim_id, target_r, r_track)
                            target_modified = True
                        except: pass
                    
            # --- Status-Bits setzen (Konflikte entfernen) ---
            if target_status and not is_family and not is_teen_adult_conflict:
                status_def = status_defs.get(target_status)
                if status_def:
                    remove_conflicts = status_def.get("remove_conflicts", [])
                    add_bits = status_def.get("add_bits", [])
                    
                    for bit in current_bits:
                        if getattr(bit, '__name__', '') in remove_conflicts:
                            try: tracker.remove_bit(target_sim.sim_id, bit)
                            except: pass
                            
                    for bit_name in add_bits:
                        try: sims4.commands.execute(f"relationship.add_bit {sim_info.sim_id} {target_sim.sim_id} {bit_name}", None)
                        except: pass
                    target_modified = True
            
            if target_modified: modified_count += 1

        ext_status = "Aktiv" if ext_enabled else "Inaktiv"
        mg_logger.log(f"   [Relations] {checked_count} geprueft, {modified_count} bearbeitet (Ext-Matrix: {ext_status})", is_debug=True, out=None, force_debug=force_debug)
        mg_logger.log(f"   [Relations] Abgeschlossen fuer {first_name}.", is_debug=True, out=None, force_debug=force_debug)

    except Exception as e:
        mg_logger.log(f"[FEHLER Relations] {e}", is_debug=False, out=out, force_debug=force_debug)