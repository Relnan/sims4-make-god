# mg_feat_traits.py
import sims4.commands
import mg_config
import mg_logger
import mg_utils
import sims4.resources
import services

def _unique_names(values):
    seen = []
    for value in values:
        name = str(value).strip()
        if name and name not in seen:
            seen.append(name)
    return seen

def _run_cheat(cmd, sim_info):
    try: sims4.commands.execute(f"{cmd} {sim_info.sim_id}", None)
    except: pass

def apply_traits(sim_info, set_id, out, force_debug, override_occult=None):
    first_name = getattr(sim_info, 'first_name', 'Sim')
    out(f"   -> [{first_name}] Verarbeite Okkult, Traits & Perks...")
    warning_msg = None

    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    if not active_set:
        return None

    # --- ENTFERNEN VON TRAITS ---
    traits_to_remove = list(active_set.get("exclude_all", []))
    if getattr(sim_info, 'is_female', False):
        traits_to_remove.extend(active_set.get("exclude_sex_female", []))
    else:
        traits_to_remove.extend(active_set.get("exclude_sex_male", []))

    remove_dislikes = active_set.get("remove_all_dislikes", False)
    remove_negatives = active_set.get("remove_negative_relations", False)
    
    if remove_dislikes or remove_negatives:
        if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker:
            for trait in tuple(sim_info.trait_tracker.equipped_traits):
                trait_name = getattr(trait, '__name__', '').lower()
                is_dislike = 'simpreference_dislikes' in trait_name or 'simpreference_hates' in trait_name
                is_fear = 'trait_fear' in trait_name or 'trait_phobia' in trait_name
                
                if (remove_dislikes and is_dislike) or (remove_negatives and is_fear):
                    raw_name = getattr(trait, '__name__', '')
                    if raw_name:
                        traits_to_remove.append(raw_name)

    traits_to_remove = _unique_names(traits_to_remove)
    for t_name in traits_to_remove:
        _run_cheat(f"traits.remove_trait {t_name}", sim_info)

    # --- OKKULT TYPEN BESTIMMEN ---
    occult_types = mg_utils.get_occult_types(sim_info)
    active_occults = []
    
    if override_occult and override_occult in occult_types:
         active_occults = [override_occult]
    elif len(occult_types) > 1:
        if 'ghost' in occult_types:
             active_occults = [t for t in occult_types if t != 'ghost'] + ['ghost']
        else:
             suggestion = " oder ".join([f"'rmg.active {set_id} {t}'" for t in occult_types])
             warning_msg = f"Okkult-Konflikt bei {first_name}: {occult_types}. Uebersprungen. Nutze {suggestion}."
             mg_logger.log(f"   [Traits/Perks] {warning_msg}", is_debug=False, out=None, force_debug=force_debug)
    elif len(occult_types) == 1:
         active_occults = occult_types

    # --- HINZUFUEGEN VON TRAITS ---
    traits_to_add = list(active_set.get("traits_all", []))
    if getattr(sim_info, 'is_female', False):
        traits_to_add.extend(active_set.get("traits_sex_female", []))
    else:
        traits_to_add.extend(active_set.get("traits_sex_male", []))

    occult_traits_dict = active_set.get("traits_occult", {})
    for occ in active_occults:
        if occ in occult_traits_dict:
            traits_to_add.extend(occult_traits_dict[occ])

    traits_to_add = _unique_names(traits_to_add)
    for t_name in traits_to_add:
         _run_cheat(f"traits.equip_trait {t_name}", sim_info)

    # --- PERKS INITIALISIEREN ---
    perks_to_add = list(active_set.get("perks_all", []))
    perks_occult = active_set.get("perks_occult", {})
    for occ in active_occults:
        if occ in perks_occult:
            perks_to_add.extend(perks_occult[occ])
    perks_to_add = _unique_names(perks_to_add)

    perks_to_remove = list(active_set.get("perks_exclude_all", []))
    perks_excl_occult = active_set.get("perks_exclude_occult", {})
    for occ in active_occults:
        if occ in perks_excl_occult:
            perks_to_remove.extend(perks_excl_occult[occ])
    perks_to_remove = _unique_names(perks_to_remove)
    
    strict_perk_mode = active_set.get("remove_unlisted_perks", False)
    perk_manager = services.get_instance_manager(sims4.resources.Types.BUCKS_PERK) if hasattr(sims4.resources.Types, 'BUCKS_PERK') else None

    # --- PERKS BEREINIGEN & HINZUFUEGEN ---
    removed_perks_count = 0
    added_perks_count = 0
    
    b_tracker = getattr(sim_info, 'bucks_tracker', None)
    if not b_tracker and hasattr(sim_info, 'get_bucks_tracker'):
         try: b_tracker = sim_info.get_bucks_tracker()
         except: pass

    if not warning_msg:
        if b_tracker and perk_manager and (strict_perk_mode or perks_to_remove):
            for perk_inst in tuple(perk_manager.types.values()):
                try:
                    if b_tracker.is_perk_unlocked(perk_inst):
                        p_name = getattr(perk_inst, '__name__', '')
                        if (strict_perk_mode and p_name not in perks_to_add) or (p_name in perks_to_remove):
                            try:
                                if hasattr(b_tracker, 'lock_perk'): b_tracker.lock_perk(perk_inst)
                                elif hasattr(b_tracker, 'remove_perk'): b_tracker.remove_perk(perk_inst)
                                removed_perks_count += 1
                            except: pass
                except: pass
        
        perks_to_add_sorted = sorted(perks_to_add)
        for p_name in perks_to_add_sorted:
            actual_p_name = p_name
            if actual_p_name.lower() == "witchperks_alchemy_2_frugalcombiner":
                actual_p_name = "witchPerks_Alchemy_2_FrugalCombinations"
                
            _run_cheat(f"bucks.unlock_perk {actual_p_name} true", sim_info)
            added_perks_count += 1
            
            if b_tracker and perk_manager:
                search_name = str(actual_p_name).lower()
                for inst in perk_manager.types.values():
                    if getattr(inst, '__name__', '').lower() == search_name:
                        try: b_tracker.unlock_perk(inst)
                        except: pass
                        break

    mg_logger.log(f"   [Traits/Perks] Abgeschlossen für {first_name} ({len(traits_to_add)} Traits, {added_perks_count} Perks, {removed_perks_count} entfernt).", is_debug=True, out=None, force_debug=force_debug)
    return warning_msg