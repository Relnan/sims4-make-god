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

def apply_traits(sim_info, set_id, out, force_debug):
    first_name = getattr(sim_info, 'first_name', 'Sim')
    out(f"   -> [{first_name}] Verarbeite Okkult, Traits & Perks...")

    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    if not active_set:
        return

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
        try:
            sims4.commands.execute(f"traits.remove_trait {t_name} {sim_info.sim_id}", None)
        except:
            pass

    # --- HINZUFUEGEN VON TRAITS ---
    traits_to_add = list(active_set.get("traits_all", []))
    if getattr(sim_info, 'is_female', False):
        traits_to_add.extend(active_set.get("traits_sex_female", []))
    else:
        traits_to_add.extend(active_set.get("traits_sex_male", []))

    occult_type = mg_utils.get_occult_type(sim_info)
    occult_traits_dict = active_set.get("traits_occult", {})
    if occult_type in occult_traits_dict:
        traits_to_add.extend(occult_traits_dict[occult_type])

    traits_to_add = _unique_names(traits_to_add)
    for t_name in traits_to_add:
        try:
            sims4.commands.execute(f"traits.equip_trait {t_name} {sim_info.sim_id}", None)
        except:
            pass

    # --- PERKS & SPELLS INITIALISIEREN ---
    perks_to_add = list(active_set.get("perks_all", []))
    perks_occult = active_set.get("perks_occult", {})
    if occult_type in perks_occult:
        perks_to_add.extend(perks_occult[occult_type])
    perks_to_add = _unique_names(perks_to_add)

    perks_to_remove = list(active_set.get("perks_exclude_all", []))
    perks_excl_occult = active_set.get("perks_exclude_occult", {})
    if occult_type in perks_excl_occult:
        perks_to_remove.extend(perks_excl_occult[occult_type])
    perks_to_remove = _unique_names(perks_to_remove)
    
    strict_perk_mode = active_set.get("remove_unlisted_perks", False)

    spells_to_add = list(active_set.get("spells_all", []))
    spells_occult = active_set.get("spells_occult", {})
    if occult_type in spells_occult:
        spells_to_add.extend(spells_occult[occult_type])
    spells_to_add = _unique_names(spells_to_add)

    perk_manager = services.get_instance_manager(sims4.resources.Types.BUCKS_PERK) if hasattr(sims4.resources.Types, 'BUCKS_PERK') else None
    recipe_manager = services.get_instance_manager(sims4.resources.Types.RECIPE) if hasattr(sims4.resources.Types, 'RECIPE') else None
    snippet_manager = services.get_instance_manager(sims4.resources.Types.SNIPPET) if hasattr(sims4.resources.Types, 'SNIPPET') else None

    def find_inst(manager, name):
        if not manager: return None
        search_name = str(name).lower()
        for inst in manager.types.values():
            if getattr(inst, '__name__', '').lower() == search_name:
                return inst
        return None

    # --- PERKS BEREINIGEN & HINZUFUEGEN ---
    removed_perks_count = 0
    added_perks_count = 0
    if hasattr(sim_info, 'bucks_tracker') and sim_info.bucks_tracker and perk_manager:
        if strict_perk_mode or perks_to_remove:
            for perk_inst in perk_manager.types.values():
                try:
                    if sim_info.bucks_tracker.is_perk_unlocked(perk_inst):
                        p_name = getattr(perk_inst, '__name__', '')
                        if (strict_perk_mode and p_name not in perks_to_add) or (p_name in perks_to_remove):
                            try:
                                if hasattr(sim_info.bucks_tracker, 'lock_perk'):
                                    sim_info.bucks_tracker.lock_perk(perk_inst)
                                removed_perks_count += 1
                            except: pass
                except: pass
        
        for p_name in perks_to_add:
            p_inst = find_inst(perk_manager, p_name)
            if p_inst:
                try:
                    sim_info.bucks_tracker.unlock_perk(p_inst)
                    added_perks_count += 1
                except: pass

    # --- SPELLS & POTIONS HINZUFUEGEN (DYNAMIC REFLECTION) ---
    if spells_to_add:
        potential_trackers = []
        for attr_name in dir(sim_info):
            if 'tracker' in attr_name.lower() or 'magic' in attr_name.lower():
                t_obj = getattr(sim_info, attr_name, None)
                if t_obj: potential_trackers.append(t_obj)
                
        if hasattr(sim_info, 'get_unlock_tracker'):
            try: potential_trackers.append(sim_info.get_unlock_tracker())
            except: pass

        for s_name in spells_to_add:
            s_inst = find_inst(recipe_manager, s_name) or find_inst(snippet_manager, s_name)
            if s_inst:
                for tracker in potential_trackers:
                    added = False
                    try:
                        if hasattr(tracker, 'add_unlock'):
                            tracker.add_unlock(s_inst, None)
                            added = True
                        elif hasattr(tracker, 'unlock_spell'):
                            tracker.unlock_spell(s_inst)
                            added = True
                        elif hasattr(tracker, 'add_spell'):
                            tracker.add_spell(s_inst)
                            added = True
                    except: pass
                    if added: break

    mg_logger.log(f"   [Traits/Perks] Abgeschlossen für {first_name} ({len(traits_to_add)} Traits, {added_perks_count} Perks, {removed_perks_count} entfernt).", is_debug=True, out=None, force_debug=force_debug)