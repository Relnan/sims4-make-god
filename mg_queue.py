import mg_logger
import mg_utils
import traceback

import mg_feat_traits
import mg_feat_stats
import mg_feat_relations
import mg_feat_wealth

def start_queue(targets, set_id_or_auto, active_household, out, force_debug, _connection=None):
    households_funded_this_run = set()
    
    for sim_info in targets:
        try:
            raw_id = str(set_id_or_auto)
            actual_set_id = raw_id
            if raw_id.startswith('option_'):
                actual_set_id = mg_utils.get_auto_set(sim_info, active_household, raw_id)
            elif raw_id == 'auto':
                actual_set_id = mg_utils.get_auto_set(sim_info, active_household, 'option_1')
                
            mg_logger.log(f"-> Bearbeite Sim: {sim_info.first_name} {sim_info.last_name} (Set: {actual_set_id})", is_debug=True, out=out, force_debug=force_debug)
            
            # Worker Module aufrufen
            mg_feat_traits.apply_traits(sim_info, actual_set_id, out, force_debug)
            mg_feat_stats.apply_stats(sim_info, actual_set_id, out, force_debug)
            mg_feat_relations.apply_relations(sim_info, actual_set_id, out, force_debug)
            
            if sim_info.household and sim_info.household.id not in households_funded_this_run:
                success = mg_feat_wealth.apply_wealth(sim_info.household, actual_set_id, out, force_debug)
                if success:
                    households_funded_this_run.add(sim_info.household.id)
                    
        except Exception as e:
            mg_logger.log(f"[FEHLER] bei {getattr(sim_info, 'first_name', 'Unbekannt')}: {str(e)}\n{traceback.format_exc()}", is_debug=False, out=out, force_debug=force_debug)
            
    mg_logger.log("MakeGod vollstaendig ausgefuehrt!", is_debug=False, out=out, force_debug=force_debug)