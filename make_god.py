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

# --- STANDARD-WERTE ---
DEFAULT_CONFIG = {
    "language": "de",
    "debug_log": True,
    "occult_motives_map": {
        "fairy": ["commodity_motive_fairyoccult_emotionalappetite"],
        "ghost": ["commodity_ghostpowers_stamina"],
        "human": ["motive_hunger", "motive_energy"]
    },
    "auto_profiles": { "option_1": { "playable_male": "0", "playable_female": "0", "npc_male": "1", "npc_female": "1" } },
    "sets": { "0": { "name": "Default", "occult_settings": {} } }
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
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f: ACTIVE_CONFIG = json.load(f)
        except: ACTIVE_CONFIG = DEFAULT_CONFIG.copy()

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
    except Exception as e:
        stats['errors'].append(f"Master-Modul fehlgeschlagen: {e}")

def _apply_occult_motives(sim_info, set_id, _connection, stats, out, debug_console):
    try:
        sets = ACTIVE_CONFIG.get("sets", {})
        active_set = sets.get(str(set_id), sets.get("0", {}))
        occult_type = _get_occult_type(sim_info)
        occult_prefs = active_set.get("occult_settings", {}).get(occult_type, {})

        if not occult_prefs.get("freeze_motives", False): return

        motives_map = active_set.get("occult_motives_map", {})
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
                
        if frozen_count > 0: stats['motives'] = frozen_count
    except Exception as e:
        stats['errors'].append(f"Motive einfrieren fehlgeschlagen: {e}")

def _apply_harmony(sim_info, set_id, _connection, stats, out, debug_console):
    try:
        stat_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
        bit_manager = services.get_instance_manager(sims4.resources.Types.RELATIONSHIP_BIT)
        client = services.client_manager().get(_connection)
        if not client or not client.active_sim: return
        
        bits = {
            "has_met": (bit_manager.get(15803), "relationshipBit_HasMet"),
            "marriage": (bit_manager.get(15816), "romantic-Married"),
            "engaged": (bit_manager.get(15814), "romantic-Engaged"),
            "romance": (bit_manager.get(15822), "romantic-Significant_Other"),
            "best_friends": (bit_manager.get(15794), "friendship-BFF"),
            "friends": (bit_manager.get(15797), "friendship-Good_Friends")
        }
        
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
        p_type = active_set.get("harmony_partnership", "none").lower()
        is_npc = (sim_info.household != client.active_sim.household)
        
        if not is_npc and p_type == "marriage": p_type = "romance"
            
        targets = [client.active_sim.sim_info] if is_npc else list(sim_info.household)

        for member in targets:
            if member and member.sim_id != sim_info.sim_id:
                try:
                    b_met, _ = bits["has_met"]
                    if b_met and not sim_info.relationship_tracker.has_bit(member.sim_id, b_met):
                        sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_met)

                    has_married = sim_info.relationship_tracker.has_bit(member.sim_id, bits["marriage"][0]) if bits["marriage"][0] else False
                    has_engaged = sim_info.relationship_tracker.has_bit(member.sim_id, bits["engaged"][0]) if bits["engaged"][0] else False
                    has_romance = sim_info.relationship_tracker.has_bit(member.sim_id, bits["romance"][0]) if bits["romance"][0] else False
                    has_bff = sim_info.relationship_tracker.has_bit(member.sim_id, bits["best_friends"][0]) if bits["best_friends"][0] else False
                    
                    current_target = p_type
                    
                    if current_target == "marriage" and not has_married:
                        b_obj, b_cmd = bits["marriage"]
                        if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                        if bits["marriage"][0] and not sim_info.relationship_tracker.has_bit(member.sim_id, bits["marriage"][0]):
                            current_target = "romance"
                    
                    if current_target == "engaged" and not has_married and not has_engaged:
                        b_obj, b_cmd = bits["engaged"]
                        if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                    
                    if current_target == "romance" and not has_married and not has_engaged and not has_romance:
                        b_obj, b_cmd = bits["romance"]
                        if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)

                    if current_target == "best_friends" and not has_bff:
                        b_obj, b_cmd = bits["best_friends"]
                        if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                    elif current_target == "friends" and not has_bff:
                        b_obj, b_cmd = bits["friends"]
                        if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)

                    f_track = stat_manager.get(16650)
                    r_track = stat_manager.get(16651)
                    if f_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, active_set.get("harmony_friendship", 100), f_track)
                    if r_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, active_set.get("harmony_romance", 100), r_track)

                except Exception as inner_e:
                    stats['errors'].append(f"Harmonie-Update zu {getattr(member, 'first_name', 'Unbekannt')} fehlgeschlagen: {inner_e}")
                    
        stats['harmony'] = p_type
    except Exception as e:
        stats['errors'].append(f"Harmonie Modul komplett fehlgeschlagen: {e}")

