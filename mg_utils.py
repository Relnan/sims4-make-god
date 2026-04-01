import services
from sims.sim_info_types import Gender
import mg_config

def get_sim_by_id(sim_id):
    """Gibt den SimInfo anhand der ID zurueck."""
    sim_info_manager = services.sim_info_manager()
    if not sim_info_manager: return None
    return sim_info_manager.get(sim_id)

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

def get_occult_type(sim_info):
    """Ermittelt den Okkult-Typ absolut strikt, um False-Positives zu vermeiden."""
    
    # 1. Native EA-Methode zuerst
    try:
        if hasattr(sim_info, 'occult_tracker') and sim_info.occult_tracker:
            if sim_info.occult_tracker.has_any_occult_or_part_occult_trait():
                ot = sim_info.occult_tracker.occult_types
                if ot:
                    type_str = str(list(ot)[0]).split('.')[-1].lower()
                    if type_str and type_str != 'none' and type_str != 'human':
                        return type_str
    except: pass

    # 2. Fallback: Trait-Tracker (Nur EXAKTE Basis-Traits prüfen)
    if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker:
        for trait in sim_info.trait_tracker.equipped_traits:
            t_name = getattr(trait, '__name__', '').lower()
            
            if t_name == 'trait_occultvampire': return 'vampire'
            if t_name == 'trait_occult_witchoccult': return 'spellcaster'
            if t_name == 'trait_occultwerewolf': return 'werewolf'
            if t_name == 'trait_occultmermaid': return 'mermaid'
            if t_name == 'trait_occultalien': return 'alien'
            
            # Mod-Unterstützung für Feen (Fairies)
            if t_name == 'trait_occult_fairy' or t_name == 'trait_occultfairy' or 'fairy_occult' in t_name: 
                return 'fairy'
            
    return "human"

def is_minor(sim_info):
    try:
        if hasattr(sim_info, 'is_teen_or_older'):
            return not sim_info.is_teen_or_older
        age_name = str(sim_info.age).split('.')[-1].upper()
        minor_ages = ['BABY', 'INFANT', 'TODDLER', 'CHILD']
        return age_name in minor_ages
    except:
        return False

def get_auto_set(sim_info, active_household, option_key="option_1"):
    profiles = mg_config.get("auto_profiles", {}).get(option_key, {})
    if not profiles:
        profiles = mg_config.get("auto_profiles", {}).get("option_1", {})
        
    if is_minor(sim_info):
        if active_household and sim_info in active_household:
            return str(profiles.get("child_playable", "10"))
        else:
            return str(profiles.get("child_npc", "11"))
    else:
        is_playable = (active_household and sim_info in active_household)
        is_male = (sim_info.gender == Gender.MALE)
        
        if is_playable:
            return str(profiles.get("adult_playable_male" if is_male else "adult_playable_female", "0"))
        else:
            return str(profiles.get("adult_npc_male" if is_male else "adult_npc_female", "1"))