import os
import json
import sims4.commands
import services
import sims4.resources
import sims4.hash_util
from datetime import datetime

from traits.trait_type import TraitType
from sims.sim_info_types import Gender

# --- PFAD-FINDUNG ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.endswith('.ts4script') else CURRENT_DIR

CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')
TEMPLATE_FILE = os.path.join(MOD_FOLDER, 'make_god_config_template.json')
LOG_FILE = os.path.join(MOD_FOLDER, 'make_god_debug.txt')

# --- STANDARD-WERTE (FALLBACK & TEMPLATE) ---
DEFAULT_CONFIG = {
    "language": "de",
    "debug_log": True,
    "auto_profiles": {
        "playable_male": "0",
        "playable_female": "0",
        "npc_male": "1",
        "npc_female": "1"
    },
    "sets": {
        "0": {
            "name": "Default God",
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "satisfaction_points": 11000,
            "add_funds": 9999999,
            "max_funds": 9999999,
            "exclude_all": ["evil", "lazy", "mean", "gloomy", "hotheaded", "jealous", "slob", "clumsy", "snob", "erratic"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "exclude_interest_male": [],
            "exclude_interest_female": [],
            "exclude_interest_bi": [],
            "traits_all": [
                "trait_Hidden_IsImmortal"
            ],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "flags_interest_male": ["trait_SexualOrientation_WooHooInterests_Female", "trait_GenderOptions_AttractedTo_Female"],
            "flags_interest_female": ["trait_SexualOrientation_WooHooInterests_Male", "trait_GenderOptions_AttractedTo_Male"],
            "flags_interest_bi": ["trait_SexualOrientation_WooHooInterests_Female", "trait_SexualOrientation_WooHooInterests_Male", "trait_GenderOptions_AttractedTo_Female", "trait_GenderOptions_AttractedTo_Male"]
        },
        "1": {
            "name": "Mortal Rich (Example)",
            "harmony_friendship": 50,
            "harmony_romance": 20,
            "satisfaction_points": 2500,
            "add_funds": 50000,
            "max_funds": 250000,
            "exclude_all": [],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "exclude_interest_male": [],
            "exclude_interest_female": [],
            "exclude_interest_bi": [],
            "traits_all": [],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "flags_interest_male": [],
            "flags_interest_female": [],
            "flags_interest_bi": []
        }
    }
}

LOCALES = {
    "de": {
        "init": "Gott-Modus Initialisierung...",
        "no_target": "Fehler: Kein Ziel-Sim gefunden.",
        "skills_max": "Faehigkeiten maximiert.",
        "traits_added": "Traits und Flags ausgeruestet.",
        "traits_cleaned": "Negative Traits entfernt.",
        "master_done": "Karriere & Bestreben abgeschlossen.",
        "harmony_done": "Haushalts-Harmonie hergestellt.",
        "config_reloaded": "Konfiguration neu geladen!",
        "funds_added": "Haushaltskonto aktualisiert.",
        "set_loaded": "Set geladen: "
    },
    "en": {
        "init": "God Mode initializing...",
        "no_target": "Error: No target Sim found.",
        "skills_max": "Skills maxed out.",
        "traits_added": "Traits and Flags equipped.",
        "traits_cleaned": "Negative traits removed.",
        "master_done": "Career & Aspiration completed.",
        "harmony_done": "Household harmony established.",
        "config_reloaded": "Configuration reloaded!",
        "funds_added": "Household funds updated.",
        "set_loaded": "Loaded Set: "
    }
}

ACTIVE_CONFIG = DEFAULT_CONFIG.copy()
ACTIVE_LOCALE = LOCALES["de"]

# --- DEBUG LOGGER ---
def _log(message):
    if ACTIVE_CONFIG.get("debug_log", False):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except: pass

# --- CONFIG MANAGER ---
def load_config():
    global ACTIVE_CONFIG, ACTIVE_LOCALE
    
    if not os.path.exists(TEMPLATE_FILE):
        try:
            with open(TEMPLATE_FILE, 'w') as f: json.dump(DEFAULT_CONFIG, f, indent=4)
        except: pass

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f: ACTIVE_CONFIG = json.load(f)
        except: ACTIVE_CONFIG = DEFAULT_CONFIG.copy()
    else:
        try:
            with open(CONFIG_FILE, 'w') as f: json.dump(DEFAULT_CONFIG, f, indent=4)
        except: pass

    lang = ACTIVE_CONFIG.get("language", "en")
    ACTIVE_LOCALE = LOCALES.get(lang, LOCALES["en"])
    _log("--- CONFIG GELADEN ---")

def t(key):
    return ACTIVE_LOCALE.get(key, key)

load_config()

# --- HELPER FUNKTIONEN ---
def get_target_sim(target_sim_id, _connection):
    if target_sim_id: return services.sim_info_manager().get(target_sim_id)
    client = services.client_manager().get(_connection)
    return client.active_sim.sim_info if client.active_sim else None

def _apply_skills(sim_info, _connection):
    skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
    count = 0
    for skill_type in tuple(skill_manager.types.values()):
        if hasattr(skill_type, 'is_skill') and skill_type.is_skill:
            tracker = sim_info.get_tracker(skill_type)
            if tracker:
                try: 
                    tracker.set_value(skill_type, skill_type.max_value)
                    count += 1
                except: pass
    _log(f"Skills maximiert fuer {sim_info.first_name} ({count} Skills).")

def _apply_traits_and_flags(sim_info, mode, set_id, interest_override, _connection):
    sets = ACTIVE_CONFIG.get("sets", {})
    active_set = sets.get(str(set_id), sets.get("0", DEFAULT_CONFIG["sets"]["0"]))
    trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)
    current_traits = [getattr(t, '__name__', '').lower() for t in sim_info.get_traits()]
    
    interest = interest_override
    if interest not in ['m', 'f', 'bi']:
        interest = 'm' if sim_info.gender == Gender.MALE else 'f'

    _log(f"Starte Traits fuer {sim_info.first_name} (Mode: {mode}, Set: {set_id}, Interest: {interest})")

    if mode in ['clean', 'remove_bad']:
        bad_keywords = active_set.get("exclude_all", []).copy()
        if sim_info.gender == Gender.MALE: bad_keywords.extend(active_set.get("exclude_sex_male", []))
        elif sim_info.gender == Gender.FEMALE: bad_keywords.extend(active_set.get("exclude_sex_female", []))
        if interest == 'm': bad_keywords.extend(active_set.get("exclude_interest_male", []))
        elif interest == 'f': bad_keywords.extend(active_set.get("exclude_interest_female", []))
        elif interest == 'bi': bad_keywords.extend(active_set.get("exclude_interest_bi", []))

        removed = 0
        for ct in current_traits:
            if any(bad in ct for bad in bad_keywords if bad):
                sims4.commands.execute(f'traits.remove_trait {ct} {sim_info.sim_id}', _connection)
                removed += 1
        _log(f"-> {removed} negative Traits entfernt.")

    if mode in ['add_only', 'clean']:
        dynamic_traits = []
        gameplay_type = getattr(TraitType, 'GAMEPLAY', 1) 
        for trait in tuple(trait_manager.types.values()):
            if getattr(trait, 'trait_type', None) == gameplay_type:
                t_name = getattr(trait, '__name__', '')
                if t_name and not any(bad in t_name.lower() for bad in active_set.get("exclude_all", [])):
                    dynamic_traits.append(t_name)
        
        specific_traits = active_set.get("traits_all", []).copy()
        if sim_info.gender == Gender.MALE: specific_traits.extend(active_set.get("traits_sex_male", []))
        elif sim_info.gender == Gender.FEMALE: specific_traits.extend(active_set.get("traits_sex_female", []))
        if interest == 'm': specific_traits.extend(active_set.get("flags_interest_male", []))
        elif interest == 'f': specific_traits.extend(active_set.get("flags_interest_female", []))
        elif interest == 'bi': specific_traits.extend(active_set.get("flags_interest_bi", []))

        all_good_traits = set(specific_traits + dynamic_traits)
        added = 0
        for t_name in all_good_traits:
            base_name = t_name.split(':')[-1].lower()
            if not any(base_name == ct or base_name in ct for ct in current_traits):
                sims4.commands.execute(f'traits.equip_trait {t_name} {sim_info.sim_id}', _connection)
                added += 1
        _log(f"-> {added} neue Traits/Flags hinzugefuegt.")

