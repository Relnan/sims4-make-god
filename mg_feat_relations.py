import services
import sims4.resources
import mg_config
import mg_utils
import mg_logger

STATUS_HIERARCHY = {
    'married': {'level': 6, 'bit_id': 15803},
    'engaged': {'level': 5, 'bit_id': 15794},
    'significant_other': {'level': 4, 'bit_id': 15822},
    'woohoo_partner': {'level': 3, 'bit_id': 250375},
    'best_friend': {'level': 2, 'bit_id': 15792},
    'friend': {'level': 1, 'bit_id': 15797}
}

def _get_highest_current_status_level(tracker, target_sim_id):
    current_bits = tracker.get_all_bits(target_sim_id)
    highest_level = 0
    for bit in current_bits:
        bit_id = getattr(bit, 'guid64', 0)
        for status_name, data in STATUS_HIERARCHY.items():
            if data['bit_id'] == bit_id and data['level'] > highest_level:
                highest_level = data['level']
    return highest_level

def apply_relations(sim_info, set_id, out, force_debug):
    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    f_val = active_set.get("harmony_friendship", 0)
    r_val = active_set.get("harmony_romance", 0)
    target_status = active_set.get("target_relationship_status", "").lower()
    
    if f_val == 0 and r_val == 0 and not target_status: return

    stat_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
    bit_manager = services.get_instance_manager(sims4.resources.Types.RELATIONSHIP_BIT)
    if not stat_manager or not bit_manager: return
    
    f_track = stat_manager.get(16650)
    r_track = stat_manager.get(16651)
    
    count = 0
    is_source_minor = mg_utils.is_minor(sim_info)

    for member in tuple(sim_info.household):
        if member.sim_id == sim_info.sim_id: continue
            
        is_target_minor = mg_utils.is_minor(member)
        tracker = sim_info.relationship_tracker
        
        try:
            is_family = False
            bits = tracker.get_all_bits(member.sim_id)
            for bit in bits:
                bit_name = getattr(bit, '__name__', '').lower()
                if 'family' in bit_name or 'parent' in bit_name or 'sibling' in bit_name or 'child' in bit_name:
                    is_family = True
                    break

            if target_status in STATUS_HIERARCHY:
                target_data = STATUS_HIERARCHY[target_status]
                current_level = _get_highest_current_status_level(tracker, member.sim_id)
                
                if current_level < target_data['level']:
                    if target_data['level'] >= 3 and (is_source_minor or is_target_minor): pass
                    elif target_data['level'] >= 3 and is_family: pass
                    else:
                        try:
                            bit_instance = bit_manager.get(target_data['bit_id'])
                            if bit_instance: tracker.add_relationship_bit(member.sim_id, bit_instance)
                        except: pass

            if f_track and f_val != 0:
                current_f = tracker.get_relationship_score(member.sim_id, f_track)
                if f_val < 0 or f_val > current_f:
                    tracker.set_relationship_score(member.sim_id, f_val, f_track)
                    count += 1
            
            if r_track and r_val != 0:
                if not (is_source_minor or is_target_minor):
                    current_r = tracker.get_relationship_score(member.sim_id, r_track)
                    if r_val < 0 or r_val > current_r:
                        try: tracker.set_relationship_score(member.sim_id, r_val, r_track)
                        except: pass
                    
        except: pass

    mg_logger.log(f"   [Beziehungen] Angepasst mit {count} Haushaltsmitgliedern.", is_debug=True, out=out, force_debug=force_debug)