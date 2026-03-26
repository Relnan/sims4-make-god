import services
import sims4.resources
import sims4.commands
import mg_config
import mg_utils
import mg_logger

def apply_stats(sim_info, set_id, out, force_debug):
    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    if not active_set: return
        
    skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
    skill_count = 0
    
    # Ermitteln, ob Player oder NPC
    active_hh_id = services.active_household_id()
    is_player = (sim_info.household_id == active_hh_id) if active_hh_id else False
    
    luck_data = active_set.get("luck", {})
    luck_val = luck_data.get("value", 0)
    luck_locked = luck_data.get("locked", False)
    allow_all_skills = active_set.get("allow_all_skills", False)
    
    do_max_skills = allow_all_skills or (active_set.get("max_player_skills", True) if is_player else active_set.get("max_npc_skills", False))
    
    # --- NEU: SKILL-ERLAUBNIS ODER FALLBACK LADEN ---
    allowed_skills = [s.lower() for s in active_set.get("allowed_skills", [])]
    
    if not allowed_skills:
        # Wenn das Set keine eigenen Skills definiert, nutze den altersabhaengigen Fallback aus der Config
        age_name = str(sim_info.age).split('.')[-1].upper()
        if age_name == 'INFANT': age_group = 'infant'
        elif age_name == 'TODDLER': age_group = 'toddler'
        elif age_name == 'CHILD': age_group = 'child'
        else: age_group = 'adult'
        
        fallback_dict = mg_config.get("fallback_skills", {})
        allowed_skills = [s.lower() for s in fallback_dict.get(age_group, [])]
    
    if skill_manager:
        for stat_type in tuple(skill_manager.types.values()):
            stat_name = getattr(stat_type, '__name__', '').lower()
            
            # --- SKILLS MAXIMIEREN ---
            if do_max_skills and hasattr(stat_type, 'is_skill') and stat_type.is_skill:
                # Pruefe, ob der Skill_Name in unserer Fallback- oder Set-Liste auftaucht
                if allow_all_skills or (allowed_skills and any(allowed in stat_name for allowed in allowed_skills)):
                    tracker = sim_info.get_tracker(stat_type)
                    if tracker:
                        try:
                            tracker.set_value(stat_type, stat_type.max_value)
                            skill_count += 1
                        except: pass
                    
            # --- LUCK (GLÜCK) ---
            if luck_data and "luck" in stat_name:
                tracker = sim_info.get_tracker(stat_type)
                if tracker:
                    try:
                        tracker.set_value(stat_type, luck_val)
                        if luck_locked:
                            stat_inst = tracker.get_statistic(stat_type)
                            if stat_inst: stat_inst.add_decay_rate_modifier(0.0)
                    except: pass
    
    # --- ZUFRIEDENHEIT ---
    points = active_set.get("satisfaction_points", 0)
    if points > 0:
        try: sims4.commands.execute(f"sims.give_satisfaction_points {points} {sim_info.sim_id}", None)
        except: pass

    # --- MOTIVE ---
    occult_type = mg_utils.get_occult_type(sim_info)
    motives_map = active_set.get("motives_to_freeze", {})
    targets = motives_map.get(occult_type, motives_map.get("human", []))
    
    frozen_count = 0
    if skill_manager and targets:
        for stat_type in tuple(skill_manager.types.values()):
            stat_name = getattr(stat_type, '__name__', '').lower()
            if stat_name in targets:
                tracker = sim_info.get_tracker(stat_type)
                if tracker:
                    stat_inst = tracker.get_statistic(stat_type)
                    if stat_inst:
                        tracker.set_value(stat_type, stat_inst.max_value)
                        try:
                            stat_inst.add_decay_rate_modifier(0.0) 
                            frozen_count += 1
                        except: pass
                        
    # --- KARRIERE ---
    do_master_careers = active_set.get("master_player_careers", True) if is_player else active_set.get("master_npc_careers", False)
    if do_master_careers and not mg_utils.is_minor(sim_info):
        if hasattr(sim_info, 'career_tracker') and sim_info.career_tracker:
            for career in tuple(sim_info.career_tracker.careers.values()):
                for _ in range(15):
                    try: career.promote()
                    except: pass
                    
        for _ in range(5): 
            try: sims4.commands.execute(f"aspirations.complete_current_milestone {sim_info.sim_id}", None)
            except: pass

    mg_logger.log(f"   [Stats] {skill_count} Skills max, {points} Zufriedenheit, {frozen_count} Motive eingefroren.", is_debug=True, out=out, force_debug=force_debug)