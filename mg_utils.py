import services
from sims.sim_info_types import Gender
import mg_config

def get_sim_by_id(sim_id):
    """Gibt den SimInfo anhand der ID zurueck."""
    sim_info_manager = services.sim_info_manager()
    if not sim_info_manager: return None
    return sim_info_manager.get(sim_id)

def get_sims_by_name(name_string, active_household=None):
    """
    Sucht nach einem Sim ueber den Namen.
    Priorisiert den aktiven Haushalt.
    Gibt eine Liste von Treffern zurueck.
    """
    sim_info_manager = services.sim_info_manager()
    if not sim_info_manager: return []
    
    search_name = str(name_string).lower().strip()
    
    # Helferfunktion zum Pruefen eines Sims
    def match_name(sim):
        fname = getattr(sim, 'first_name', '').lower()
        lname = getattr(sim, 'last_name', '').lower()
        full_name = f"{fname} {lname}".strip()
        return search_name == fname or search_name == lname or search_name == full_name

    matches_household = []
    matches_global = []

    for sim in sim_info_manager.values():
        if match_name(sim):
            if active_household and sim in active_household:
                matches_household.append(sim)
            else:
                matches_global.append(sim)

    # Prioritaet: Aktiver Haushalt zuerst
    if matches_household:
        return matches_household
    return matches_global

def get_occult_type(sim_info):
    """Gibt den Occult-Typ als einfachen String zurueck (vampire, spellcaster, human...)."""
    occult_str = "human"
    if hasattr(sim_info, 'occult_tracker') and sim_info.occult_tracker.has_any_occult_or_part_occult_trait():
        try:
            ot = sim_info.occult_tracker.occult_types
            if ot:
                occult_str = str(list(ot)[0]).split('.')[-1].lower()
        except:
            occult_str = "occult"
    return occult_str

def is_minor(sim_info):
    """
    Prueft extrem robust, ob der Sim ein Kind, Kleinkind, Saeugling oder Baby ist.
    Sicher gegenkuenftige und alte EA-Patches.
    """
    try:
        # Nativer Check (effizientest, existiert aber in alten Spieleversionen nicht)
        if hasattr(sim_info, 'is_teen_or_older'):
            return not sim_info.is_teen_or_older
            
        # Fallback auf reinen Altersnamen (Sicherer als Enum-Check, da EA gelegentlich Enums erweitert/löscht)
        age_name = str(sim_info.age).split('.')[-1].upper()
        minor_ages = ['BABY', 'INFANT', 'TODDLER', 'CHILD']
        return age_name in minor_ages
    except:
        return False # Bei einem Komplettfehler behandeln wir ihn sicherheitshalber nicht als Kind

def get_auto_set(sim_info, active_household, option_key="option_1"):
    """
    Ermittelt das korrekte Set aus den auto_profiles basierend auf
    Alter, Geschlecht und ob der Sim spielbar (im aktiven Haushalt) ist.
    """
    profiles = mg_config.get("auto_profiles", {}).get(option_key, {})
    
    # Fallback auf Standard, falls Option in Config fehlt
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