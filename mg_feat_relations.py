import sims4.commands
import mg_config
import mg_logger
import mg_utils
import services
import sims4.resources

def apply_relations(sim_info, set_id, out, force_debug):
    """Setzt Freundschaft, Romantik und bereinigt negative Beziehungen nach Scope."""
    try:
        active_set = mg_config.get("sets", {}).get(str(set_id), {})
        if not active_set: return
        
        tracker = getattr(sim_info, 'relationship_tracker', None)
        if not tracker: return

        # Hole Haushaltsmitglieder intern, um die Signatur für mg_main.py nicht zu brechen
        targets = list(sim_info.household) if getattr(sim_info, 'household', None) else [sim_info]

        # --- 1. NEGATIVE BEZIEHUNGEN BEREINIGEN (GETRENNT NACH HAUSHALT & SCOPE) ---
        remove_negatives_scope = active_set.get("remove_negative_relations", False)
        remove_negatives_household = active_set.get("remove_negative_relations_household", False)
        
        if remove_negatives_scope or remove_negatives_household:
            raw_scope = active_set.get("remove_negative_relations_scope", 
                                            ["roommate", "key", "friend", "romantic", "woohoo", "married", "significant"])
            if not raw_scope: raw_scope = []
            scope_keywords = [str(s).lower() for s in raw_scope]

            negative_keywords = ['enemy', 'despised', 'bitter', 'grudge', 'hate', 'furious', 
                                 'awkward', 'creepy', 'bad', 'negative', 'divorced', 'breakup', 
                                 'cheated', 'resent', 'hurt', 'hostile', 'angry', 'dislike', 
                                 'frustrated', 'fear', 'jealous', 'guilt']

            for target_id in tuple(tracker.target_sim_gen()):
                target_sim_info = mg_utils.get_sim_by_id(target_id)
                is_in_scope = False
                
                if remove_negatives_household and target_sim_info:
                    if getattr(target_sim_info, 'household_id', None) == getattr(sim_info, 'household_id', None):
                        is_in_scope = True
                
                current_bits = tuple(tracker.get_all_bits(target_id))
                if not is_in_scope and remove_negatives_scope:
                    for bit in current_bits:
                        b_name = getattr(bit, '__name__', '').lower()
                        if any(kw in b_name for kw in scope_keywords):
                            is_in_scope = True
                            break
                        if 'fear' in b_name or 'jealous' in b_name:
                            is_in_scope = True
                            break
                
                if is_in_scope:
                    for bit in current_bits:
                        raw_b_name = getattr(bit, '__name__', '')
                        b_name = raw_b_name.lower()
                        
                        if any(kw in b_name for kw in negative_keywords):
                            # Diagnose-Schritt: Exakte Fehlererfassung
                            try:
                                tracker.remove_bit(target_id, bit)
                            except AttributeError:
                                # Fallback für den Fall, dass die Methode in neueren Patches anders heißt
                                try:
                                    tracker.remove_relationship_bit(target_id, bit)
                                except Exception as e2:
                                    mg_logger.log(f"      [Warnung] API Remove (Alt) blockiert für '{raw_b_name}'. Grund: {type(e2).__name__} - {str(e2)}", is_debug=True, out=out, force_debug=force_debug)
                            except Exception as e:
                                mg_logger.log(f"      [Warnung] API Remove blockiert für '{raw_b_name}'. Grund: {type(e).__name__} - {str(e)}", is_debug=True, out=out, force_debug=force_debug)
                            
                            # Bidirektional
                            if target_sim_info:
                                target_tracker = getattr(target_sim_info, 'relationship_tracker', None)
                                if target_tracker:
                                    try:
                                        target_tracker.remove_bit(sim_info.sim_id, bit)
                                    except:
                                        pass
                            
                            # Konsolen-Command-Fallback
                            try:
                                sims4.commands.execute(f"relationship.remove_bit {sim_info.sim_id} {target_id} {raw_b_name}", None)
                                sims4.commands.execute(f"relationship.remove_bit {target_id} {sim_info.sim_id} {raw_b_name}", None)
                            except:
                                pass

        # --- 2. POSITIVE HAUSHALTSBEZIEHUNGEN FORCIEREN ---
        target_f = active_set.get("harmony_friendship", 0)
        target_r = active_set.get("harmony_romance", 0)
        target_status = active_set.get("target_relationship_status", "")

        if target_f == 0 and target_r == 0 and not target_status:
            return

        skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        f_track = skill_manager.get(16650) if skill_manager else None
        r_track = skill_manager.get(16651) if skill_manager else None

        for target_sim in targets:
            if target_sim.sim_id == sim_info.sim_id: continue 

            if target_f != 0 and f_track:
                try: tracker.set_relationship_score(target_sim.sim_id, target_f, f_track)
                except: pass
                
            if target_r != 0 and r_track:
                if getattr(sim_info, 'age', 0) >= 8 and getattr(target_sim, 'age', 0) >= 8:
                    try: tracker.set_relationship_score(target_sim.sim_id, target_r, r_track)
                    except: pass
                    
            if target_status:
                _apply_status_bit_via_command(sim_info.sim_id, target_sim.sim_id, target_status)

        log_msg = f"   [Relations] Haushalts-Beziehungen aktualisiert (Scope={remove_negatives_scope}, HH={remove_negatives_household})"
        mg_logger.log(log_msg, is_debug=True, out=out, force_debug=force_debug)

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
        try: sims4.commands.execute(cmd.format(sim_id, target_id), None)
        except: pass