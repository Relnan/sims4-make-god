import os
import json
import sims4.commands
import services
import sims4.resources
from datetime import datetime
from traits.trait_type import TraitType
from sims.sim_info_types import Gender
from protocolbuffers import Consts_pb2

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

# --- CORE LOGIK (MIT STATS-TRACKING) ---
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
        _log(f"Fehler bei Skills fuer {sim_info.first_name}: {e}")

def _apply_master(sim_info, set_id, _connection, stats, out, debug_console):
    try:
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
        
        # 1. Karriere maximieren
        if sim_info.career_tracker:
            for career in tuple(sim_info.career_tracker.careers.values()):
                for _ in range(15):
                    try: career.promote()
                    except: pass
                        
        # 2. Bestreben abschließen
        for _ in range(5):
            try: sims4.commands.execute(f'aspirations.complete_current_milestone {sim_info.sim_id}', _connection)
            except: pass
                
        # 3. Zufriedenheitspunkte vergeben (Zurueck zum bewaehrten Cheat aus dem alten Skript!)
        points = active_set.get("satisfaction_points", 0)
        if points > 0:
            try:
                sims4.commands.execute(f'sims.give_satisfaction_points {points} {sim_info.sim_id}', _connection)
            except Exception as e:
                _log(f"Fehler bei Zufriedenheitspunkten: {e}")

        stats['mastered'] = True
        msg = f"Karrieren, Bestreben & Zufriedenheit ({points}) fuer {sim_info.first_name} gemastert."
        _log(msg)
        if debug_console: out(f"[DEBUG] {msg}")
    except Exception as e:
        stats['errors'].append(f"Master-Modul fehlgeschlagen: {e}")
        _log(f"Fehler im Master-Modul fuer {sim_info.first_name}: {e}")

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
        bit_manager = services.get_instance_manager(sims4.resources.Types.RELATIONSHIP_BIT)
        client = services.client_manager().get(_connection)
        if not client or not client.active_sim: return
        
        bits = {
            "marriage": (bit_manager.get(15816), "romantic-Married"),
            "engaged": (bit_manager.get(15814), "romantic-Engaged"),
            "romance": (bit_manager.get(15822), "romantic-Significant_Other"),
            "best_friends": (bit_manager.get(15794), "friendship-BFF"),
            "friends": (bit_manager.get(15797), "friendship-Good_Friends")
        }
        
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), {})
        p_type = active_set.get("harmony_partnership", "none").lower()
        
        is_npc = (sim_info.household != client.active_sim.household)
        
        if not is_npc and p_type == "marriage":
            p_type = "romance"
            if debug_console: out(f"[DEBUG] Haushalts-Override: Marriage -> Romance fuer {sim_info.first_name}")
            
        targets = [client.active_sim.sim_info] if is_npc else list(sim_info.household)

        for member in targets:
            if member and member.sim_id != sim_info.sim_id:
                try:
                    f_track = stat_manager.get(16650)
                    r_track = stat_manager.get(16651)
                    if f_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, active_set.get("harmony_friendship", 100), f_track)
                    if r_track: sim_info.relationship_tracker.set_relationship_score(member.sim_id, active_set.get("harmony_romance", 100), r_track)
                    
                    has_married = sim_info.relationship_tracker.has_bit(member.sim_id, bits["marriage"][0]) if bits["marriage"][0] else False
                    has_engaged = sim_info.relationship_tracker.has_bit(member.sim_id, bits["engaged"][0]) if bits["engaged"][0] else False
                    has_romance = sim_info.relationship_tracker.has_bit(member.sim_id, bits["romance"][0]) if bits["romance"][0] else False
                    has_bff = sim_info.relationship_tracker.has_bit(member.sim_id, bits["best_friends"][0]) if bits["best_friends"][0] else False
                    
                    current_target = p_type
                    
                    if current_target == "marriage":
                        if not has_married:
                            b_obj, b_cmd = bits["marriage"]
                            if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                            if b_cmd: sims4.commands.execute(f'relationship.add_bit {sim_info.sim_id} {member.sim_id} {b_cmd}', _connection)
                            
                            if bits["marriage"][0] and not sim_info.relationship_tracker.has_bit(member.sim_id, bits["marriage"][0]):
                                current_target = "romance"
                                stats['errors'].append(f"Hochzeit mit {member.first_name} blockiert, Fallback auf Romance.")
                                if debug_console: out(f"[DEBUG ERROR] Hochzeit blockiert. Kaskade zu Romance.")
                    
                    if current_target == "engaged":
                        if not has_married and not has_engaged:
                            b_obj, b_cmd = bits["engaged"]
                            if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                            if b_cmd: sims4.commands.execute(f'relationship.add_bit {sim_info.sim_id} {member.sim_id} {b_cmd}', _connection)
                            
                            if bits["engaged"][0] and not sim_info.relationship_tracker.has_bit(member.sim_id, bits["engaged"][0]):
                                current_target = "romance"
                                stats['errors'].append(f"Verlobung mit {member.first_name} blockiert, Fallback auf Romance.")
                    
                    if current_target == "romance":
                        if not has_married and not has_engaged and not has_romance:
                            b_obj, b_cmd = bits["romance"]
                            if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                            if b_cmd: sims4.commands.execute(f'relationship.add_bit {sim_info.sim_id} {member.sim_id} {b_cmd}', _connection)

                    if current_target == "best_friends":
                        if not has_bff:
                            b_obj, b_cmd = bits["best_friends"]
                            if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                            if b_cmd: sims4.commands.execute(f'relationship.add_bit {sim_info.sim_id} {member.sim_id} {b_cmd}', _connection)
                    elif current_target == "friends":
                        if not has_bff:
                            b_obj, b_cmd = bits["friends"]
                            if b_obj: sim_info.relationship_tracker.add_relationship_bit(member.sim_id, b_obj)
                            if b_cmd: sims4.commands.execute(f'relationship.add_bit {sim_info.sim_id} {member.sim_id} {b_cmd}', _connection)

                except Exception as inner_e:
                    stats['errors'].append(f"Harmonie-Update zu {getattr(member, 'first_name', 'Unbekannt')} uebersprungen.")
                    
        stats['harmony'] = p_type
        msg = f"Harmonie fuer {sim_info.first_name} aktualisiert (Ziel-Status: {p_type})."
        _log(msg)
        if debug_console: out(f"[DEBUG] {msg}")
    except Exception as e:
        stats['errors'].append(f"Harmonie Modul fehlgeschlagen.")

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
                        if debug_console: out(f"[DEBUG] Trait entfernt: {t_name}")
                except Exception: 
                    stats['errors'].append(f"Konnte Trait '{t_name}' nicht entfernen.")

        if mode in ['add_only', 'clean']:
            to_add = active_set.get("traits_all", []).copy()
            to_add.extend(occult_prefs.get("traits", []))
            if sim_info.gender == Gender.MALE: to_add.extend(active_set.get("traits_sex_male", []))
            else: to_add.extend(active_set.get("traits_sex_female", []))
            
            for t_name in set(to_add):
                try:
                    sims4.commands.execute(f'traits.equip_trait {t_name} {sim_info.sim_id}', _connection)
                    stats['traits_add'] += 1
                    if debug_console: out(f"[DEBUG] Trait hinzugefuegt: {t_name}")
                except Exception:
                    stats['errors'].append(f"Konnte Trait '{t_name}' nicht hinzufuegen.")
                    
        _log(f"-> {stats['traits_rem']} Traits entfernt, {stats['traits_add']} Traits hinzugefuegt.")
    except Exception as e:
        stats['errors'].append("Trait-Modul komplett fehlgeschlagen.")

