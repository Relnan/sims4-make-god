import os
import json
import sims4.commands
import services
import sims4.resources
from datetime import datetime
from traits.trait_type import TraitType
from sims.sim_info_types import Gender
from protocolbuffers import Consts_pb2
import zone
from sims.sim import Sim

# --- PFAD-FINDUNG ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.endswith('.ts4script') else CURRENT_DIR
CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')
LOG_FILE = os.path.join(MOD_FOLDER, 'make_god_debug.txt')

# --- STANDARD-WERTE (Wird generiert, wenn keine Config existiert) ---
DEFAULT_CONFIG = {
    "language": "de",
    "debug_log": True,
    "occult_motives_map": {
        "fairy": ["commodity_motive_fairyoccult_emotionalappetite"],
        "ghost": ["commodity_ghostpowers_stamina"],
        "human": ["motive_hunger", "motive_energy"]
    },
    "auto_profiles": {
        "playable_male": "0",
        "playable_female": "0",
        "npc_male": "1",
        "npc_female": "1"
    },
    "sets": {
        "0": {
            "name": "Ultimate God",
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "satisfaction_points": 50000,
            "add_funds": 9999999,
            "max_funds": 9999999,
            "exclude_all": [],
            "traits_all": ["trait_Longevity"]
        }
    }
}

ACTIVE_CONFIG = DEFAULT_CONFIG.copy()

def _log(message):
    if ACTIVE_CONFIG.get("debug_log", False):
        try:
            with open(LOG_FILE, 'a', encoding='utf-8') as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {message}\n")
        except: pass

def load_config():
    global ACTIVE_CONFIG
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f: 
                ACTIVE_CONFIG = json.load(f)
        except Exception as e: 
            _log(f"Fehler beim Laden der Config, nutze Fallback: {e}")
            ACTIVE_CONFIG = DEFAULT_CONFIG.copy()
    else:
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f: 
                json.dump(DEFAULT_CONFIG, f, indent=4)
            ACTIVE_CONFIG = DEFAULT_CONFIG.copy()
        except: pass

def _get_occult_type(sim_info):
    occult_str = "human"
    if hasattr(sim_info, 'occult_tracker') and sim_info.occult_tracker.has_any_occult_or_part_occult_trait():
        try:
            ot = sim_info.occult_tracker.occult_types
            if ot: occult_str = str(list(ot)[0]).split('.')[-1].lower()
        except: occult_str = "occult"
    return occult_str

# --- CORE LOGIK ---
def _apply_skills(sim_info, _connection, stats, out, debug_console):
    try:
        skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        if not skill_manager: return
        count = 0
        for skill_type in tuple(skill_manager.types.values()):
            if hasattr(skill_type, 'is_skill') and skill_type.is_skill:
                tracker = sim_info.get_tracker(skill_type)
                if tracker:
                    try: 
                        tracker.set_value(skill_type, skill_type.max_value)
                        count += 1
                    except: pass
        stats['skills'] = count
        msg = f"Skills maximiert fuer {sim_info.first_name} ({count} Skills)."
        _log(msg)
        if debug_console: out(f"[DEBUG] {msg}")
    except Exception as e:
        stats['errors'].append(f"Skills fehlgeschlagen: {e}")

def _apply_master(sim_info, set_id, _connection, stats, out, debug_console):
    try:
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
        if sim_info.career_tracker:
            for career in tuple(sim_info.career_tracker.careers.values()):
                for _ in range(15):
                    try: career.promote()
                    except: pass
                        
        for _ in range(5):
            try: sims4.commands.execute(f'aspirations.complete_current_milestone {sim_info.sim_id}', _connection)
            except: pass
                
        points = active_set.get("satisfaction_points", 0)
        if points > 0:
            try: sims4.commands.execute(f'sims.give_satisfaction_points {points} {sim_info.sim_id}', _connection)
            except Exception as e: _log(f"Fehler bei Zufriedenheitspunkten: {e}")

        stats['mastered'] = True
        msg = f"Karrieren, Bestreben & Zufriedenheit ({points}) fuer {sim_info.first_name} gemastert."
        _log(msg)
        if debug_console: out(f"[DEBUG] {msg}")
    except Exception as e:
        stats['errors'].append(f"Master-Modul fehlgeschlagen: {e}")

