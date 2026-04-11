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

def _parse_args_and_debug(args):
    args_list = [str(a).lower().strip() for a in args]
    force_debug_level = None
    
    while args_list and args_list[-1] in ['debug', 'debug_all']:
        val = args_list.pop()
        if val == 'debug' and not force_debug_level:
            force_debug_level = 'normal'
        elif val == 'debug_all':
            force_debug_level = 'all'
            
    return args_list, force_debug_level

# Initiales Laden beim Import
mg_config.load_config()

# --- HAUPT-ROUTING (Akzeptiert nun 'rmg' und 'make_god' als Befehl) ---
@sims4.commands.Command('rmg', 'make_god', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_base(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    args_list, force_debug_level = _parse_args_and_debug(args)
    force_debug = force_debug_level is not None
    
    mg_config.load_config()
    client = services.client_manager().get(_connection)
    if not client: return
    
    if not args_list:
        out("=== Relnans Make God (RMG) - Befehlsreferenz ===")
        out("Nutzung: rmg [Modus] [Set_ID|auto] [override_occult] [debug|debug_all]")
        out(" ")
        out("Verfuegbare Shortcuts:")
        out("- rmg.all [Set_ID|auto] [override]     -> Auf den ganzen Haushalt.")
        out("- rmg.active [Set_ID|auto] [override]  -> Nur auf den aktiven Sim.")
        out("- rmg.add id <ID>                      -> Verbindet Sim via ID mit aktivem Sim.")
        out("- rmg.add name <Name>                  -> Verbindet Sim via Name mit aktivem Sim.")
        out("- rmg.id <ID> [Set_ID] [override]      -> Auf Sim mit der ID.")
        out("- rmg.name <Name> [Set_ID] [override]  -> Auf gefundenen Sim.")
        out("- rmg.bat <BatchName> [Target]         -> Fuehrt Liste aus config.json aus.")
        out("- rmg.stop                             -> Bricht aktuelle Make God Queue ab.")
        out("- rmg.dump                             -> Erstellt einen Textdatei-Dump (aktiver Sim).")
        out("- rmg.dump all                         -> Erstellt einen Dump fuer den ganzen Haushalt.")
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
    override_occult = None

    if args_list:
        mode = args_list[0]
        
    def _extract_set_and_override(args_sublist):
        s_id = 'auto'
        o_occ = None
        if len(args_sublist) > 0:
            s_id = _normalize_selector(args_sublist[0])
        if len(args_sublist) > 1:
            o_occ = args_sublist[1]
        return s_id, o_occ
        
    if mode == 'all':
        for sim in active_household:
            targets_with_reason.append((sim, "Household"))
        
        inc_roommates = mg_config.get("include_roommates_in_all", False)
        inc_keyholders = mg_config.get("include_keyholders_in_all", False)
        inc_woohoo = mg_config.get("include_woohoo_partners_in_all", False)
        inc_best_friends = mg_config.get("include_best_friends_in_all", False)
        inc_significant_others = mg_config.get("include_significant_others_in_all", False)
        inc_engaged = mg_config.get("include_engaged_in_all", False)
        inc_married = mg_config.get("include_married_in_all", False)
        
        any_inc = any([inc_roommates, inc_keyholders, inc_woohoo, inc_best_friends, inc_significant_others, inc_engaged, inc_married])
        
        if any_inc and active_sim_info:
            tracker = getattr(active_sim_info, 'relationship_tracker', None)
            if tracker:
                target_ids_in_household = [t[0].sim_id for t in targets_with_reason]
                for target_id in tuple(tracker.target_sim_gen()):
                    if target_id not in target_ids_in_household:
                        has = {
                            "roommate": False,
                            "key": False,
                            "woohoo": False,
                            "best_friend": False,
                            "significant_other": False,
                            "engaged": False,
                            "married": False
                        }
                        
                        for bit in tuple(tracker.get_all_bits(target_id)):
                            b_name = getattr(bit, '__name__', '').lower()
                            if 'roommate' in b_name: has["roommate"] = True
                            if 'key' in b_name: has["key"] = True
                            if 'woohoo' in b_name: has["woohoo"] = True
                            if 'bestfriends' in b_name or '-bff' in b_name or 'best_friends' in b_name: has["best_friend"] = True
                            if 'significantother' in b_name: has["significant_other"] = True
                            if 'engaged' in b_name: has["engaged"] = True
                            if 'married' in b_name: has["married"] = True
                        
                        reason = None
                        if inc_roommates and has["roommate"]: reason = "Roommate"
                        elif inc_keyholders and has["key"]: reason = "Keyholder"
                        elif inc_woohoo and has["woohoo"]: reason = "Woohoo Partner"
                        elif inc_best_friends and has["best_friend"]: reason = "Best Friend"
                        elif inc_significant_others and has["significant_other"]: reason = "Significant Other"
                        elif inc_engaged and has["engaged"]: reason = "Engaged"
                        elif inc_married and has["married"]: reason = "Married"
                            
                        if reason:
                            target_sim = mg_utils.get_sim_by_id(target_id)
                            if target_sim:
                                targets_with_reason.append((target_sim, reason))
                                
        if len(args_list) > 1:
            set_id, override_occult = _extract_set_and_override(args_list[1:])
        
    elif mode == 'active':
        if active_sim_info: targets_with_reason.append((active_sim_info, "Aktiver Sim"))
        if len(args_list) > 1:
            set_id, override_occult = _extract_set_and_override(args_list[1:])
        
    elif mode == 'id':
        if len(args_list) > 1:
            try:
                found_sim = mg_utils.get_sim_by_id(int(args_list[1]))
                if found_sim: targets_with_reason.append((found_sim, "Manuelle ID"))
            except: pass
        if len(args_list) > 2:
            set_id, override_occult = _extract_set_and_override(args_list[2:])
        
    elif mode == 'name':
        if len(args_list) > 1:
            name_args = list(args_list[1:])
            known_occults = ['vampire', 'spellcaster', 'werewolf', 'mermaid', 'alien', 'fairy', 'ghost', 'human']
            
            if name_args and name_args[-1] in known_occults:
                override_occult = name_args.pop()
                
            if name_args:
                potential_set = name_args[-1]
                if re.match(r'^(?:option_?|opt)?(\d+)$', potential_set) or potential_set == 'auto':
                    set_id = _normalize_selector(potential_set)
                    name_args.pop()
            
            search_str = " ".join(name_args)
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
        # Fallback
        for sim in active_household:
            targets_with_reason.append((sim, "Household"))
        set_id, override_occult = _extract_set_and_override(args_list)

    targets = []
    target_reason_map = {}
    if targets_with_reason:
        if force_debug: out("--- Liste der erfassten Sims ---")
        for sim, reason in targets_with_reason:
            targets.append(sim)
            sim_id = getattr(sim, 'sim_id', None)
            if sim_id is not None and sim_id not in target_reason_map:
                target_reason_map[sim_id] = reason
            if force_debug:
                first = getattr(sim, 'first_name', '')
                last = getattr(sim, 'last_name', '')
                out(f" -> [{first} {last}, {reason}] wird verarbeitet.")

    if not targets:
        out("[FEHLER] Keine passenden Sims gefunden.")
        return

    if active_sim_info:
        for target_sim in targets:
            if target_sim.sim_id != active_sim_info.sim_id:
                try: sims4.commands.execute(f"relationship.add_bit {active_sim_info.sim_id} {target_sim.sim_id} 15803", None)
                except: pass

    out(f"Sende {len(targets)} Sim(s) an die Queue fuer Set '{set_id}'...")
    
    # Debug-Zusatzinfos (z.B. Household / Roommate / Keyholder) an die Queue weiterreichen
    mg_queue.start_queue(targets, set_id, active_household, out, force_debug_level, override_occult, _connection, target_reason_map)


# --- BATCH SYSTEM (ERWEITERT MIT ARRAY/LISTEN TARGETING) ---
@sims4.commands.Command('rmg.bat', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_bat(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    if not args:
        out("Nutzung: rmg.bat <BatchName> [id \"<ID1, ID2>\" | name \"<Name1, Name2>\" | active] [Arg0] [Arg1] ...")
        return
        
    args_list, force_debug_level = _parse_args_and_debug(args)
    if not args_list:
        out("[FEHLER] Parameter-Liste ist leer (Fehlender BatchName).")
        return
        
    force_debug = force_debug_level is not None
    
    # Sicherstellen, dass original_args nicht ueber den Index hinaus modifiziert werden
    original_args = list(args)
    if force_debug and original_args and original_args[-1].lower().strip() in ['debug', 'debug_all']:
        original_args.pop()

    batch_name_str = args_list[0].lower()
    
    mg_config.load_config()
    batches = mg_config.get("batches", {})
    
    actual_batch = None
    for k, v in batches.items():
        if k.lower() == batch_name_str:
            actual_batch = v
            break
            
    if not actual_batch:
        out(f"[FEHLER] Batch '{batch_name_str}' nicht gefunden.")
        return
        
    client = services.client_manager().get(_connection)
    active_sim_info = client.active_sim.sim_info if (client and client.active_sim) else None
    
    # 1. Ziel-Sim Array Evaluierung (Targeting)
    target_sims = []
    used_targeting_args = 0
    batch_args_lower = args_list[1:]
    
    if len(batch_args_lower) >= 1:
        mode = batch_args_lower[0]
        if mode == 'id' and len(batch_args_lower) >= 2:
            id_strings = str(original_args[2]).split(',')
            for id_str in id_strings:
                clean_id = id_str.strip()
                if not clean_id: continue
                try:
                    sim_id = int(clean_id)
                    found_sim = mg_utils.get_sim_by_id(sim_id)
                    if found_sim:
                        target_sims.append(found_sim)
                    else:
                        out(f"[FEHLER] Sim mit ID {sim_id} nicht gefunden. Uebersprungen.")
                except:
                    out(f"[FEHLER] Ungueltige ID uebergeben: '{clean_id}'")
            used_targeting_args = 2
            
        elif mode == 'name' and len(batch_args_lower) >= 2:
            name_strings = str(original_args[2]).split(',')
            for name_str in name_strings:
                search_str = name_str.strip()
                if not search_str: continue
                
                matches = mg_utils.get_sims_by_fuzzy_name(search_str)
                if not matches:
                    out(f"[FEHLER] Kein Sim gefunden fuer '{search_str}'. Uebersprungen.")
                elif len(matches) > 1:
                    out(f"[INFO] Mehrere moegliche Sims gefunden fuer '{search_str}'. Nutze exakte ID!")
                    for i, sim in enumerate(matches[:10], start=1):
                        s_id = getattr(sim, 'sim_id', 'unbekannt')
                        first = getattr(sim, 'first_name', '')
                        last = getattr(sim, 'last_name', '')
                        out(f"   {i}. {first} {last} | ID: {s_id}")
                else:
                    target_sims.append(matches[0])
            used_targeting_args = 2
            
        elif mode == 'active':
            if active_sim_info: target_sims.append(active_sim_info)
            used_targeting_args = 1

    # Fallback, falls jemand einfach 'rmg.bat deb' eintippt
    if not target_sims and (not batch_args_lower or batch_args_lower[0] not in ['id', 'name', 'active']):
        if active_sim_info:
            target_sims.append(active_sim_info)

    if not target_sims:
        out("[FEHLER] Keine gueltigen Ziel-Sims fuer diesen Batch gefunden.")
        return

    # 2. Verbleibende Argumente fuer Platzhalter {0}, {1} isolieren
    remaining_args = original_args[1 + used_targeting_args:]
        
    out(f"=== Starte Batch: {batch_name_str} fuer {len(target_sims)} Sim(s) ===")
    
    # 3. Schleife fuer jeden gefundenen Sim
    for target_sim in target_sims:
        sim_id_str = str(target_sim.sim_id)
        sim_first = getattr(target_sim, 'first_name', '')
        sim_last = getattr(target_sim, 'last_name', '')
        sim_full = f"{sim_first} {sim_last}".strip()
        
        out(f" -> Verarbeite: {sim_full}")
        
        for cmd in actual_batch:
            cmd_str = str(cmd).strip()
            if not cmd_str: continue
            
            if cmd_str.lower().startswith('rmg.bat') or cmd_str.lower().startswith('make_god.bat'):
                out(f"    [Uebersprungen] Rekursions-Schutz aktiv.")
                continue
                
            # A. Positionale Platzhalter {0}, {1} ersetzen
            for i, arg in enumerate(remaining_args):
                cmd_str = cmd_str.replace(f"{{{i}}}", str(arg))
                
            if re.search(r'\{\d+\}', cmd_str):
                out(f"    [FEHLER] Nicht genuegend Argumente uebergeben fuer '{cmd_str}'.")
                continue
                
            # B. Kontext-Platzhalter ersetzen
            cmd_str = cmd_str.replace("[sim_id]", sim_id_str)
            cmd_str = cmd_str.replace("[sim_first]", sim_first)
            cmd_str = cmd_str.replace("[sim_last]", sim_last)
            cmd_str = cmd_str.replace("[sim_name]", f'"{sim_full}"')
                
            out(f"    Ausfuehrung: [{cmd_str}]")
            try:
                sims4.commands.execute(cmd_str, _connection)
            except Exception as e:
                out(f"       [FEHLER] {e}")
                
    out(f"=== Batch '{batch_name_str}' abgeschlossen ===")


@sims4.commands.Command('rmg.add', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_add(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    args_list, force_debug_level = _parse_args_and_debug(args)
    force_debug = force_debug_level is not None
    
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
    except Exception as e:
        out(f"[FEHLER] apply_manual_relation: {e}")

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

@sims4.commands.Command('rmg.stop', 'rmg.cancel', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_stop(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    mg_queue.cancel_queue(out)


# --- DIE UI-BRIDGE (MACRO RUNNER / PIE MENU) ---
@sims4.commands.Command('make_god_ui_trigger', 'rmg.ui_trigger', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_ui_trigger(sim_id=None, action_id="01", _connection=None):
    # SICHERHEITS-FALLBACK: Wenn EA die Connection verliert, holen wir sie uns selbst.
    if _connection is None:
        client = services.client_manager().get_first_client()
        if client: _connection = client.id

    out = sims4.commands.CheatOutput(_connection)
    try: sims4.commands.cheats_enabled = True
    except: pass
    
    mg_config.load_config()
    
    if not sim_id: return

    # 1. Sicherer Cast der ID (EA uebergibt oft Hex-Strings statt int)
    try: parsed_id = int(str(sim_id), 0)
    except Exception as e:
        mg_logger.log(f"[FEHLER] UI-Trigger: Konnte Sim-ID ({sim_id}) nicht lesen. {e}", is_debug=False, out=out)
        return
        
    target_sim = mg_utils.get_sim_by_id(parsed_id)
    if not target_sim: 
        mg_logger.log(f"[FEHLER] UI-Trigger: Sim mit ID {parsed_id} existiert nicht.", is_debug=False, out=out)
        return
        
    client = services.client_manager().get(_connection)
    active_household = client.active_sim.sim_info.household if (client and client.active_sim) else None
    
    # 2. Pruefen: Ist der Ziel-Sim spielbar (im aktiven Haushalt) oder NPC?
    is_playable = False
    if active_household and getattr(target_sim, 'household_id', None) == active_household.id:
        is_playable = True

    # 3. Config-Schluessel zusammenbauen (z.B. "ui_playable_01" oder "ui_npc_01")
    raw_action = str(action_id).replace('"', '').strip()
    action_suffix = raw_action.zfill(2)
    
    config_key = f"ui_playable_{action_suffix}" if is_playable else f"ui_npc_{action_suffix}"
    
    # 4. Macros aus der JSON laden
    macros = mg_config.get("macros", {})
    macro_commands = macros.get(config_key, [])
    
    if not macro_commands:
        mg_logger.log(f"[UI] Keine Macro-Befehle fuer '{config_key}' in der Config gefunden. Abbruch.", is_debug=True, out=out)
        return
        
    log_label = "PLAYABLE" if is_playable else "NPC"
    mg_logger.log(f"[UI] Macro '{config_key}' gestartet fuer {log_label} Sim: '{target_sim.first_name}'.", is_debug=False, out=out, force_debug=True)
    
    # 5. Befehle sequenziell ausfuehren
    for raw_cmd in macro_commands:
        cmd_to_run = str(raw_cmd).replace("[sim_id]", str(parsed_id))
        
        mg_logger.log(f"   -> Execute: {cmd_to_run}", is_debug=True, out=out, force_debug=True)
        try:
            sims4.commands.execute(cmd_to_run, _connection)
        except Exception as e:
            mg_logger.log(f"      [FEHLER] bei Befehl '{cmd_to_run}': {e}", is_debug=False, out=out)