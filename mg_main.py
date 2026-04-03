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

# --- ZENTRALER ARGUMENT-PARSER ---
def _parse_args_and_debug(args):
    """Filtert das Schlüsselwort 'debug' ausschliesslich am Ende der Eingabe heraus."""
    args_list = [str(a).lower().strip() for a in args]
    force_debug = False
    
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
    
    args_list, force_debug = _parse_args_and_debug(args)
    
    mg_config.load_config()
    client = services.client_manager().get(_connection)
    if not client: return
    
    # --- BEFEHLSREFERENZ / HILFEMENÜ ---
    if not args_list:
        out("=== Relnans Make God (RMG) - Befehlsreferenz ===")
        out("Nutzung: rmg [Modus] [Set_ID|auto|option_X] [debug]")
        out(" ")
        out("Verfuegbare Shortcuts:")
        out("- rmg.all [Set_ID|auto]   -> Auf den ganzen Haushalt.")
        out("- rmg.active [Set_ID|auto]-> Nur auf den aktiven Sim.")
        out("- rmg.add id <ID>         -> Verbindet Sim via ID mit aktivem Sim.")
        out("- rmg.add name <Name>     -> Verbindet Sim via Name mit aktivem Sim.")
        out("- rmg.id <ID> [Set_ID]    -> Auf Sim mit der ID.")
        out("- rmg.name <Name> [Set_ID]-> Auf gefundenen Sim (z.B. rmg.name yuki behr 2).")
        out("- rmg.bat <BatchName>     -> Fuehrt Liste aus config.json aus.")
        out("- rmg.dump                -> Erstellt einen Textdatei-Dump (aktiver Sim).")
        out("- rmg.dump all            -> Erstellt einen Dump fuer den ganzen Haushalt.")
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
            
    targets_with_reason = []
    set_id = 'auto'
    mode = 'all'

    if args_list:
        mode = args_list[0]
        
    if mode == 'all':
        for sim in active_household:
            targets_with_reason.append((sim, "Household"))
        
        inc_roommates = mg_config.get("include_roommates_in_all", False)
        inc_keyholders = mg_config.get("include_keyholders_in_all", False)
        
        if (inc_roommates or inc_keyholders) and active_sim_info:
            tracker = getattr(active_sim_info, 'relationship_tracker', None)
            if tracker:
                target_ids_in_household = [t[0].sim_id for t in targets_with_reason]
                for target_id in tuple(tracker.target_sim_gen()):
                    if target_id not in target_ids_in_household:
                        has_roommate = False
                        has_key = False
                        for bit in tuple(tracker.get_all_bits(target_id)):
                            b_name = getattr(bit, '__name__', '').lower()
                            if 'roommate' in b_name: has_roommate = True
                            if 'key' in b_name: has_key = True
                        
                        reason = None
                        if inc_roommates and has_roommate:
                            reason = "Roommate"
                        elif inc_keyholders and has_key:
                            reason = "Keyholder"
                            
                        if reason:
                            target_sim = mg_utils.get_sim_by_id(target_id)
                            if target_sim:
                                targets_with_reason.append((target_sim, reason))
                                
        if len(args_list) > 1: set_id = _normalize_selector(args_list[1])
        
    elif mode == 'active':
        if active_sim_info: targets_with_reason.append((active_sim_info, "Aktiver Sim"))
        if len(args_list) > 1: set_id = _normalize_selector(args_list[1])
        
    elif mode == 'id':
        if len(args_list) > 1:
            try:
                found_sim = mg_utils.get_sim_by_id(int(args_list[1]))
                if found_sim: targets_with_reason.append((found_sim, "Manuelle ID"))
            except: pass
        if len(args_list) > 2: set_id = _normalize_selector(args_list[2])
        
    elif mode == 'name':
        if len(args_list) > 1:
            # Puerft, ob das letzte Wort ein Set (z.B. "2" oder "option_2") ist
            potential_set = args_list[-1]
            if re.match(r'^(?:option_?|opt)?(\d+)$', potential_set) or potential_set == 'auto':
                set_id = _normalize_selector(potential_set)
                search_str = " ".join(args_list[1:-1]) # Alles dazwischen ist der Name
            else:
                search_str = " ".join(args_list[1:]) # Kein Set angegeben, der Rest ist Name
            
            if not search_str:
                out("[FEHLER] Kein Name angegeben.")
                return
                
            matches = mg_utils.get_sims_by_fuzzy_name(search_str, active_household)
            if len(matches) == 1:
                targets_with_reason.append((matches[0], "Namens-Suche"))
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
                
    else:
        for sim in active_household:
            targets_with_reason.append((sim, "Household"))
        set_id = _normalize_selector(args_list[0])

    # --- ZUSAMMENFASSEN UND AUSGEBEN ---
    targets = []
    if targets_with_reason:
        if force_debug: out("--- Liste der erfassten Sims ---")
        for sim, reason in targets_with_reason:
            targets.append(sim)
            if force_debug:
                first = getattr(sim, 'first_name', '')
                last = getattr(sim, 'last_name', '')
                out(f" -> [{first} {last}, {reason}] wird verarbeitet.")

    if not targets:
        out("[FEHLER] Keine passenden Sims gefunden.")
        return