def _apply_occult_motives(sim_info, set_id, _connection, stats, out, debug_console):
    try:
        sets = ACTIVE_CONFIG.get("sets", {})
        active_set = sets.get(str(set_id), sets.get("0", {}))
        occult_type = _get_occult_type(sim_info)
        occult_prefs = active_set.get("occult_settings", {}).get(occult_type, {})

        if not occult_prefs.get("freeze_motives", False): return

        motives_map = ACTIVE_CONFIG.get("occult_motives_map", {})
        targets = motives_map.get(occult_type, [])
        if not targets: return

        stat_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        if not stat_manager: return
        
        frozen_count = 0
        for stat_type in tuple(stat_manager.types.values()):
            stat_name = getattr(stat_type, '__name__', '').lower()
            if stat_name in targets:
                tracker = sim_info.get_tracker(stat_type)
                if tracker:
                    stat_inst = tracker.get_statistic(stat_type)
                    if stat_inst:
                        tracker.set_value(stat_type, stat_inst.max_value)
                        try: stat_inst.add_decay_rate_modifier(0.0)
                        except: pass
                        frozen_count += 1
                
        if frozen_count > 0: 
            stats['motives'] = frozen_count
            msg = f"Motive für {sim_info.first_name} ({occult_type}) in Set {set_id} eingefroren: {frozen_count}"
            _log(msg)
            if debug_console: out(f"[DEBUG] {msg}")
    except Exception as e:
        stats['errors'].append(f"Motive einfrieren fehlgeschlagen: {e}")

def _apply_harmony(sim_info, set_id, _connection, stats, out, debug_console):
    try:
        stat_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        f_track = stat_manager.get(16650) # LTR_Friendship_Main
        r_track = stat_manager.get(16651) # LTR_Romance_Main

        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
        f_val = active_set.get("harmony_friendship", 100)
        r_val = active_set.get("harmony_romance", 100)
        
        count = 0
        for member in tuple(sim_info.household):
            if member.sim_id != sim_info.sim_id:
                try:
                    if f_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, f_val, f_track)
                    if r_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, r_val, r_track)
                    count += 1
                except: pass
                    
        stats['harmony'] = count
        msg = f"Harmonie fuer {sim_info.first_name} mit {count} Haushaltsmitgliedern hergestellt."
        _log(msg)
        if debug_console: out(f"[DEBUG] {msg}")
    except Exception as e:
        stats['errors'].append(f"Harmonie Modul fehlgeschlagen: {e}")

def _apply_traits_and_flags(sim_info, mode, set_id, interest_override, _connection, stats, out, debug_console):
    try:
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
        occult_type = _get_occult_type(sim_info)
        occult_prefs = active_set.get("occult_settings", {}).get(occult_type, {})

        interest = interest_override
        if interest not in ['m', 'f', 'bi']:
            interest = 'bi'

        if mode in ['clean', 'remove_bad']:
            excludes = active_set.get("exclude_all", []).copy()
            excludes.extend(occult_prefs.get("exclude", []))
            
            if sim_info.gender == Gender.MALE: excludes.extend(active_set.get("exclude_sex_male", []))
            elif sim_info.gender == Gender.FEMALE: excludes.extend(active_set.get("exclude_sex_female", []))
            
            if interest == 'm': excludes.extend(active_set.get("exclude_interest_male", []))
            elif interest == 'f': excludes.extend(active_set.get("exclude_interest_female", []))
            elif interest == 'bi': excludes.extend(active_set.get("exclude_interest_bi", []))

            for t in list(sim_info.get_traits()):
                t_name = getattr(t, '__name__', 'unbekannt').lower()
                try:
                    if any(ex in t_name for ex in excludes if ex):
                        sims4.commands.execute(f'traits.remove_trait {t_name} {sim_info.sim_id}', _connection)
                        stats['traits_rem'] += 1
                except: pass

        if mode in ['add_only', 'clean']:
            to_add = active_set.get("traits_all", []).copy()
            to_add.extend(occult_prefs.get("traits", []))
            
            if sim_info.gender == Gender.MALE: to_add.extend(active_set.get("traits_sex_male", []))
            else: to_add.extend(active_set.get("traits_sex_female", []))
            
            if interest == 'm': to_add.extend(active_set.get("flags_interest_male", []))
            elif interest == 'f': to_add.extend(active_set.get("flags_interest_female", []))
            elif interest == 'bi': to_add.extend(active_set.get("flags_interest_bi", []))
            
            for t_name in set(to_add):
                try:
                    sims4.commands.execute(f'traits.equip_trait {t_name} {sim_info.sim_id}', _connection)
                    stats['traits_add'] += 1
                except: pass
                
        msg = f"Traits/Flags für {sim_info.first_name}: {stats['traits_add']} hinzugefügt, {stats['traits_rem']} entfernt."
        _log(msg)
        if debug_console: out(f"[DEBUG] {msg}")
    except Exception as e:
        stats['errors'].append(f"Trait-Modul fehlgeschlagen: {e}")

