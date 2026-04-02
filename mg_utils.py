import services
from sims.sim_info_types import Gender
import sims4.resources
import mg_config

def get_sim_by_id(sim_id):
    """Gibt den SimInfo anhand der ID zurueck."""
    sim_info_manager = services.sim_info_manager()
    return sim_info_manager.get(sim_id) if sim_info_manager else None

def get_sims_by_name(name_string, active_household=None):
    """Einfache Namenssuche (Fallback)."""
    return get_sims_by_fuzzy_name(name_string, active_household)

def get_sims_by_fuzzy_name(name_string, active_household=None):
    """Sucht nach einem Sim ueber Teilstrings und entfernt Anfuehrungszeichen."""
    sim_info_manager = services.sim_info_manager()
    if not sim_info_manager: return []
    
    search_terms = str(name_string).lower().replace('"', '').split()
    if not search_terms: return []
    
    all_matches = []
    search_full = " ".join(search_terms)

    for sim in sim_info_manager.values():
        fname = getattr(sim, 'first_name', '').lower()
        lname = getattr(sim, 'last_name', '').lower()
        full_name = f"{fname} {lname}".strip()
        
        # 1. Exakter Treffer erzwingt sofortige Rueckgabe
        if full_name == search_full:
            return [sim]
            
        # 2. Fuzzy Suche (Teilstrings)
        hit = False
        for term in search_terms:
            if term == fname or term == lname:
                hit = True
                break
        if hit:
            all_matches.append(sim)

    return all_matches

def is_apartment_or_penthouse():
    """Prueft, ob das aktuelle Lot ein Apartment oder Penthouse ist."""
    try:
        plex_service = services.get_plex_service()
        if plex_service and plex_service.is_active_zone_a_plex():
            return True
    except: pass
    
    try:
        venue_manager = services.get_instance_manager(sims4.resources.Types.VENUE)
        venue_service = services.venue_service()
        if venue_service and venue_manager:
            active_venue = venue_service.source_venue_type
            v_name = getattr(active_venue, '__name__', '').lower()
            if 'penthouse' in v_name or 'apartment' in v_name:
                return True
    except: pass
    
    return False

def get_occult_type(sim_info):
    try:
        if hasattr(sim_info, 'occult_tracker') and sim_info.occult_tracker:
            if sim_info.occult_tracker.has_any_occult_or_part_occult_trait():
                ot = sim_info.occult_tracker.occult_types
                if ot:
                    type_str = str(list(ot)[0]).split('.')[-1].lower()
                    if type_str and type_str not in ['none', 'human']: 
                        return type_str
    except: pass

    if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker:
        for trait in sim_info.trait_tracker.equipped_traits:
            t_name = getattr(trait, '__name__', '').lower()
            if t_name == 'trait_occultvampire': return 'vampire'
            if t_name == 'trait_occult_witchoccult': return 'spellcaster'
            if t_name == 'trait_occultwerewolf': return 'werewolf'
            if t_name == 'trait_occultmermaid': return 'mermaid'
            if t_name == 'trait_occultalien': return 'alien'
            if t_name == 'trait_occult_fairy' or t_name == 'trait_occultfairy' or 'fairy_occult' in t_name: 
                return 'fairy'
            
    return "human"

def is_minor(sim_info):
    try:
        if hasattr(sim_info, 'is_teen_or_older'):
            return not sim_info.is_teen_or_older
        return str(sim_info.age).split('.')[-1].upper() in ['BABY', 'INFANT', 'TODDLER', 'CHILD']
    except:
        return False

def get_auto_set(sim_info, active_household, option_key="option_1"):
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