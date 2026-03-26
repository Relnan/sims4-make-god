import mg_config
import mg_logger
from protocolbuffers import Consts_pb2

def apply_wealth(household, set_id, out, force_debug):
    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    add_f = active_set.get("add_funds", 0)
    max_f = active_set.get("max_funds", 9999999)
    
    if add_f <= 0 or not household: return False
        
    try:
        current_funds = household.funds.money
        new_funds = min(current_funds + add_f, max_f)
        diff = new_funds - current_funds
        
        if diff > 0:
            first_sim = next(iter(household), None)
            if first_sim:
                household.funds.add(diff, Consts_pb2.TELEMETRY_MONEY_CHEAT, first_sim)
                mg_logger.log(f"   [Geld] {diff} Simoleons hinzugefuegt. (Neu: {new_funds})", is_debug=True, out=out, force_debug=force_debug)
                return True
    except: pass
    return False