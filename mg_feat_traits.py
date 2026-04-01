# ... existing code ...
import sims4.commands
import mg_config
import mg_logger
import mg_utils
import sims4.resources
import services

def apply_traits(sim_info, set_id, out, force_debug):
    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    if not active_set: return

    # --- ENTFERNEN VON TRAITS ---
    traits_to_remove = list(active_set.get("exclude_all", []))
    if sim_info.is_female:
        traits_to_remove.extend(active_set.get("exclude_sex_female", []))
    else:
        traits_to_remove.extend(active_set.get("exclude_sex_male", []))

    # NEU: Dislikes (Abneigungen) automatisch entfernen
    if active_set.get("remove_all_dislikes", False):
        if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker:
            for t in sim_info.trait_tracker.equipped_traits:
                t_name = getattr(t, '__name__', '').lower()
                if 'simpreference_dislikes' in t_name or 'simpreference_hates' in t_name:
                    traits_to_remove.append(getattr(t, '__name__'))

    for t_name in traits_to_remove:
        try:
            sims4.commands.execute(f"traits.remove_trait {t_name} {sim_info.sim_id}", None)
        except: pass

    # --- HINZUFUEGEN VON TRAITS ---
# ... existing code ...
    for t_name in traits_to_add:
        try:
            sims4.commands.execute(f"traits.equip_trait {t_name} {sim_info.sim_id}", None)
        except: pass

    # --- NEU: HINZUFUEGEN VON PERKS & SPELLS ---
    perks_to_add = list(active_set.get("perks_all", []))
    perks_occult = active_set.get("perks_occult", {})
    if occult_type in perks_occult:
        perks_to_add.extend(perks_occult[occult_type])

    spells_to_add = list(active_set.get("spells_all", []))
    spells_occult = active_set.get("spells_occult", {})
    if occult_type in spells_occult:
        spells_to_add.extend(spells_occult[occult_type])

    if perks_to_add or spells_to_add:
        perk_manager = services.get_instance_manager(sims4.resources.Types.BUCKS_PERK)
        recipe_manager = services.get_instance_manager(sims4.resources.Types.RECIPE)
        snippet_manager = services.get_instance_manager(sims4.resources.Types.SNIPPET)
        
        def find_inst(manager, name):
            if not manager: return None
            search_name = name.lower()
            for inst in manager.types.values():
                if getattr(inst, '__name__', '').lower() == search_name:
                    return inst
            return None

        # Perks freischalten (Okkulte Fähigkeiten, Ruhm etc.)
        if perks_to_add and hasattr(sim_info, 'bucks_tracker') and sim_info.bucks_tracker:
            for p_name in perks_to_add:
                p_inst = find_inst(perk_manager, p_name)
                if p_inst:
                    try: sim_info.bucks_tracker.unlock_perk(p_inst)
                    except: pass

        # Spells & Recipes freischalten (Magie, Tränke etc.)
        if spells_to_add and hasattr(sim_info, 'unlock_tracker') and sim_info.unlock_tracker:
            for s_name in spells_to_add:
                s_inst = find_inst(recipe_manager, s_name) or find_inst(snippet_manager, s_name)
                if s_inst:
                    try: sim_info.unlock_tracker.add_unlock(s_inst, None)
                    except: pass

    mg_logger.log(f"   [Traits/Perks] {len(traits_to_add)} Traits hinzu, {len(traits_to_remove)} entfernt (Perks: {len(perks_to_add)}, Spells: {len(spells_to_add)}).", is_debug=True, out=out, force_debug=force_debug)