# --- HAUPT BEFEHL ---
@sims4.commands.Command('make_god', command_type=sims4.commands.CommandType.Live)
def cmd_make_god(*args, _connection=None):
    load_config()
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass

    client = services.client_manager().get(_connection)
    if not client or not client.active_sim: return
    
    active_sim = client.active_sim.sim_info
    active_household = active_sim.household
    targets = []
    set_id = 'auto'
    debug_console = False
    
    args_str = [str(a) for a in args]
    if 'debug' in [a.lower() for a in args_str]:
        debug_console = True
        args_str = [a for a in args_str if a.lower() != 'debug']

    if not args_str:
        targets = list(active_household)
    else:
        mode = args_str[0].lower()
        if mode == 'all':
            targets = list(active_household)
            if len(args_str) > 1: set_id = args_str[1]
        elif mode == 'active':
            targets = [active_sim]
            if len(args_str) > 1: set_id = args_str[1]
        elif mode == 'id':
            if len(args_str) > 1:
                try:
                    sim_id = int(args_str[1])
                    found_sim = services.sim_info_manager().get(sim_id)
                    if found_sim: targets = [found_sim]
                except: pass
            if len(args_str) > 2: set_id = args_str[2]
        else:
            targets = list(active_household)
            set_id = args_str[0]

    if not targets:
        out("[FEHLER] Ziel nicht gefunden.")
        return
        
    for sim_info in targets:
        stats = {
            'traits_rem': 0, 'traits_add': 0, 'skills': 0, 'motives': 0, 
            'mastered': False, 'harmony': 'none', 'errors': []
        }
        try:
            sid = str(set_id)
            if sid == 'auto':
                is_npc = (sim_info.household != active_household)
                pk = f"{'npc' if is_npc else 'playable'}_{'male' if sim_info.gender == Gender.MALE else 'female'}"
                sid = ACTIVE_CONFIG.get("auto_profiles", {}).get(pk, "0")
            
            _apply_traits_and_flags(sim_info, 'clean', sid, 'auto', _connection, stats, out, debug_console)
            _apply_skills(sim_info, _connection, stats, out, debug_console)
            _apply_occult_motives(sim_info, sid, _connection, stats, out, debug_console)
            _apply_harmony(sim_info, sid, _connection, stats, out, debug_console)
            _apply_master(sim_info, sid, _connection, stats, out, debug_console)
            
            if stats['errors'] and debug_console:
                for err in stats['errors']: out(f"[ERROR] {err}")
        except: pass

    try:
        sid_funds = ACTIVE_CONFIG.get("auto_profiles", {}).get("playable_male", "0") if set_id == 'auto' else set_id
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(sid_funds), ACTIVE_CONFIG.get("sets", {}).get("0", {}))
        add_f = active_set.get("add_funds", 0)
        if add_f > 0 and targets:
            current_funds = targets[0].household.funds.money
            new_funds = min(current_funds + add_f, active_set.get("max_funds", 9999999))
            diff = new_funds - current_funds
            if diff > 0:
                targets[0].household.funds.add(diff, Consts_pb2.TELEMETRY_MONEY_CHEAT, targets[0])
    except: pass
    out(f"Make God ausgefuehrt fuer {len(targets)} Sim(s).")


# ==========================================
# DUMP FUNKTIONEN 
# ==========================================
def _get_dump_filepath(sim_info, prefix, include_timestamp=False):
    gender_str = str(sim_info.gender).split('.')[-1].lower()
    occult_str = _get_occult_type(sim_info)
    current_file = os.path.abspath(__file__)
    mod_folder = os.path.dirname(current_file.split('.ts4script')[0]) if '.ts4script' in current_file else os.path.dirname(current_file)
    
    timestamp = "_" + datetime.now().strftime("%Y_%m_%d_%H_%M") if include_timestamp else ""
    filename = f"{prefix}_{gender_str}_{occult_str}_{sim_info.first_name}{timestamp}.txt"
    return os.path.join(mod_folder, filename)