def _apply_traits_and_flags(sim_info, mode, set_id, interest_override, _connection, stats, out, debug_console):
    try:
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
        occult_type = _get_occult_type(sim_info)
        occult_prefs = active_set.get("occult_settings", {}).get(occult_type, {})

        if mode in ['clean', 'remove_bad']:
            excludes = active_set.get("exclude_all", []).copy()
            excludes.extend(occult_prefs.get("exclude", []))
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
            
            for t_name in set(to_add):
                try:
                    sims4.commands.execute(f'traits.equip_trait {t_name} {sim_info.sim_id}', _connection)
                    stats['traits_add'] += 1
                except: pass
    except Exception as e:
        stats['errors'].append("Trait-Modul komplett fehlgeschlagen.")

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
                sid = ACTIVE_CONFIG.get("auto_profiles", {}).get("option_1", {}).get(pk, "0")
            
            _apply_traits_and_flags(sim_info, 'clean', sid, 'auto', _connection, stats, out, debug_console)
            _apply_skills(sim_info, _connection, stats, out, debug_console)
            _apply_occult_motives(sim_info, sid, _connection, stats, out, debug_console)
            _apply_harmony(sim_info, sid, _connection, stats, out, debug_console)
            _apply_master(sim_info, sid, _connection, stats, out, debug_console)
        except: pass

    try:
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), ACTIVE_CONFIG.get("sets", {}).get("0", {}))
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
# DUMP FUNKTIONEN (ANGEPASST FÜR UI TARGETS)
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
    
    # Check ob eine spezifische Sim-ID übergeben wurde (z.B. durch Shift+Click)
    if args_str and args_str[0].lower() == 'id' and len(args_str) > 1:
        try:
            sim_id = int(args_str[1])
            sim_info = services.sim_info_manager().get(sim_id)
        except: pass
            
    # Fallback auf aktiven Sim
    if not sim_info:
        sim_info = client.active_sim.sim_info if client.active_sim else None
        
    if not sim_info:
        out("Fehler: Kein Sim für den Dump gefunden.")
        return

    out(f"Starte vollstaendigen Dump fuer {sim_info.first_name} {sim_info.last_name}...")
    
    # 1. Stats Dump
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

    # 2. Traits Dump
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
    
    # 3. Global All Game Traits Dump
    try:
        global_path = _get_dump_filepath(sim_info, "god_dump_GLOBAL_ALL_TRAITS", False)
        with open(global_path, 'w', encoding='utf-8') as f:
            f.write("=== GLOBALER DUMP: ALLE IM SPIEL GEFUNDENEN TRAITS ===\n")
            f.write("-" * 60 + "\n\n")
            trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)
            all_t = []
            for t in tuple(trait_manager.types.values()):
                try: all_t.append(f"[{str(getattr(t, 'trait_type', 'UNKNOWN')).split('.')[-1]}] {getattr(t, '__name__', str(t))}")
                except: pass
            all_t.sort()
            for line in all_t: f.write(line + "\n")
    except: out("Fehler beim globalen Dump.")
    
    out("Vollstaendiger Dump abgeschlossen! Siehe Mod-Ordner.")


# ==========================================
# INJECTOR FÜR DAS SHIFT+CLICK MENÜ
# ==========================================
MAKE_GOD_INTERACTIONS = [
    17493189874868957557, # Option 1
    17493189874868957558, # Option 2
    17493189874868957559, # Option 3
    17493189874868957560, # Haushalt
    17493189874868957561  # DUMP (Das ist dein 5. Knopf!)
]

original_zone_load = zone.Zone.do_zone_spin_up

def inject_make_god_pie_menu(*args, **kwargs):
    result = original_zone_load(*args, **kwargs)
    try:
        affordance_manager = services.get_instance_manager(sims4.resources.Types.INTERACTION)
        affordances = list(Sim._super_affordances)
        added_count = 0
        
        for interaction_id in MAKE_GOD_INTERACTIONS:
            my_interaction = affordance_manager.get(interaction_id)
            if my_interaction is not None and my_interaction not in affordances:
                affordances.append(my_interaction)
                added_count += 1
                
        if added_count > 0:
            Sim._super_affordances = tuple(affordances)
            _log(f"UI Injection erfolgreich: {added_count} Buttons hinzugefuegt.")
    except Exception as e:
        _log(f"Fehler bei UI Injection: {e}")
                
    return result

zone.Zone.do_zone_spin_up = inject_make_god_pie_menu
load_config()