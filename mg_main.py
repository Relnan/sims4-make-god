import sims4.commands
import services
import re

import mg_config
import mg_logger
import mg_utils
import mg_queue
import mg_dump

# Erlaubt benutzerfreundliche Eingaben wie option1/option_1/opt1
def _normalize_selector(value):
    raw = str(value).lower().strip()
    m = re.match(r'^(?:option_?|opt)(\d+)$', raw)
    if m:
        return f"option_{m.group(1)}"
    return raw

# --- NEU: ZENTRALER ARGUMENT-PARSER ---
def _parse_args_and_debug(args):
    """Filtert das Schlüsselwort 'debug' ausschliesslich am Ende der Eingabe heraus."""
    args_list = [str(a).lower().strip() for a in args]
    force_debug = False
    
    # Prüft und entfernt 'debug' nur, wenn es das allerletzte Argument ist.
    # So bleiben Namen wie "Male Debug" (in Quotes) oder "Debug Mueller" (als Mittelwort) intakt.
    while args_list and args_list[-1] == 'debug':
        force_debug = True
        args_list.pop()
        
    return args_list, force_debug

# Initiales Laden beim Import
mg_config.load_config()

# --- HAUPT-ROUTING (Akzeptiert nun 'rmg' und 'make_god' als Befehl) ---
@sims4.commands.Command('rmg', 'make_god', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_base(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    # 1. Parameter global bereinigen
    args_list, force_debug = _parse_args_and_debug(args)
    
    mg_config.load_config()
    client = services.client_manager().get(_connection)
    if not client: return
    
    if not args_list:
        out("=== Relnans Make God (RMG) - Befehlsreferenz ===")
        out("Nutzung: rmg [Modus] [Set_ID|auto|option_X] [debug]")
        out(" ")
        out("Verfuegbare Shortcuts:")
        out("- rmg.all [Set_ID]    -> Auf den ganzen Haushalt.")
        out("- rmg.active [Set_ID] -> Nur auf den aktiven Sim.")
        out("- rmg.add id <ID>     -> Verbindet Sim via ID mit aktivem Sim.")
        out("- rmg.add name <Name> -> Verbindet Sim via Name mit aktivem Sim.")
        out("- rmg.id <ID> [Set_ID]-> Wendet Profil auf ID an.")
        out("- rmg.name \"Name\"     -> Wendet Profil auf gefundenen Sim an.")
        out("- rmg.dump            -> Erstellt einen Textdatei-Dump.")
        out("==================================================")
        return
        
    active_sim_info = client.active_sim.sim_info if client.active_sim else None
    active_household_raw = active_sim_info.household if active_sim_info else None
    
    if not active_household_raw:
        out("[FEHLER] Kein aktiver Haushalt.")
        return
        
    active_household = []
    for sim in active_household_raw:
        try:
            if str(sim.age).split('.')[-1].upper() != 'BABY':
                active_household.append(sim)
        except:
            active_household.append(sim)
            
    targets = []
    set_id = 'auto'
    mode = 'all'

    if args_list:
        mode = args_list[0]
        
    if mode == 'all':
        targets = list(active_household)
        inc_roommates = mg_config.get("include_roommates_in_all", False)
        inc_keyholders = mg_config.get("include_keyholders_in_all", False)
        
        if (inc_roommates or inc_keyholders) and active_sim_info:
            tracker = getattr(active_sim_info, 'relationship_tracker', None)
            if tracker:
                target_ids_in_household = [t.sim_id for t in targets]
                for target_id in tuple(tracker.target_sim_gen()):
                    if target_id not in target_ids_in_household:
                        for bit in tuple(tracker.get_all_bits(target_id)):
                            b_name = getattr(bit, '__name__', '').lower()
                            if (inc_roommates and 'roommate' in b_name) or (inc_keyholders and 'key' in b_name):
                                target_sim = mg_utils.get_sim_by_id(target_id)
                                if target_sim:
                                    targets.append(target_sim)
                                break
                                
        if len(args_list) > 1: set_id = _normalize_selector(args_list[1])
    elif mode == 'active':
        if active_sim_info: targets = [active_sim_info]
        if len(args_list) > 1: set_id = _normalize_selector(args_list[1])
    elif mode == 'id':
        if len(args_list) > 1:
            try:
                found_sim = mg_utils.get_sim_by_id(int(args_list[1]))
                if found_sim: targets = [found_sim]
            except: pass
        if len(args_list) > 2: set_id = _normalize_selector(args_list[2])
    elif mode == 'name':
        if len(args_list) > 1:
            search_str = " ".join(args_list[1:])
            matches = mg_utils.get_sims_by_fuzzy_name(search_str, active_household)
            if len(matches) == 1:
                targets = matches
            elif len(matches) > 1:
                out(f"[FEHLER] Mehrdeutiger Name: {len(matches)} Sims gefunden fuer '{search_str}'.")
                max_lines = 20
                for i, sim in enumerate(matches[:max_lines], start=1):
                    sim_id = getattr(sim, 'sim_id', 'unbekannt')
                    first = getattr(sim, 'first_name', '')
                    last = getattr(sim, 'last_name', '')
                    try: hh_name = getattr(sim.household, 'name', 'Unbekannt') if getattr(sim, 'household', None) else 'Unbekannt'
                    except: hh_name = 'Unbekannt'
                    out(f"{i}. {first} {last} | ID: {sim_id} | HH: {hh_name}")
                if len(matches) > max_lines:
                    out(f"... und {len(matches) - max_lines} weitere Treffer.")
                out("Bitte nutze rmg.id <SimID> oder gib einen genaueren Namen an.")
                return
        if len(args_list) > 2: set_id = _normalize_selector(args_list[2])
    else:
        targets = list(active_household)
        set_id = _normalize_selector(args_list[0])

    if not targets:
        out("[FEHLER] Keine passenden Sims gefunden.")
        return

    out(f"Sende {len(targets)} Sim(s) an die Queue fuer Set '{set_id}'...")
    mg_queue.start_queue(targets, set_id, active_household, out, force_debug, _connection)


# --- MANUELLE VERKNÜPFUNG (rmg.add) ---
@sims4.commands.Command('rmg.add', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_add(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    # 1. Parameter global bereinigen
    args_list, force_debug = _parse_args_and_debug(args)
    
    mg_config.load_config()
    client = services.client_manager().get(_connection)
    if not client: return
    active_sim_info = client.active_sim.sim_info if client.active_sim else None
    
    if not active_sim_info:
        out("[FEHLER] Kein aktiver Sim gefunden. Aktiviere einen Sim.")
        return

    if len(args_list) < 2:
        out("Nutzung: rmg.add name <Name> ODER rmg.add id <SimID>")
        return
        
    mode = args_list[0]
    target_sim = None
    
    if mode == 'id':
        try: target_sim = mg_utils.get_sim_by_id(int(args_list[1]))
        except: pass
        if not target_sim:
            out(f"[FEHLER] Kein Sim mit der ID {args_list[1]} gefunden.")
            return
    elif mode == 'name':
        search_str = " ".join(args_list[1:])
        matches = mg_utils.get_sims_by_fuzzy_name(search_str)
        if not matches:
            out(f"[FEHLER] Kein Sim gefunden fuer Teilstring '{search_str}'.")
            return
        elif len(matches) > 1:
            out(f"[INFO] Mehrere moegliche Sims gefunden fuer '{search_str}':")
            max_lines = 15
            for i, sim in enumerate(matches[:max_lines], start=1):
                sim_id = getattr(sim, 'sim_id', 'unbekannt')
                first = getattr(sim, 'first_name', '')
                last = getattr(sim, 'last_name', '')
                hh_id = getattr(sim, 'household_id', 'Unbekannt')
                try: hh_name = getattr(sim.household, 'name', 'Unbekannt') if getattr(sim, 'household', None) else 'Unbekannt'
                except: hh_name = 'Unbekannt'
                
                out(f"{i}. {first} {last} | ID: {sim_id} | HH: {hh_name} ({hh_id})")
            out("Bitte nutze 'rmg.add id <SimID>' mit der korrekten ID aus der Liste.")
            return
        else:
            target_sim = matches[0]
    else:
        out("Unbekannter Modus. Nutze 'rmg.add name' oder 'rmg.add id'.")
        return
        
    if target_sim.sim_id == active_sim_info.sim_id:
        out("[FEHLER] Du kannst den aktiven Sim nicht mit sich selbst verknuepfen.")
        return
        
    out(f"Starte rmg.add fuer Ziel-Sim: {getattr(target_sim, 'first_name', '')} {getattr(target_sim, 'last_name', '')}")
    out("[HINWEIS] Wenn der Ziel-Sim aktuell nicht im Level geladen (hidden) ist, koennen bestimmte Beziehungs-Updates stumm fehlschlagen.")
    
    import mg_feat_relations
    settings = mg_config.get("manual_add_settings", {})
    
    try:
        mg_feat_relations.apply_manual_relation(active_sim_info, target_sim, settings, out, force_debug)
    except AttributeError:
        out("[CRITICAL] Das Skript 'mg_feat_relations' enthaelt nicht die benoetigte Funktion. Bitte stelle sicher, dass die Datei aktualisiert und neu kompiliert wurde.")
    except Exception as e:
        out(f"[FEHLER] apply_manual_relation: {e}")


# --- DIREKTE SHORTCUTS ---
@sims4.commands.Command('rmg.all', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_all(*args, _connection=None):
    cmd_rmg_base('all', *args, _connection=_connection)

@sims4.commands.Command('rmg.active', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_active(*args, _connection=None):
    cmd_rmg_base('active', *args, _connection=_connection)

@sims4.commands.Command('rmg.id', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_id(*args, _connection=None):
    cmd_rmg_base('id', *args, _connection=_connection)

@sims4.commands.Command('rmg.name', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_name(*args, _connection=None):
    cmd_rmg_base('name', *args, _connection=_connection)

# --- DIE UI-BRIDGE (PICKER-MENU) ---
@sims4.commands.Command('make_god_ui_trigger', 'rmg.ui_trigger', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_ui_trigger(sim_id=None, option_key='option_1', _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    mg_config.load_config()
    try: parsed_id = int(str(sim_id), 0)
    except Exception as e: return
    target_sim = mg_utils.get_sim_by_id(parsed_id)
    if not target_sim: return
    client = services.client_manager().get(_connection)
    active_household = client.active_sim.sim_info.household if (client and client.active_sim) else None
    
    if option_key == 'household':
        targets = list(target_sim.household) if target_sim.household else [target_sim]
        inc_roommates = mg_config.get("include_roommates_in_all", False)
        inc_keyholders = mg_config.get("include_keyholders_in_all", False)
        if inc_roommates or inc_keyholders:
            tracker = getattr(target_sim, 'relationship_tracker', None)
            if tracker:
                t_ids = [t.sim_id for t in targets]
                for tid in tuple(tracker.target_sim_gen()):
                    if tid not in t_ids:
                        for bit in tuple(tracker.get_all_bits(tid)):
                            b_name = getattr(bit, '__name__', '').lower()
                            if (inc_roommates and 'roommate' in b_name) or (inc_keyholders and 'key' in b_name):
                                r_sim = mg_utils.get_sim_by_id(tid)
                                if r_sim: targets.append(r_sim)
                                break
        mg_queue.start_queue(targets, 'auto', active_household, out, False, _connection)
    else:
        mg_queue.start_queue([target_sim], option_key, active_household, out, False, _connection)