# --- BEFEHLE ---
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
    
    # 1. Debug-Flag herausfiltern, egal wo es steht
    args_str = [str(a) for a in args]
    if 'debug' in [a.lower() for a in args_str]:
        debug_console = True
        args_str = [a for a in args_str if a.lower() != 'debug']

    # 2. Argumente intelligent parsen
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
        elif mode == 'name':
            if len(args_str) > 2:
                first = args_str[1].lower()
                last = args_str[2].lower()
                for sim in services.sim_info_manager().get_all():
                    if getattr(sim, 'first_name', '').lower() == first and getattr(sim, 'last_name', '').lower() == last:
                        targets = [sim]
                        break
            if len(args_str) > 3: set_id = args_str[3]
        else:
            targets = list(active_household)
            set_id = args_str[0]

    # Fehler werfen, falls Target nicht existiert
    if not targets:
        out("[FEHLER] Ziel nicht gefunden. Ueberpruefe Name oder ID.")
        return
        
    _log(f"--- BATCH MAKE_GOD GESTARTET (Targets: {len(targets)}) ---")
    if debug_console: out(f"--- BATCH MAKE_GOD GESTARTET (Debug Mode ON) ---")
    
    for sim_info in targets:
        out(f"--- {sim_info.first_name} gestartet ---")
        
        # Tracking-Dictionary pro Sim
        stats = {
            'traits_rem': 0, 'traits_add': 0,
            'skills': 0, 'motives': 0, 'mastered': False,
            'harmony': 'none', 'errors': []
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
            
        except Exception as e:
            msg = f"SCHWERER FEHLER bei {getattr(sim_info, 'first_name', 'Sim')}: {str(e)}"
            _log(msg)
            stats['errors'].append(msg)

        # Zusammenfassung in der Konsole ausgeben
        for err in stats['errors']:
            out(f"  -> Uebersprungen/Fehler: {err}")
            
        changes = stats['traits_rem'] + stats['traits_add'] + stats['skills'] + stats['motives']
        if changes == 0 and not stats['mastered']:
            out(f"--- {sim_info.first_name} abgeschlossen: Keine Aenderungen vorgenommen.\n")
        else:
            out(f"--- {sim_info.first_name} abgeschlossen: +{stats['traits_add']} Traits, -{stats['traits_rem']} Traits, {stats['skills']} Skills max, {stats['motives']} Motive fixiert.\n")

    try:
        active_set = ACTIVE_CONFIG.get("sets", {}).get(str(set_id), ACTIVE_CONFIG.get("sets", {}).get("0", {}))
        add_f = active_set.get("add_funds", 0)
        if add_f > 0 and targets:
            current_funds = targets[0].household.funds.money
            new_funds = min(current_funds + add_f, active_set.get("max_funds", 9999999))
            diff = new_funds - current_funds
            if diff > 0:
                targets[0].household.funds.add(diff, Consts_pb2.TELEMETRY_MONEY_CHEAT, targets[0])
                _log(f"Haushaltskonto erhoeht um {diff}.")
                out(f"--- Haushaltskonto um {diff} Simoleons erhoeht ---")
    except: pass

# ==========================================
# DUMP FUNKTIONEN
# ==========================================
def _get_dump_filepath(sim_info, prefix, include_timestamp=False):
    gender_str = str(sim_info.gender).split('.')[-1].lower()
    occult_str = "human"
    if hasattr(sim_info, 'occult_tracker') and sim_info.occult_tracker is not None:
        if sim_info.occult_tracker.has_any_occult_or_part_occult_trait():
            try:
                occult_types = sim_info.occult_tracker.occult_types
                if occult_types:
                    occult_str = str(list(occult_types)[0]).split('.')[-1].lower()
            except:
                occult_str = "occult"
                
    current_file = os.path.abspath(__file__)
    mod_folder = os.path.dirname(current_file.split('.ts4script')[0]) if '.ts4script' in current_file else os.path.dirname(current_file)
    
    timestamp = ""
    if include_timestamp:
        # Format: Jahr_Monat_Tag_Stunde_Minute
        timestamp = "_" + datetime.now().strftime("%Y_%m_%d_%H_%M")
    
    filename = f"{prefix}_{gender_str}_{occult_str}_{sim_info.first_name}{timestamp}.txt"
    return os.path.join(mod_folder, filename)

@sims4.commands.Command('make_god_dump_stats', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_dump_stats(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    client = services.client_manager().get(_connection)
    if client is None or client.active_sim is None: return
    
    sim_info = client.active_sim.sim_info
    # Hier setzen wir include_timestamp=True
    filepath = _get_dump_filepath(sim_info, "god_dump_stats", include_timestamp=True)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"=== STATISTIC & COMMODITY DUMP FUER {sim_info.first_name} {sim_info.last_name} ===\n")
            f.write("-" * 60 + "\n\n")
            
            stats_list = []
            
            # 1. Commodities (Bedürfnisse, Motives, Occult Energie)
            if hasattr(sim_info, 'commodity_tracker') and sim_info.commodity_tracker is not None:
                for stat in sim_info.commodity_tracker:
                    try:
                        stat_type = getattr(stat, 'stat_type', type(stat))
                        stat_name = getattr(stat_type, '__name__', str(stat_type))
                        current_value = stat.get_value()
                        stats_list.append(f"[COMMODITY] {stat_name} : {current_value}")
                    except: pass
            
            # 2. Reguläre Statistiken
            if hasattr(sim_info, 'statistic_tracker') and sim_info.statistic_tracker is not None:
                for stat in sim_info.statistic_tracker:
                    try:
                        stat_type = getattr(stat, 'stat_type', type(stat))
                        stat_name = getattr(stat_type, '__name__', str(stat_type))
                        current_value = stat.get_value()
                        stats_list.append(f"[STATISTIC] {stat_name} : {current_value}")
                    except: pass
            
            stats_list.sort()
            if stats_list:
                for line in stats_list:
                    f.write(line + "\n")
            else:
                f.write("Keine Statistiken oder Commodities gefunden.\n")
                    
        output(f"Stats-Dump erfolgreich: {filepath}")
    except Exception as e:
        output(f"Fehler beim Erstellen des Stats-Dumps: {e}")

@sims4.commands.Command('make_god_dump_traits', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_dump_traits(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    client = services.client_manager().get(_connection)
    
    if client is None or client.active_sim is None:
        output("Fehler: Kein aktiver Sim gefunden.")
        return
        
    sim_info = client.active_sim.sim_info
    filepath = _get_dump_filepath(sim_info, "god_dump_traits", include_timestamp=True)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"=== TRAITS DUMP FUER {sim_info.first_name} {sim_info.last_name} ===\n")
            f.write("-" * 60 + "\n\n")
            
            if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker is not None:
                traits_list = []
                for trait in sim_info.trait_tracker.equipped_traits:
                    trait_name = getattr(trait, '__name__', str(trait))
                    trait_type = str(getattr(trait, 'trait_type', 'UNKNOWN')).split('.')[-1]
                    traits_list.append(f"[{trait_type}] {trait_name}")
                
                traits_list.sort()
                for line in traits_list:
                    f.write(line + "\n")
            else:
                f.write("Kein Trait-Tracker gefunden.\n")
                    
        output(f"Traits-Dump erfolgreich: {filepath}")
    except Exception as e:
        output(f"Fehler beim Erstellen des Traits-Dumps: {e}")

@sims4.commands.Command('make_god_dump_all_game_traits', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_dump_all_game_traits(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    # Greift auf den globalen Manager für alle Traits im Spiel zu
    trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)

    # Nutzt denselben zentralen Helper wie die anderen Dump-Funktionen
    # und erzeugt bewusst keinen Zeitstempel.
    client = services.client_manager().get(_connection)
    if client is None or client.active_sim is None:
        output("Fehler: Kein aktiver Sim gefunden.")
        return

    sim_info = client.active_sim.sim_info
    filepath = _get_dump_filepath(sim_info, "god_dump_GLOBAL_ALL_TRAITS", include_timestamp=False)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=== GLOBALER DUMP: ALLE IM SPIEL GEFUNDENEN TRAITS ===\n")
            f.write("Nutzbar für deine 'traits_all' oder 'exclude' Listen\n")
            f.write("-" * 60 + "\n\n")
            
            all_traits = []
            for trait in tuple(trait_manager.types.values()):
                try:
                    t_name = getattr(trait, '__name__', str(trait))
                    # Bestimmt den Typ (PERSONALITY, GAMEPLAY, HIDDEN etc.)
                    t_type = str(getattr(trait, 'trait_type', 'UNKNOWN')).split('.')[-1]
                    all_traits.append(f"[{t_type}] {t_name}")
                except: pass
            
            all_traits.sort()
            for line in all_traits:
                f.write(line + "\n")
                
        output(f"Globaler Trait-Dump erfolgreich! Datei: {filepath}")
    except Exception as e:
        output(f"Fehler beim globalen Dump: {e}")

@sims4.commands.Command('make_god_dump', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_dump_all(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("Starte vollstaendigen Dump (Stats & Traits)...")
    cmd_make_god_dump_stats(_connection)
    cmd_make_god_dump_traits(_connection)
    cmd_make_god_dump_all_game_traits(_connection)
    output("Vollstaendiger Dump abgeschlossen! Siehe Mod-Ordner.")

load_config()