import services
import sims4.resources
import sims4.commands
import mg_config
import mg_utils
import mg_logger

def _run_cheat(cmd, sim_info):
    """Hilfsfunktion zum Ausfuehren von Cheats auf einen spezifischen Sim"""
    try:
        sims4.commands.execute(f"{cmd} {sim_info.sim_id}", None)
    except: pass

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
                is_safe_skill = False
                safe_keywords = ['skill', 'major', 'minor', 'toddler', 'infant', 'child', 'retail', 'lore', 'robot']
                if any(k in stat_name for k in safe_keywords):
                    is_safe_skill = True
                    
                bad_words = ['sickness', 'illness', 'disease', 'ailment', 'curse', 'infection', 'poison']
                if any(bad in stat_name for bad in bad_words):
                    is_safe_skill = False
                
                if allow_all_skills and not is_safe_skill:
                    continue 
                
                if allow_all_skills or (allowed_skills and any(allowed in stat_name for allowed in allowed_skills)):
                    tracker = sim_info.get_tracker(stat_type)
                    if tracker:
                        try:
                            tracker.set_value(stat_type, stat_type.max_value)
                            skill_count += 1
                        except: pass
                        
    # --- OCCULT RÄNGE MAXIMIEREN ---
    if do_max_skills:
        occult_ranks = [
            ("rankedStatistic_WitchOccult_WitchXP", 2850),
            ("rankedStatistic_Werewolf_Progression", 3000),
            ("rankedStatistic_FairyOccult_FairyXP", 4658)
        ]
        for stat, val in occult_ranks:
            _run_cheat(f"stats.set_stat {stat} {val}", sim_info)
                    
    # --- LUCK (GLÜCK) ÜBER CHEAT-SYSTEM ---
    if luck_data:
        _run_cheat(f"stats.set_stat statistic_LuckSys_Luck {luck_val}", sim_info)
    
    # --- ZUFRIEDENHEIT ---
    points = active_set.get("satisfaction_points", 0)
    if points > 0:
        _run_cheat(f"sims.give_satisfaction_points {points}", sim_info)

    # --- MOTIVE / BEDÜRFNISSE FÜLLEN & EINFRIEREN ---
    fill_mode = active_set.get("fill_motives_mode", "all")
    freeze_motives = active_set.get("freeze_motives", False)
    
    if fill_mode != "none":
        if fill_mode == "all":
            # EA Command um ALLES auf einmal zu füllen
            _run_cheat("sims.fill_all_commodities", sim_info)
            
        occult_type = mg_utils.get_occult_type(sim_info)
        motives_map = active_set.get("motives_to_fill", {})
        targets = motives_map.get(occult_type, motives_map.get("human", []))
        
        # Gezieltes füllen (wenn config gewählt) und ggf. einfrieren
        if targets:
            for m in targets:
                if fill_mode == "config":
                    _run_cheat(f"fillmotive {m}", sim_info)
                
                # Der native Python "Freeze" Lock (hilft besonders bei Okkulten)
                if freeze_motives and skill_manager:
                    for stat_type in tuple(skill_manager.types.values()):
                        stat_name = getattr(stat_type, '__name__', '').lower()
                        if stat_name == m.lower():
                            tracker = sim_info.get_tracker(stat_type)
                            if tracker:
                                stat_inst = tracker.get_statistic(stat_type)
                                if stat_inst:
                                    # Verhindert, dass wir aus Versehen Flüche/Wut einfrieren (diese müssen entleert werden)
                                    if "charge" in stat_name or "fury" in stat_name:
                                        tracker.set_value(stat_type, stat_inst.min_value)
                                    try: stat_inst.add_decay_rate_modifier(0.0)
                                    except: pass

                        
    # --- KARRIERE & SCHULE ---
    do_master_careers = active_set.get("master_player_careers", True) if is_player else active_set.get("master_npc_careers", False)
    if do_master_careers:
        if mg_utils.is_minor(sim_info):
            # Schule für Kinder und Teenager
            age_name = str(sim_info.age).split('.')[-1].upper()
            if age_name == 'CHILD':
                for _ in range(4): _run_cheat("careers.promote gradeschool", sim_info)
            elif age_name == 'TEEN':
                for _ in range(4): _run_cheat("careers.promote highschool", sim_info)
        else:
            # Normale Karrieren für Erwachsene
            if hasattr(sim_info, 'career_tracker') and sim_info.career_tracker:
                for career in tuple(sim_info.career_tracker.careers.values()):
                    for _ in range(15):
                        try: career.promote()
                        except: pass
                        
        # Meilensteine abschließen
        for _ in range(5): 
            _run_cheat("aspirations.complete_current_milestone", sim_info)

    # --- KRANKHEITS- & FLUCH-BUFFS ENTFERNEN ---
    sickness_buffs = [
        "sicknessSystem_Illness_Ailment_CoughSneeze", "sicknessSystem_Illness_Ailment_Dizzy",
        "sicknessSystem_Illness_Ailment_Fever", "sicknessSystem_Illness_Ailment_GasAndGiggles",
        "sicknessSystem_Illness_Ailment_Headache", "sicknessSystem_Illness_Ailment_ItchyPlumbob",
        "sicknessSystem_Illness_Ailment_Nausea", "sicknessSystem_Illness_Ailment_SeeingFlashes",
        "sicknessSystem_Illness_Ailment_StarryEyes", "sicknessSystem_Illness_Ailment_SteamyEars",
        "buff_Ailments_MainBuff_LuckSuck", "buff_BalanceSys_Hidden_AilmentCooldown"
    ]
    for b in sickness_buffs:
        _run_cheat(f"sims.remove_buff {b}", sim_info)

    mg_logger.log(f"   [Stats] {skill_count} Skills max. Motive-Mode: {fill_mode} (Freeze: {freeze_motives}).", is_debug=True, out=out, force_debug=force_debug)