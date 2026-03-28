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
    
    # --- SKILL-ERLAUBNIS ODER FALLBACK LADEN ---
    allowed_skills = [s.lower() for s in active_set.get("allowed_skills", [])]
    
    if not allowed_skills:
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
                # Der ultimative Schutzfilter gegen EA's "Hidden Skills"
                is_safe_skill = False
                safe_keywords = ['skill', 'major', 'minor', 'toddler', 'infant', 'child', 'retail', 'lore', 'robot']
                if any(k in stat_name for k in safe_keywords):
                    is_safe_skill = True
                    
                bad_words = ['sickness', 'illness', 'disease', 'ailment', 'curse', 'infection', 'poison']
                if any(bad in stat_name for bad in bad_words):
                    is_safe_skill = False
                
                # Ueberspringe wilde EA-Variablen, die keine echten Faheigkeiten sind
                if allow_all_skills and not is_safe_skill:
                    continue 
                
                if allow_all_skills or (allowed_skills and any(allowed in stat_name for allowed in allowed_skills)):
                    tracker = sim_info.get_tracker(stat_type)
                    if tracker:
                        try:
                            tracker.set_value(stat_type, stat_type.max_value)
                            skill_count += 1
                        except: pass
                    
            # --- LUCK (GLUECK) ---
            # FIX: Verhindert, dass wir aus Versehen "LuckSuck" (Pech/Fluch) auf 100 setzen!
            if luck_data and "luck" in stat_name:
                bad_luck_words = ['suck', 'ailment', 'curse', 'bad', 'illness']
                if not any(bad in stat_name for bad in bad_luck_words):
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
                        # FIX: Hexen-Ladung (Charge) und Werwolf-Wut (Fury) MUESSEN auf MINIMAL (0) gesetzt werden!
                        # Max Charge = Magische Ueberladung (Flueche/Tod). Max Fury = Werwolf-Rampage.
                        if "charge" in stat_name or "fury" in stat_name:
                            target_val = stat_inst.min_value
                        else:
                            target_val = stat_inst.max_value
                            
                        tracker.set_value(stat_type, target_val)
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

    # --- KRANKHEITS- & FLUCH-BUFFS ENTFERNEN (Aktive Heilung) ---
    sickness_buffs = [
        "sicknessSystem_Illness_Ailment_CoughSneeze",
        "sicknessSystem_Illness_Ailment_Dizzy",
        "sicknessSystem_Illness_Ailment_Fever",
        "sicknessSystem_Illness_Ailment_GasAndGiggles",
        "sicknessSystem_Illness_Ailment_Headache",
        "sicknessSystem_Illness_Ailment_ItchyPlumbob",
        "sicknessSystem_Illness_Ailment_Nausea",
        "sicknessSystem_Illness_Ailment_SeeingFlashes",
        "sicknessSystem_Illness_Ailment_StarryEyes",
        "sicknessSystem_Illness_Ailment_SteamyEars",
        "buff_Ailments_MainBuff_LuckSuck",
        "buff_BalanceSys_Hidden_AilmentCooldown"
    ]
    for b in sickness_buffs:
        try: sims4.commands.execute(f"sims.remove_buff {b} {sim_info.sim_id}", None)
        except: pass

    mg_logger.log(f"   [Stats] {skill_count} Skills max, {points} Zufriedenheit, {frozen_count} Motive eingefroren.", is_debug=True, out=out, force_debug=force_debug)