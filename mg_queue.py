import mg_logger
import mg_utils
import traceback
import alarms
import date_and_time
import mg_dump
import mg_config
import services

import mg_feat_traits
import mg_feat_stats
import mg_feat_relations
import mg_feat_wealth

_is_queue_running = False
_current_queue_state = None

def start_queue(targets, set_id_or_auto, active_household, out, force_debug_level, override_occult=None, _connection=None, target_reason_map=None):
    global _is_queue_running, _current_queue_state
    
    # 1. Early Validation: Ist der Occult-Override gueltig? (Fail Fast)
    if override_occult is not None:
        try:
            # Wir uebergeben None als Sim, um nur den String-Override zu pruefen
            mg_utils.get_occult_types(None, override_occult)
        except ValueError as e:
            mg_logger.log(f"[FEHLER] {e}", is_debug=False, out=out)
            return

    if _is_queue_running:
        mg_logger.log("[Queue] Eine andere Warteschlange laeuft bereits. Bitte warten.", is_debug=False, out=out)
        return
        
    _is_queue_running = True
    active_debug_level = force_debug_level if force_debug_level else mg_config.get("debug_level", "normal")
    
    state = {
        'households_funded': set(),
        'before_dumps': {},
        'debug_level': active_debug_level,
        'run_timestamp': mg_dump.get_timestamp(),
        'targets_len': len(targets),
        'processed': 0,
        'alarm_handle': None
    }
    
    chunk_size = 2
    mg_logger.log(f"[Queue] Starte asynchrone Verarbeitung fuer {len(targets)} Sim(s)...", is_debug=False, out=out)
    
    # Wichtiges Feedback fuer den Nutzer, falls das Spiel pausiert ist:
    out(">>> HINWEIS: Entpausiere das Spiel (Play druecken), damit MakeGod im Hintergrund arbeiten kann! <<<")
    
    def process_chunk(handle=None):
        global _is_queue_running, _current_queue_state
        index = state['processed']
        zone = services.current_zone()
        
        if index >= len(targets):
            if state['debug_level'] == 'all':
                mg_logger.log(f"[Queue] Sims bearbeitet. Warte auf EA-Engine fuer Nachher-Dumps...", is_debug=False, out=out)
                delay_sim_mins = mg_config.get("debug_alarm_delay", 5.0)
                try:
                    state['alarm_handle'] = alarms.add_alarm(zone, date_and_time.create_time_span(minutes=delay_sim_mins), finish_debug)
                except:
                    finish_debug(None)
            else:
                _is_queue_running = False
                _current_queue_state = None
                mg_logger.log("MakeGod vollstaendig ausgefuehrt!", is_debug=False, out=out)
            return

        chunk = targets[index:index+chunk_size]
        for sim_info in chunk:
            if not sim_info or not getattr(sim_info, 'is_valid', True): 
                state['processed'] += 1
                continue
                
            try:
                raw_id = str(set_id_or_auto)
                actual_set_id = raw_id
                if raw_id.startswith('option_'):
                    actual_set_id = mg_utils.get_auto_set(sim_info, active_household, raw_id)
                elif raw_id == 'auto':
                    actual_set_id = mg_utils.get_auto_set(sim_info, active_household, 'option_1')

                force_debug = (state['debug_level'] in ['normal', 'all'])

                first_name = getattr(sim_info, 'first_name', 'Unbekannt')
                last_name = getattr(sim_info, 'last_name', '')
                reason = "Unbekannt"
                sim_id = getattr(sim_info, 'sim_id', None)
                if target_reason_map and sim_id in target_reason_map:
                    reason = target_reason_map.get(sim_id, reason)

                mg_logger.log(
                    f"[Queue] Bearbeite Sim: {first_name} {last_name} | Grund: {reason} | Set: {actual_set_id}",
                    is_debug=True,
                    out=out,
                    force_debug=force_debug
                )
                    
                if state['debug_level'] == 'all':
                    state['before_dumps'][sim_info.sim_id] = mg_dump.export_ai_debug_dump(sim_info)
                
                # Parameter override_occult und _connection werden hier durchgereicht
                mg_feat_traits.apply_traits(sim_info, actual_set_id, out, force_debug, override_occult, _connection)
                mg_feat_stats.apply_stats(sim_info, actual_set_id, out, force_debug, override_occult, _connection)
                mg_feat_relations.apply_relations(sim_info, actual_set_id, out, force_debug, group_targets=targets, _connection=_connection)
                
                if getattr(sim_info, 'household', None) and sim_info.household.id not in state['households_funded']:
                    success = mg_feat_wealth.apply_wealth(sim_info.household, actual_set_id, out, force_debug)
                    if success:
                        state['households_funded'].add(sim_info.household.id)
            except Exception as e:
                mg_logger.log(f"[FEHLER] bei {getattr(sim_info, 'first_name', 'Unbekannt')}: {str(e)}\n{traceback.format_exc()}", is_debug=False, out=out, force_debug=True)
            
            state['processed'] += 1
            
        mg_logger.log(f"[Queue] {state['processed']} von {state['targets_len']} Sims verarbeitet...", is_debug=True, out=out)
        
        try:
            # 1 Sim-Minute = ca. 1 echte Sekunde bei normalem Speed
            zone = services.current_zone()
            state['alarm_handle'] = alarms.add_alarm(zone, date_and_time.create_time_span(minutes=1), process_chunk)
        except Exception as e:
            mg_logger.log(f"[FEHLER Alarm] {e}", is_debug=False, out=out)
            process_chunk(None)

    def finish_debug(handle=None):
        global _is_queue_running, _current_queue_state
        mg_logger.log(f"[Queue] Schreibe Vorher-Nachher Dumps in Run-Log...", is_debug=False, out=out)
        for sim_info in targets:
            s_id = getattr(sim_info, 'sim_id', None)
            if not s_id or s_id not in state['before_dumps']:
                continue
                
            before_str = state['before_dumps'][s_id]
            
            # Objekt-Zerstoerung waehrend des Delays abfangen
            if not getattr(sim_info, 'is_valid', True):
                after_str = "[FEHLER] Sim-Instanz wurde waehrend der Wartezeit zerstoert oder ausgelagert."
            else:
                after_str = mg_dump.export_ai_debug_dump(sim_info)
                
            mg_dump.export_debug_comparison(sim_info, state['run_timestamp'], before_str, after_str)
            
        _is_queue_running = False
        _current_queue_state = None
        mg_logger.log("MakeGod vollstaendig ausgefuehrt! Dumps in mod_folder gespeichert.", is_debug=False, out=out)
        
    state['callback_process'] = process_chunk
    state['callback_finish'] = finish_debug
    _current_queue_state = state
    
    process_chunk(None)