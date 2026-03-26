import sims4.commands
import services
import re

import mg_config
import mg_logger
import mg_utils
import mg_queue
import mg_dump

# Erlaubt benutzerfreundliche Eingaben wie option1/option_1/opt1
# und skaliert fuer beliebige Nummern (z.B. option_12).
def _normalize_selector(value):
    raw = str(value).lower().strip()
    m = re.match(r'^(?:option_?|opt)(\d+)$', raw)
    if m:
        return f"option_{m.group(1)}"
    return raw

# Initiales Laden beim Import
mg_config.load_config()

# --- HAUPT-ROUTING (Akzeptiert nun 'rmg' und 'make_god' als Befehl) ---
@sims4.commands.Command('rmg', 'make_god', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_base(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    mg_config.load_config()
    client = services.client_manager().get(_connection)
    if not client: return
    
    args_list = [str(a).lower() for a in args]
    
    # --- BEFEHLSREFERENZ / HILFEMENÜ ---
    if not args_list:
        out("=== Relnans Make God (RMG) - Befehlsreferenz ===")
        out("Nutzung: rmg [Modus] [Set_ID|auto|option_X] [debug]")
        out(" ")
        out("Verfuegbare Shortcuts:")
        out("- rmg.all [Set_ID|auto|option_X]    -> Auf den ganzen Haushalt.")
        out("- rmg.active [Set_ID|auto|option_X] -> Nur auf den aktiven Sim.")
        out("- rmg.id <ID> [Set_ID|auto|option_X]-> Auf Sim mit der ID.")
        out("- rmg.name \"Name\" [Set|auto|option_X]-> Auf gefundenen Sim.")
        out("- rmg.dump            -> Erstellt einen Textdatei-Dump (aktiver Sim).")
        out("- rmg.dump all        -> Erstellt einen Dump fuer den ganzen Haushalt.")
        out(" ")
        out("Beispiele:")
        out("rmg.all auto       -> Smarte Zuweisung (Kinder kriegen Kinder-Set etc.)")
        out("rmg.all 1          -> Erzwingt Set 1 fuer ALLE im Haushalt.")
        out("rmg.active 0 debug -> Set 0 auf aktiven Sim mit genauen Logs.")
        out("rmg auto           -> Kurzbefehl fuer 'rmg all auto'.")
        out("==================================================")
        return
        
    force_debug = False
    if 'debug' in args_list:
        force_debug = True
        args_list.remove('debug')
        
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
            matches = mg_utils.get_sims_by_name(args_list[1], active_household)
            if len(matches) == 1:
                targets = matches
            elif len(matches) > 1:
                out(f"[FEHLER] Mehrdeutiger Name: {len(matches)} Sims gefunden fuer '{args_list[1]}'.")
                out("Trefferliste:")

                max_lines = 20
                for i, sim in enumerate(matches[:max_lines], start=1):
                    sim_id = getattr(sim, 'sim_id', 'unbekannt')
                    first = getattr(sim, 'first_name', '')
                    last = getattr(sim, 'last_name', '')
                    label = "Haushalt" if (active_household and sim in active_household) else "NPC"
                    out(f"{i}. {first} {last} | ID: {sim_id} | {label}")

                if len(matches) > max_lines:
                    out(f"... und {len(matches) - max_lines} weitere Treffer.")

                out("Bitte nutze rmg.id <SimID> oder gib einen genaueren Namen an.")
                return
        if len(args_list) > 2: set_id = _normalize_selector(args_list[2])
    else:
        # Fallback: Wenn jemand z.B. nur "rmg 0" oder "rmg auto" eintippt
        targets = list(active_household)
        set_id = _normalize_selector(args_list[0])

    if not targets:
        out("[FEHLER] Keine passenden Sims gefunden.")
        return

    out(f"Sende {len(targets)} Sim(s) an die Queue fuer Set '{set_id}'...")
    mg_queue.start_queue(targets, set_id, active_household, out, force_debug, _connection)


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
    
    # 1. Sicherer Cast der ID (EA uebergibt oft Hex-Strings statt int)
    try:
        parsed_id = int(str(sim_id), 0)
    except Exception as e:
        mg_logger.log(f"[FEHLER] UI-Trigger: Konnte Sim-ID ({sim_id}) nicht lesen. {e}", is_debug=False, out=out)
        return
        
    target_sim = mg_utils.get_sim_by_id(parsed_id)
    if not target_sim: 
        mg_logger.log(f"[FEHLER] UI-Trigger: Sim mit ID {parsed_id} existiert nicht.", is_debug=False, out=out)
        return
        
    client = services.client_manager().get(_connection)
    active_household = client.active_sim.sim_info.household if (client and client.active_sim) else None
    
    # 2. Schreiben des Klicks in die Log-Datei
    mg_logger.log(f"[UI] Menue-Button geklickt fuer Sim: '{target_sim.first_name}' (Befehl: {option_key})", is_debug=False, out=out, force_debug=True)
    
    if option_key == 'household':
        targets = list(target_sim.household) if target_sim.household else [target_sim]
        mg_queue.start_queue(targets, 'auto', active_household, out, False, _connection)
    else:
        mg_queue.start_queue([target_sim], option_key, active_household, out, False, _connection)