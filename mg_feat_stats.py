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
    
    # Ermitteln, ob der Sim zum aktuell gespielten Haushalt gehoert (Player) oder ein NPC ist
    active_hh_id = services.active_household_id()
    is_player = (sim_info.household_id == active_hh_id) if active_hh_id else False
    
    luck_data = active_set.get("luck", {})
    luck_val = luck_data.get("value", 0)
    luck_locked = luck_data.get("locked", False)
    
    # --- SKILL KONFIGURATION AUSWERTEN ---
    do_max_skills = active_set.get("max_player_skills", True) if is_player else active_set.get("max_npc_skills", False)
    
    # Wenn die Liste leer ist, wird alles maximiert. Ansonsten nur Treffer. (Wir machen alles lowercase fuer sichere Suche)
    allowed_skills = [s.lower() for s in active_set.get("allowed_skills", [])]
    
    if skill_manager:
        for stat_type in tuple(skill_manager.types.values()):
            stat_name = getattr(stat_type, '__name__', '').lower()
            
            # SKILLS
            if do_max_skills and hasattr(stat_type, 'is_skill') and stat_type.is_skill:
                # Pruefen, ob Array leer ist ODER der Skill-Name im Array vorkommt (z.B. "fitness" in "statistic_skill_adultmajor_fitness")
                if not allowed_skills or any(allowed in stat_name for allowed in allowed_skills):
                    tracker = sim_info.get_tracker(stat_type)
                    if tracker:
                        try:
                            tracker.set_value(stat_type, stat_type.max_value)
                            skill_count += 1
                        except: pass
                    
            # LUCK (Glueck)
            if luck_data and "luck" in stat_name:
                tracker = sim_info.get_tracker(stat_type)
                if tracker:
                    try:
                        tracker.set_value(stat_type, luck_val)
                        if luck_locked:
                            stat_inst = tracker.get_statistic(stat_type)
                            if stat_inst: stat_inst.add_decay_rate_modifier(0.0)
                    except: pass
    
    points = active_set.get("satisfaction_points", 0)
    if points > 0:
        try: sims4.commands.execute(f"sims.give_satisfaction_points {points} {sim_info.sim_id}", None)
        except: pass

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
                        
    # --- KARRIERE KONFIGURATION AUSWERTEN ---
    do_master_careers = active_set.get("master_player_careers", True) if is_player else active_set.get("master_npc_careers", False)
    
    # Karrieren und Bestreben pushen (nur wenn erlaubt UND der Sim kein Kind ist)
    if do_master_careers and not mg_utils.is_minor(sim_info):
        if hasattr(sim_info, 'career_tracker') and sim_info.career_tracker:
            # career_tracker.careers.values() beinhaltet NUR die aktiven Berufe des Sims
            for career in tuple(sim_info.career_tracker.careers.values()):
                for _ in range(15):
                    try: career.promote()
                    except: pass
                    
        for _ in range(5): 
            try: sims4.commands.execute(f"aspirations.complete_current_milestone {sim_info.sim_id}", None)
            except: pass

    mg_logger.log(f"   [Stats] {skill_count} Skills max, {points} Zufriedenheit, {frozen_count} Motive eingefroren.", is_debug=True, out=out, force_debug=force_debug)