@sims4.commands.Command('make_god_dump', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_dump(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    client = services.client_manager().get(_connection)
    if not client: return
    
    sim_info = None
    args_str = [str(a) for a in args]
    
    if args_str and args_str[0].lower() == 'id' and len(args_str) > 1:
        try:
            sim_id = int(args_str[1])
            sim_info = services.sim_info_manager().get(sim_id)
        except: pass
            
    if not sim_info:
        sim_info = client.active_sim.sim_info if client.active_sim else None
        
    if not sim_info:
        out("Fehler: Kein Sim für den Dump gefunden.")
        return

    out(f"Starte vollstaendigen Dump fuer {sim_info.first_name} {sim_info.last_name}...")
    
    try:
        stats_path = _get_dump_filepath(sim_info, "god_dump_stats", True)
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(f"=== STATISTIC & COMMODITY DUMP FUER {sim_info.first_name} {sim_info.last_name} ===\n")
            f.write("-" * 60 + "\n\n")
            stats_list = []
            if hasattr(sim_info, 'commodity_tracker') and sim_info.commodity_tracker is not None:
                for stat in sim_info.commodity_tracker:
                    try:
                        t = getattr(stat, 'stat_type', type(stat))
                        stats_list.append(f"[COMMODITY] {getattr(t, '__name__', str(t))} : {stat.get_value()}")
                    except: pass
            if hasattr(sim_info, 'statistic_tracker') and sim_info.statistic_tracker is not None:
                for stat in sim_info.statistic_tracker:
                    try:
                        t = getattr(stat, 'stat_type', type(stat))
                        stats_list.append(f"[STATISTIC] {getattr(t, '__name__', str(t))} : {stat.get_value()}")
                    except: pass
            stats_list.sort()
            for line in stats_list: f.write(line + "\n")
    except: out("Fehler beim Stats-Dump.")

    try:
        traits_path = _get_dump_filepath(sim_info, "god_dump_traits", True)
        with open(traits_path, 'w', encoding='utf-8') as f:
            f.write(f"=== TRAITS DUMP FUER {sim_info.first_name} {sim_info.last_name} ===\n")
            f.write("-" * 60 + "\n\n")
            if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker is not None:
                t_list = []
                for t in sim_info.trait_tracker.equipped_traits:
                    t_list.append(f"[{str(getattr(t, 'trait_type', 'UNKNOWN')).split('.')[-1]}] {getattr(t, '__name__', str(t))}")
                t_list.sort()
                for line in t_list: f.write(line + "\n")
    except: out("Fehler beim Traits-Dump.")
    
    out("Vollstaendiger Dump abgeschlossen! Siehe Mod-Ordner.")

# ==========================================
# MANUELLER INJECTOR FÜR DAS SHIFT+CLICK MENÜ
# ==========================================
MAKE_GOD_INTERACTIONS = [
    17493103394834157941, # Option 1
    17493103394834157942, # Option 2
    17493103394834157943, # Option 3
    17493103394834157944, # Haushalt
    17493103394834157945  # DUMP
]

@sims4.commands.Command('make_god_inject', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_inject(_connection=None):
    out = sims4.commands.CheatOutput(_connection)
    
    try:
        affordance_manager = services.get_instance_manager(sims4.resources.Types.INTERACTION)
        if not affordance_manager:
            out("Fehler: Affordance Manager ist nicht bereit.")
            return
            
        affordances = list(Sim._super_affordances)
        added_count = 0
        missing_ids = []
        
        for interaction_id in MAKE_GOD_INTERACTIONS:
            my_interaction = affordance_manager.get(interaction_id)
            if my_interaction is not None:
                if my_interaction not in affordances:
                    affordances.append(my_interaction)
                    added_count += 1
            else:
                missing_ids.append(interaction_id)
                
        if added_count > 0:
            Sim._super_affordances = tuple(affordances)
            out(f"ERFOLG: {added_count} Buttons zum Sim hinzugefuegt!")
            _log(f"Manuelle UI Injection erfolgreich: {added_count} Buttons hinzugefuegt.")
        
        if missing_ids:
            out(f"FEHLSCHLAG: {len(missing_ids)} IDs nicht gefunden. Sind sie in der .package?")
            for mid in missing_ids:
                out(f"-> Vermisse ID: {mid}")
            _log(f"Manuelle UI Injection fehlgeschlagen für IDs: {missing_ids}")
            
        if added_count == 0 and not missing_ids:
            out("INFO: Buttons waren bereits am Sim angeheftet.")
            
    except Exception as e:
        out(f"Schwerer Fehler: {e}")
        _log(f"Fehler bei manueller UI Injection: {e}")

load_config()