def _apply_harmony(sim_info, set_id, _connection):
    stat_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
    
    # In Sims 4 sind das die festen, exakten IDs fuer Freundschaft und Romantik
    f_track = stat_manager.get(16650) # LTR_Friendship_Main
    r_track = stat_manager.get(16651) # LTR_Romance_Main
    
    # Werte aus dem aktiven Set laden (Fallback auf 100)
    sets = ACTIVE_CONFIG.get("sets", {})
    active_set = sets.get(str(set_id), sets.get("0", DEFAULT_CONFIG["sets"]["0"]))
    f_val = active_set.get("harmony_friendship", 100)
    r_val = active_set.get("harmony_romance", 100)

    count = 0
    for member in tuple(sim_info.household):
        if member.sim_id != sim_info.sim_id:
            # 1. Direkte API-Methode
            try:
                if f_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, f_val, f_track)
                if r_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, r_val, r_track)
            except: pass
            
            # 2. Cheat-Befehl Fallback
            try:
                sims4.commands.execute(f'modifyrelationship "{sim_info.first_name}" "{sim_info.last_name}" "{member.first_name}" "{member.last_name}" {f_val} LTR_Friendship_Main', _connection)
                sims4.commands.execute(f'modifyrelationship "{sim_info.first_name}" "{sim_info.last_name}" "{member.first_name}" "{member.last_name}" {r_val} LTR_Romance_Main', _connection)
            except: pass
            
            count += 1
            
    _log(f"Harmonie fuer {sim_info.first_name} mit {count} Haushaltsmitgliedern hergestellt (F:{f_val} / R:{r_val}).")

