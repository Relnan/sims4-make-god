import sims4.commands
from sims.sim_info_types import Gender
import mg_config
import mg_logger

def _run_cheat(cmd, sim_info):
    try:
        # None als Verbindung unterdrueckt die nervigen EA-Fehlermeldungen!
        sims4.commands.execute(f"{cmd} {sim_info.sim_id}", None)
    except: pass

def apply_traits(sim_info, set_id, out, force_debug):
    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    if not active_set: return

    stats = {'add': 0, 'rem': 0}
    is_male = (sim_info.gender == Gender.MALE)

    excludes = active_set.get("exclude_all", []).copy()
    excludes.extend(active_set.get("exclude_sex_male", []) if is_male else active_set.get("exclude_sex_female", []))
    
    current_traits = list(sim_info.get_traits()) if hasattr(sim_info, 'get_traits') else []
    for t in current_traits:
        t_name = getattr(t, '__name__', 'unbekannt').lower()
        if any(ex.lower() in t_name for ex in excludes if ex):
            _run_cheat(f"traits.remove_trait {t_name}", sim_info)
            stats['rem'] += 1

    to_add = active_set.get("traits_all", []).copy()
    to_add.extend(active_set.get("traits_sex_male", []) if is_male else active_set.get("traits_sex_female", []))

    for t_name in set(to_add):
        if t_name:
            _run_cheat(f"traits.equip_trait {t_name}", sim_info)
            stats['add'] += 1

    mg_logger.log(f"   [Traits] {stats['add']} hinzugefuegt, {stats['rem']} entfernt.", is_debug=True, out=out, force_debug=force_debug)