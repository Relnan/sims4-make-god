# mg_utils.py
import services
from sims.sim_info_types import Gender
import mg_config

def get_sim_by_id(sim_id):
    """Gibt den SimInfo anhand der ID zurueck."""
    sim_info_manager = services.sim_info_manager()
    return sim_info_manager.get(sim_id) if sim_info_manager else None

def get_sims_by_name(name_string, active_household=None):
    """Sucht nach einem Sim ueber den Namen."""
    sim_info_manager = services.sim_info_manager()
    if not sim_info_manager: return []
    
    search_name = str(name_string).lower().strip()
    
    def match_name(sim):
        fname = getattr(sim, 'first_name', '').lower()
        lname = getattr(sim, 'last_name', '').lower()
        full_name = f"{fname} {lname}".strip()
        return search_name == fname or search_name == lname or search_name == full_name

    all_matches = []
    for sim in sim_info_manager.values():
        if match_name(sim):
            all_matches.append(sim)

    return all_matches

def get_sims_by_fuzzy_name(name_string, active_household=None):
    """Sucht nach einem Sim ueber den Namen (Teil-Uebereinstimmung)."""
    sim_info_manager = services.sim_info_manager()
    if not sim_info_manager: return []
    
    search_name = str(name_string).lower().strip()
    
    all_matches = []
    for sim in sim_info_manager.values():
        fname = getattr(sim, 'first_name', '').lower()
        lname = getattr(sim, 'last_name', '').lower()
        full_name = f"{fname} {lname}".strip()
        
        if search_name in fname or search_name in lname or search_name in full_name:
            all_matches.append(sim)

    return all_matches

def get_occult_types(sim_info):
    """
    Ermittelt ALLE Okkult-Typen strikt und gibt eine Liste zurueck.
    witch wird zu spellcaster gemappt.
    """
    found_types = set()
    
    # 1. Check über den Occult Tracker (zuverlässig)
    try:
        if hasattr(sim_info, 'occult_tracker') and sim_info.occult_tracker:
            if sim_info.occult_tracker.has_any_occult_or_part_occult_trait():
                if hasattr(sim_info.occult_tracker, 'occult_types'):
                    for ot in sim_info.occult_tracker.occult_types:
                        type_str = str(ot).split('.')[-1].lower()
                        if type_str == 'witch':
                            found_types.add('spellcaster')
                        elif type_str and type_str not in ['none', 'human']:
                            found_types.add(type_str)
    except: pass

    # 2. Fallback über Traits (exaktes Matching)
    if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker:
        for trait in sim_info.trait_tracker.equipped_traits:
            t_name = getattr(trait, '__name__', '').lower()
            if t_name == 'trait_occultvampire': found_types.add('vampire')
            elif t_name == 'trait_occult_witchoccult': found_types.add('spellcaster')
            elif t_name == 'trait_occultwerewolf': found_types.add('werewolf')
            elif t_name == 'trait_occultmermaid': found_types.add('mermaid')
            elif t_name == 'trait_occultalien': found_types.add('alien')
            elif t_name == 'trait_occult_fairy': found_types.add('fairy')
            elif t_name == 'trait_isghost': found_types.add('ghost')
            
    return list(found_types) if found_types else ["human"]

def is_minor(sim_info):
    """Prueft, ob der Sim ein Kind oder juenger ist."""
    try:
        if hasattr(sim_info, 'is_teen_or_older'):
            return not sim_info.is_teen_or_older
        return str(sim_info.age).split('.')[-1].upper() in ['BABY', 'INFANT', 'TODDLER', 'CHILD']
    except:
        return False

def get_auto_set(sim_info, active_household, option_key="option_1"):
    """Ermittelt das passende Config-Set basierend auf Alter, Geschlecht und Haushalt."""
    profiles = mg_config.get("auto_profiles", {}).get(option_key, {})
    if not profiles:
        profiles = mg_config.get("auto_profiles", {}).get("option_1", {})
        
    is_playable = (active_household and sim_info in active_household)
    
    if is_minor(sim_info):
        return str(profiles.get("child_playable" if is_playable else "child_npc", "10"))
    else:
        is_male = (sim_info.gender == Gender.MALE)
        if is_playable:
            return str(profiles.get("adult_playable_male" if is_male else "adult_playable_female", "0"))
        else:
            return str(profiles.get("adult_npc_male" if is_male else "adult_npc_female", "1"))