def _apply_master(sim_info, _connection):
    if sim_info.career_tracker:
        active_careers = tuple(sim_info.career_tracker.careers.values())
        for career in active_careers:
            try:
                for _ in range(15): career.promote()
                sim_info.career_tracker.remove_career(career.guid64)
            except: pass
    try:
        for _ in range(5): sims4.commands.execute(f'aspirations.complete_current_milestone {sim_info.sim_id}', _connection)
    except: pass
    _log(f"Karrieren & Bestreben fuer {sim_info.first_name} gemastert.")

# --- BEFEHLE (COMMANDS) ---
@sims4.commands.Command('reload_god_config', command_type=sims4.commands.CommandType.Live)
def cmd_reload_config(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    load_config()
    output(t("config_reloaded"))

@sims4.commands.Command('skill_god', command_type=sims4.commands.CommandType.Live)
def cmd_skill_god(target_sim_id:int=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_target_sim(target_sim_id, _connection)
    if not sim_info: return output(t("no_target"))
    _apply_skills(sim_info, _connection)
    output(f"{sim_info.first_name}: {t('skills_max')}")

# FEHLER BEHOBEN: target_sim_id ist nun der letzte Parameter, damit "remove_bad" als Mode erkannt wird!
@sims4.commands.Command('trait_god', command_type=sims4.commands.CommandType.Live)
def cmd_trait_god(mode:str='add_only', set_id:str='0', interest_override:str='auto', target_sim_id:int=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_target_sim(target_sim_id, _connection)
    if not sim_info: return output(t("no_target"))
    
    _apply_traits_and_flags(sim_info, mode, set_id, interest_override, _connection)
    set_name = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {}).get("name", f"Set {set_id}")
    output(f"{t('set_loaded')}{set_name}")
    if mode in ['clean', 'remove_bad']: output(f"{sim_info.first_name}: {t('traits_cleaned')}")
    if mode in ['add_only', 'clean']: output(f"{sim_info.first_name}: {t('traits_added')}")

@sims4.commands.Command('harmony_god', command_type=sims4.commands.CommandType.Live)
def cmd_harmony_god(set_id:str='0', target_sim_id:int=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_target_sim(target_sim_id, _connection)
    if not sim_info: return output(t("no_target"))
    _apply_harmony(sim_info, set_id, _connection)
    output(f"{sim_info.first_name}: {t('harmony_done')}")

@sims4.commands.Command('master_god', command_type=sims4.commands.CommandType.Live)
def cmd_master_god(target_sim_id:int=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_target_sim(target_sim_id, _connection)
    if not sim_info: return output(t("no_target"))
    _apply_master(sim_info, _connection)
    output(f"{sim_info.first_name}: {t('master_done')}")

@sims4.commands.Command('make_god', command_type=sims4.commands.CommandType.Live)
def cmd_make_god(target_mode:str='active', set_id:str='0', interest_override:str='auto', _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output(t("init"))
    
    client = services.client_manager().get(_connection)
    if not client or not client.active_sim: return output(t("no_target"))
    
    targets = []
    if target_mode == 'all': targets = list(client.active_sim.sim_info.household)
    elif target_mode == 'active': targets = [client.active_sim.sim_info]
    elif target_mode.isdigit():
        sim_info = services.sim_info_manager().get(int(target_mode))
        if sim_info: targets = [sim_info]

    sets = ACTIVE_CONFIG.get("sets", {})
    active_set = sets.get(str(set_id), sets.get("0", DEFAULT_CONFIG["sets"]["0"]))
    set_name = active_set.get("name", f"Set {set_id}")
    output(f"{t('set_loaded')}{set_name}")
    _log(f"--- BATCH MAKE_GOD GESTARTET (Targets: {len(targets)}) ---")

    for sim_info in targets:
        _apply_traits_and_flags(sim_info, 'clean', set_id, interest_override, _connection)
        _apply_skills(sim_info, _connection)
        _apply_harmony(sim_info, set_id, _connection)
        _apply_master(sim_info, _connection)
        sat_points = active_set.get("satisfaction_points", 0)
        if sat_points > 0:
            sims4.commands.execute(f'sims.give_satisfaction_points {sat_points} {sim_info.sim_id}', _connection)
    
    try:
        if targets:
            first_sim = targets[0]
            current_funds = first_sim.household.funds.money
            add_f = active_set.get("add_funds", 0)
            max_f = active_set.get("max_funds", 9999999)
            new_funds = min(current_funds + add_f, max_f)
            diff = new_funds - current_funds
            if diff > 0:
                sims4.commands.execute(f'sims.modify_funds {diff}', _connection)
                output(t("funds_added"))
                _log(f"Haushaltskonto erhoeht um {diff}.")
    except: pass

@sims4.commands.Command('make_god_auto', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_auto(target_sim_id:int=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_target_sim(target_sim_id, _connection)
    if not sim_info: return output(t("no_target"))
    
    is_npc = getattr(sim_info, 'is_npc', False)
    status_key = "npc" if is_npc else "playable"
    gender_key = "male" if sim_info.gender == Gender.MALE else "female"
    profile_key = f"{status_key}_{gender_key}"
    
    auto_profiles = ACTIVE_CONFIG.get("auto_profiles", {})
    set_id = auto_profiles.get(profile_key, "0")
    
    active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
    set_name = active_set.get("name", f"Set {set_id}")
    output(f"Auto-Detect ({profile_key}): {t('set_loaded')}{set_name}")
    _log(f"--- MAKE_GOD_AUTO GESTARTET fuer {sim_info.first_name} (Profil: {profile_key}) ---")

    _apply_traits_and_flags(sim_info, 'clean', set_id, 'auto', _connection)
    _apply_skills(sim_info, _connection)
    _apply_harmony(sim_info, set_id, _connection)
    _apply_master(sim_info, _connection)
    
    sat_points = active_set.get("satisfaction_points", 0)
    if sat_points > 0:
        sims4.commands.execute(f'sims.give_satisfaction_points {sat_points} {sim_info.sim_id}', _connection)
    
    if not is_npc:
        try:
            current_funds = sim_info.household.funds.money
            add_f = active_set.get("add_funds", 0)
            max_f = active_set.get("max_funds", 9999999)
            new_funds = min(current_funds + add_f, max_f)
            diff = new_funds - current_funds
            if diff > 0:
                sims4.commands.execute(f'sims.modify_funds {diff}', _connection)
                output(t("funds_added"))
                _log(f"Haushaltskonto erhoeht um {diff}.")
        except: pass

@sims4.commands.Command('dump_traits_god', command_type=sims4.commands.CommandType.Live)
def cmd_dump_traits_god(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)
    
    dump_file = os.path.join(MOD_FOLDER, 'all_traits_dump.txt')
    output("Sammle und analysiere Traits & Flags...")
    _log("Dump_traits_god ausgefuehrt.")
    
    list_traits, list_flags, list_others = [], [], []
    
    for trait in tuple(trait_manager.types.values()):
        t_name = getattr(trait, '__name__', 'UNKNOWN')
        t_type_raw = getattr(trait, 'trait_type', 'UNKNOWN')
        t_type = str(t_type_raw).split('.')[-1] 
        line = f"[{t_type}] {t_name}"
        
        if t_type in ['PERSONALITY', 'GAMEPLAY', 'ASPIRATION', 'REWARD']: list_traits.append(line)
        elif t_type == 'HIDDEN' or 'GenderOptions' in t_name or 'SexualOrientation' in t_name: list_flags.append(line)
        else: list_others.append(line)
            
    list_traits.sort()
    list_flags.sort()
    list_others.sort()
    
    try:
        with open(dump_file, 'w') as f:
            f.write("=== SICHTBARE TRAITS ===\n")
            for line in list_traits: f.write(line + "\n")
            f.write("\n\n=== VERSTECKTE FLAGS ===\n")
            for line in list_flags: f.write(line + "\n")
            f.write("\n\n=== SONSTIGE ===\n")
            for line in list_others: f.write(line + "\n")
        output("Erfolg! Liste in all_traits_dump.txt gespeichert.")
    except:
        output("Fehler beim Erstellen der Liste.")