# --- NEU: Alle Ziel-Sims mit dem aktiven Sim bekannt machen ---
    if active_sim_info:
        for target_sim in targets:
            if target_sim.sim_id != active_sim_info.sim_id:
                sims4.commands.execute(f"relationship.add_bit {active_sim_info.sim_id} {target_sim.sim_id} 15803", None)

    out(f"Sende {len(targets)} Sim(s) an die Queue fuer Set '{set_id}'...")
    mg_queue.start_queue(targets, set_id, active_household, out, force_debug, _connection)


# --- BATCH SYSTEM (rmg.bat) ---
@sims4.commands.Command('rmg.bat', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_bat(batch_name=None, *args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    if not batch_name:
        out("Nutzung: rmg.bat <BatchName> [Arg1] [Arg2] ...")
        return
        
    mg_config.load_config()
    batches = mg_config.get("batches", {})
    batch_name_str = str(batch_name).lower()
    
    actual_batch = None
    for k, v in batches.items():
        if k.lower() == batch_name_str:
            actual_batch = v
            break
            
    if not actual_batch:
        out(f"[FEHLER] Batch '{batch_name}' nicht in der make_god_config gefunden.")
        return
        
    out(f"=== Starte Batch: {batch_name} ({len(actual_batch)} Befehle) ===")
    for cmd in actual_batch:
        cmd_str = str(cmd).strip()
        if not cmd_str: continue
        
        # Rekursions-Schutz
        if cmd_str.lower().startswith('rmg.bat') or cmd_str.lower().startswith('make_god.bat'):
            out(f" -> [Uebersprungen] Rekursions-Schutz: Verschachtelte Batches ({cmd_str}) sind nicht erlaubt.")
            continue
            
        # Platzhalter {0}, {1} etc. durch die eingegebenen Argumente ersetzen
        for i, arg in enumerate(args):
            cmd_str = cmd_str.replace(f"{{{i}}}", str(arg))
            
        # Pruefen, ob noch unaufgeloeste Platzhalter (z.B. {1}) im String existieren
        if re.search(r'\{\d+\}', cmd_str):
            out(f" -> [FEHLER] Uebersprungen: Nicht genuegend Argumente uebergeben fuer '{cmd_str}'.")
            continue
            
        out(f" -> Ausfuehrung: [{cmd_str}]")
        try:
            sims4.commands.execute(cmd_str, _connection)
        except Exception as e:
            out(f"    [FEHLER] {e}")
            
    out(f"=== Batch '{batch_name}' abgeschlossen ===")


# --- MANUELLE VERKNÜPFUNG (rmg.add) ---
@sims4.commands.Command('rmg.add', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_add(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
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
    if force_debug:
        out("[HINWEIS] Wenn der Ziel-Sim aktuell nicht im Level geladen (hidden) ist, koennen bestimmte Beziehungs-Updates stumm fehlschlagen.")
    
    import mg_feat_relations
    settings = mg_config.get("manual_add_settings", {})
    
    try:
        mg_feat_relations.apply_manual_relation(active_sim_info, target_sim, settings, out, force_debug)
    except AttributeError:
        out("[CRITICAL] Das Skript 'mg_feat_relations' enthaelt nicht die benoetigte Funktion. Bitte stelle sicher, dass die Datei aktualisiert und neu kompiliert wurde.")
    except Exception as e:
        out(f"[FEHLER] apply_manual_relation: {e}")


# --- DIREKTE SHORTCUTS (rmg.all, rmg.active etc.) ---
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
        targets_with_reason = []
        hh_sims = list(target_sim.household) if target_sim.household else [target_sim]
        for s in hh_sims:
            targets_with_reason.append((s, "Household"))
        
        inc_roommates = mg_config.get("include_roommates_in_all", False)
        inc_keyholders = mg_config.get("include_keyholders_in_all", False)
        
        if inc_roommates or inc_keyholders:
            tracker = getattr(target_sim, 'relationship_tracker', None)
            if tracker:
                t_ids = [t[0].sim_id for t in targets_with_reason]
                for tid in tuple(tracker.target_sim_gen()):
                    if tid not in t_ids:
                        has_roommate = False
                        has_key = False
                        for bit in tuple(tracker.get_all_bits(tid)):
                            b_name = getattr(bit, '__name__', '').lower()
                            if 'roommate' in b_name: has_roommate = True
                            if 'key' in b_name: has_key = True
                        
                        reason = None
                        if inc_roommates and has_roommate: reason = "Roommate"
                        elif inc_keyholders and has_key: reason = "Keyholder"
                        
                        if reason:
                            r_sim = mg_utils.get_sim_by_id(tid)
                            if r_sim: targets_with_reason.append((r_sim, reason))

        targets = [t[0] for t in targets_with_reason]
        
        # --- NEU: Bekannt machen ---
        active_sim_info_ui = client.active_sim.sim_info if client and client.active_sim else None
        if active_sim_info_ui:
            for t_sim in targets:
                if t_sim.sim_id != active_sim_info_ui.sim_id:
                    sims4.commands.execute(f"relationship.add_bit {active_sim_info_ui.sim_id} {t_sim.sim_id} 15803", None)

        mg_queue.start_queue(targets, 'auto', active_household, out, False, _connection)
    else:
        # --- NEU: Bekannt machen ---
        active_sim_info_ui = client.active_sim.sim_info if client and client.active_sim else None
        if active_sim_info_ui and target_sim.sim_id != active_sim_info_ui.sim_id:
             sims4.commands.execute(f"relationship.add_bit {active_sim_info_ui.sim_id} {target_sim.sim_id} 15803", None)
             
        mg_queue.start_queue([target_sim], option_key, active_household, out, False, _connection)