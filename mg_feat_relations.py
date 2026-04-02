import sims4.commands
import mg_config
import mg_logger
import mg_utils
import services
import sims4.resources

# --- URSPRÜNGLICHE LOGIK FÜR KOMPLETTE SETS ---
def apply_relations(sim_info, set_id, out, force_debug, group_targets=None):
    try:
        first_name = getattr(sim_info, 'first_name', 'Sim')
        out(f"   -> [{first_name}] Berechne Beziehungen & Netzwerk...")

        active_set = mg_config.get("sets", {}).get(str(set_id), {})
        if not active_set: return
        
        tracker = getattr(sim_info, 'relationship_tracker', None)
        if not tracker: return

        targets = group_targets if group_targets else (list(sim_info.household) if getattr(sim_info, 'household', None) else [sim_info])
        
        skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        f_track = skill_manager.get(16650) if skill_manager else None
        r_track = skill_manager.get(16651) if skill_manager else None

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

        checked_count = 0
        modified_count = 0

        for target_id in tuple(tracker.target_sim_gen()):
            if target_id == sim_info.sim_id: continue
            
            checked_count += 1
            target_modified = False
            target_sim_info = None  
            current_bits = tuple(tracker.get_all_bits(target_id))
            
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
                            if curr_f < t_friendship:
                                try: 
                                    tracker.set_relationship_score(target_id, t_friendship, f_track)
                                    target_modified = True
                                except: pass
                                
                        if t_romance is not None and r_track:
                            if getattr(sim_info, 'age', 0) >= 8 and getattr(target_sim_info, 'age', 0) >= 8:
                                curr_r = tracker.get_relationship_score(target_id, r_track)
                                if curr_r < t_romance:
                                    try: 
                                        tracker.set_relationship_score(target_id, t_romance, r_track)
                                        target_modified = True
                                    except: pass
            
            if target_modified: modified_count += 1

        target_f = active_set.get("harmony_friendship", -999)
        target_r = active_set.get("harmony_romance", -999)
        target_status = active_set.get("target_relationship_status", "")

        for target_sim in targets:
            if target_sim.sim_id == sim_info.sim_id: continue 
            checked_count += 1
            target_modified = False

            if target_f != -999 and f_track:
                curr_f = tracker.get_relationship_score(target_sim.sim_id, f_track)
                if curr_f < target_f:
                    try: 
                        tracker.set_relationship_score(target_sim.sim_id, target_f, f_track)
                        target_modified = True
                    except: pass
                
            if target_r != -999 and r_track:
                if getattr(sim_info, 'age', 0) >= 8 and getattr(target_sim, 'age', 0) >= 8:
                    curr_r = tracker.get_relationship_score(target_sim.sim_id, r_track)
                    if curr_r < target_r:
                        try: 
                            tracker.set_relationship_score(target_sim.sim_id, target_r, r_track)
                            target_modified = True
                        except: pass
                    
            if target_status:
                if _apply_status_bit_via_command(sim_info.sim_id, target_sim.sim_id, target_status):
                    target_modified = True
            
            if target_modified: modified_count += 1

        ext_status = "Aktiv" if ext_enabled else "Inaktiv"
        mg_logger.log(f"   [Relations] {checked_count} geprüft, {modified_count} bearbeitet", is_debug=True, out=None, force_debug=force_debug)

    except Exception as e:
        mg_logger.log(f"[FEHLER Relations] {e}", is_debug=False, out=out, force_debug=force_debug)

def _apply_status_bit_via_command(sim_id, target_id, status):
    status_map = {
        "friend": "relationship.add_bit {0} {1} relbit_Friend",
        "best_friend": "relationship.add_bit {0} {1} relbit_BestFriends",
        "woohoo_partner": "relationship.add_bit {0} {1} RomanticCombo_WoohooPartners",
        "significant_other": "relationship.add_bit {0} {1} RomanticCombo_SignificantOther",
        "engaged": "relationship.add_bit {0} {1} RomanticCombo_Engaged",
        "married": "relationship.add_bit {0} {1} RomanticCombo_Married"
    }
    cmd = status_map.get(status)
    if cmd:
        try: 
            sims4.commands.execute(cmd.format(sim_id, target_id), None)
            return True
        except: pass
    return False

# --- NEU: MANUELLE LOGIK FÜR RMG.ADD ---
def apply_manual_relation(sim_info, target_sim, settings, out, force_debug=False):
    """
    Wendet Friendship, Romance und Keyholder basierend auf der Config direkt an.
    """
    try:
        tracker = getattr(sim_info, 'relationship_tracker', None)
        if not tracker: return
        
        target_id = target_sim.sim_id
        
        # 1. Fallback Werte holen
        t_friendship = settings.get("friendship", 1)
        t_romance = settings.get("romance", -999)
        
        # 2. Culling-Schutz (Verhindert MCCC Löschung)
        if t_friendship <= 0 and t_friendship != -999:
            t_friendship = 1
            
        skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        f_track = skill_manager.get(16650) if skill_manager else None
        r_track = skill_manager.get(16651) if skill_manager else None
        
        if t_friendship != -999 and f_track:
            tracker.set_relationship_score(target_id, t_friendship, f_track)
            out(f" -> Friendship gesetzt auf: {t_friendship}")
            
        if t_romance != -999 and r_track:
            if getattr(sim_info, 'age', 0) >= 8 and getattr(target_sim, 'age', 0) >= 8:
                tracker.set_relationship_score(target_id, t_romance, r_track)
                out(f" -> Romance gesetzt auf: {t_romance}")
            else:
                out(" -> [INFO] Romance ignoriert (Mindestalter nicht erreicht).")

        # 3. Keyholder Zuweisung
        add_key = settings.get("add_keyholder", False)
        if add_key:
            if mg_utils.is_apartment_or_penthouse():
                out(" -> [INFO] Keyholder-Status uebersprungen (Lot ist Apartment/Penthouse).")
            else:
                _apply_keyholder(sim_info, target_sim, out)
                
    except Exception as e:
        out(f"[FEHLER] apply_manual_relation: {e}")

def _apply_keyholder(sim_info, target_sim, out):
    """
    Zuweisung des Hauschluessels (Keyholder) ueber den offiziellen EA Konsolenbefehl.
    Dies umgeht API-Abstuerze bei nicht-geladenen (hidden) Sims.
    """
    try:
        sim_id = sim_info.sim_id
        target_id = target_sim.sim_id
        
        # Das offizielle EA Beziehungs-Bit fuer Schluesselhalter
        key_bit = "relbit_HasKey"
        
        # Zuweisung per Konsole erzwingen
        try:
            sims4.commands.execute(f"relationship.add_bit {sim_id} {target_id} {key_bit}", None)
            out(" -> [OK] Keyholder-Status erfolgreich zugewiesen.")
        except Exception as e:
            out(f" -> [FEHLER] Konsolenbefehl blockiert: {e}")
            
    except Exception as e:
        out(f" -> [FEHLER] Keyholder-Zuweisung komplett fehlgeschlagen: {e}")