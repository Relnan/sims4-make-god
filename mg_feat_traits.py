import sims4.commands
import mg_config
import mg_logger
import mg_utils

def apply_traits(sim_info, set_id, out, force_debug):
    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    if not active_set: return

    # --- ENTFERNEN VON TRAITS ---
    traits_to_remove = list(active_set.get("exclude_all", []))
    if sim_info.is_female:
        traits_to_remove.extend(active_set.get("exclude_sex_female", []))
    else:
        traits_to_remove.extend(active_set.get("exclude_sex_male", []))

    for t_name in traits_to_remove:
        try:
            sims4.commands.execute(f"traits.remove_trait {t_name} {sim_info.sim_id}", None)
        except: pass

    # --- HINZUFUEGEN VON TRAITS ---
    traits_to_add = list(active_set.get("traits_all", []))
    if sim_info.is_female:
        traits_to_add.extend(active_set.get("traits_sex_female", []))
    else:
        traits_to_add.extend(active_set.get("traits_sex_male", []))
        
    # Okkult-spezifische Traits laden
    occult_type = mg_utils.get_occult_type(sim_info)
    occult_traits_dict = active_set.get("traits_occult", {})
    if occult_type in occult_traits_dict:
        traits_to_add.extend(occult_traits_dict[occult_type])

    for t_name in traits_to_add:
        try:
            sims4.commands.execute(f"traits.equip_trait {t_name} {sim_info.sim_id}", None)
        except: pass

    mg_logger.log(f"   [Traits] {len(traits_to_add)} zum Hinzufuegen, {len(traits_to_remove)} zum Entfernen gesendet (Okkult: {occult_type}).", is_debug=True, out=out, force_debug=force_debug)