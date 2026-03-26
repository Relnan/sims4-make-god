import sims4.commands
import services

import mg_config
import mg_logger
import mg_utils
import mg_queue
import mg_dump

# Initiales Laden beim Import
mg_config.load_config()

@sims4.commands.Command('make_god', command_type=sims4.commands.CommandType.Live)
def cmd_make_god(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    
    # 1. WICHTIG: Cheats aktivieren, sonst funktionieren Trait/Punkt-Zuweisungen nicht!
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    mg_config.load_config()
    client = services.client_manager().get(_connection)
    if not client: return
    
    # 2. DEBUG ARGUMENT AUSWERTEN
    args_list = [str(a).lower() for a in args]
    force_debug = False
    if 'debug' in args_list:
        force_debug = True
        args_list.remove('debug')
        
    active_sim_info = client.active_sim.sim_info if client.active_sim else None
    active_household_raw = active_sim_info.household if active_sim_info else None
    
    if not active_household_raw:
        out("[FEHLER] Kein aktiver Haushalt.")
        return
        
    # Babys filtern
    active_household = []
    for sim in active_household_raw:
        try:
            if str(sim.age).split('.')[-1].upper() != 'BABY':
                active_household.append(sim)
        except:
            active_household.append(sim)
            
    targets = []
    set_id = '0'
    mode = 'all'

    if args_list:
        mode = args_list[0]
        
    if mode == 'all':
        targets = list(active_household)
        if len(args_list) > 1: set_id = str(args_list[1])
    elif mode == 'active':
        if active_sim_info: targets = [active_sim_info]
        if len(args_list) > 1: set_id = str(args_list[1])
    elif mode == 'id':
        if len(args_list) > 1:
            try:
                found_sim = mg_utils.get_sim_by_id(int(args_list[1]))
                if found_sim: targets = [found_sim]
            except: pass
        if len(args_list) > 2: set_id = str(args_list[2])
    elif mode == 'name':
        if len(args_list) > 1:
            matches = mg_utils.get_sims_by_name(args_list[1], active_household)
            if len(matches) == 1: targets = matches
        if len(args_list) > 2: set_id = str(args_list[2])
    else:
        targets = list(active_household)
        set_id = str(args_list[0])

    if not targets:
        out("[FEHLER] Keine passenden Sims gefunden.")
        return

    out(f"Sende {len(targets)} Sim(s) an die Queue fuer Set '{set_id}'...")
    
    # WICHTIG: Wir uebergeben out, force_debug UND _connection!
    mg_queue.start_queue(targets, set_id, active_household, out, force_debug, _connection)


# --- DIE UI-BRIDGE (PICKER-MENU) ---
@sims4.commands.Command('make_god_ui_trigger', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_ui_trigger(sim_id: int, option_key: str, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    mg_config.load_config()
    target_sim = mg_utils.get_sim_by_id(sim_id)
    if not target_sim: return
        
    client = services.client_manager().get(_connection)
    active_household = client.active_sim.sim_info.household if (client and client.active_sim) else None
    
    out(f"[UI] Trigger empfangen: Sim '{target_sim.first_name}', Option '{option_key}'")
    mg_queue.start_queue([target_sim], option_key, active_household, out, False, _connection)