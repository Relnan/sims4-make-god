import services
import sims4.resources
import sims4.commands
import mg_config
import mg_utils
import mg_logger

def _run_cheat(cmd, sim_info, global_cmd=False, _connection=None):
    """Hilfsfunktion zum Ausfuehren von Cheats auf einen spezifischen Sim oder global."""
    try:
        if global_cmd:
            sims4.commands.execute(cmd, None)
        else:
            sims4.commands.execute(f"{cmd} {sim_info.sim_id}", None)
    except:
        pass

def _clear_negative_buffs(sim_info):
    """Hybrides System: Loescht Buffs nach Mood oder Fallback-Namen, respektiert Excludes."""
    exclude_buffs = [str(s).lower() for s in mg_config.get("buffs_exclude_from_clear", [])]
    old_sickness_fallbacks = [
        "sicknesssystem_illness_ailment_coughsneeze", "sicknesssystem_illness_ailment_dizzy",
        "sicknesssystem_illness_ailment_fever", "sicknesssystem_illness_ailment_gasandgiggles",
        "sicknesssystem_illness_ailment_headache", "sicknesssystem_illness_ailment_itchyplumbob",
        "sicknesssystem_illness_ailment_nausea", "sicknesssystem_illness_ailment_seeingflashes",
        "sicknesssystem_illness_ailment_starryeyes", "sicknesssystem_illness_ailment_steamyears",
        "buff_ailments_mainbuff_lucksuck", "buff_balancesys_hidden_ailmentcooldown"
    ]
    
    buff_comp = getattr(sim_info, 'buff_component', None)
    if not buff_comp: return 0
    
    removed = 0
    for buff in tuple(buff_comp):
        try:
            buff_type = getattr(buff, 'buff_type', buff)
            b_name = getattr(buff_type, '__name__', '').lower()
            
            # 1. Pruefung: Steht der Buff auf der Blacklist des Nutzers/Systems?
            if any(e in b_name for e in exclude_buffs):
                continue
                
            remove_it = False
            
            # 2. Pruefung: Fallback fuer versteckte System-Krankheiten und Flueche
            if b_name in old_sickness_fallbacks or any(s in b_name for s in ['sickness', 'illness', 'disease', 'ailment', 'curse', 'infection', 'poison']):
                remove_it = True
                
            # 3. Pruefung: Dynamische Mood-Erkennung (fuer Moodlets aus allen Mods & DLCs)
            mood_type = getattr(buff_type, 'mood_type', None)
            if mood_type:
                m_name = getattr(mood_type, '__name__', '').lower()
                if any(bad in m_name for bad in ['tense', 'angry', 'sad', 'embarrassed', 'uncomfortable', 'scared', 'bored']):
                    remove_it = True
                    
            if remove_it:
                buff_comp.remove_buff_by_type(buff_type)
                removed += 1
        except: pass
        
    return removed

def apply_stats(sim_info, set_id, out, force_debug, override_occult=None, _connection=None):
    active_set = mg_config.get("sets", {}).get(str(set_id), {})
    if not active_set: return
        
    skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
    skill_count = 0
    
    # Ermitteln, ob Player oder NPC
    active_hh_id = services.active_household_id()
    is_player = (sim_info.household_id == active_hh_id) if active_hh_id else False
    
    # Zentralen Occult-Typ (Liste) fuer diesen Lauf ermitteln
    occult_types = mg_utils.get_occult_types(sim_info, override_occult)
    
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
                        
    # --- OCCULT RAENGE MAXIMIEREN ---
    if do_max_skills:
        occult_ranks = []
        if 'vampire' in occult_types:
            occult_ranks.append(("rankedStatistic_Occult_VampireXP", 32000))
        if 'spellcaster' in occult_types:
            occult_ranks.append(("rankedStatistic_WitchOccult_WitchXP", 2850))
        if 'werewolf' in occult_types:
            occult_ranks.append(("rankedStatistic_Werewolf_Progression", 3000))
        if 'fairy' in occult_types:
            occult_ranks.append(("rankedStatistic_FairyOccult_FairyXP", 4658))

        for stat, val in occult_ranks:
            _run_cheat(f"stats.set_stat {stat} {val}", sim_info, _connection=_connection)
                    
    # --- LUCK (GLUECK) UEBER CHEAT-SYSTEM ---
    if luck_data:
        _run_cheat(f"stats.set_stat statistic_LuckSys_Luck {luck_val}", sim_info, _connection=_connection)
    
    # --- ZUFRIEDENHEIT ---
    points = active_set.get("satisfaction_points", 0)
    if points > 0:
        _run_cheat(f"sims.give_satisfaction_points {points}", sim_info, _connection=_connection)

    # --- MOTIVE / BEDUERFNISSE FUELLEN & EINFRIEREN ---
    fill_mode = active_set.get("fill_motives_mode", "all")
    freeze_motives = active_set.get("freeze_motives", False)
    
    if fill_mode != "none":
        if fill_mode == "all":
            # EA Command um ALLES auf einmal zu fuellen (Globaler Cheat ohne Sim-ID)
            _run_cheat("sims.fill_all_commodities", sim_info, global_cmd=True, _connection=_connection)
            
        motives_map = active_set.get("motives_to_fill", {})
        
        # Sammle alle Motive fuer alle Okkult-Typen des Sims (Wichtig fuer Hybride)
        targets = []
        for occ in occult_types:
            if occ in motives_map:
                targets.extend(motives_map[occ])
                
        # Fallback, falls der Okkult-Typ leer in der Config ist, aber ein human Block existiert
        if not targets and "human" in motives_map:
            targets.extend(motives_map["human"])
            
        # Duplikate entfernen
        targets = list(set(targets))
        
        # Gezieltes fuellen (wenn config gewaehlt) und ggf. einfrieren
        if targets:
            for m in targets:
                if fill_mode == "config":
                    _run_cheat(f"fillmotive {m}", sim_info, _connection=_connection)
                
                # Der native Python "Freeze" Lock (hilft besonders bei Okkulten)
                if freeze_motives and skill_manager:
                    for stat_type in tuple(skill_manager.types.values()):
                        stat_name = getattr(stat_type, '__name__', '').lower()
                        if stat_name == m.lower():
                            tracker = sim_info.get_tracker(stat_type)
                            if tracker:
                                stat_inst = tracker.get_statistic(stat_type)
                                if stat_inst:
                                    # Verhindert, dass wir aus Versehen Flueche/Wut einfrieren (diese muessen entleert werden)
                                    if "charge" in stat_name or "fury" in stat_name:
                                        tracker.set_value(stat_type, stat_inst.min_value)
                                    try: stat_inst.add_decay_rate_modifier(0.0)
                                    except: pass

                        
    # --- KARRIERE & SCHULE ---
    do_master_careers = active_set.get("master_player_careers", True) if is_player else active_set.get("master_npc_careers", False)
    if do_master_careers:
        if mg_utils.is_minor(sim_info):
            # Schule fuer Kinder und Teenager
            age_name = str(sim_info.age).split('.')[-1].upper()
            if age_name == 'CHILD':
                for _ in range(4): _run_cheat("careers.promote gradeschool", sim_info, _connection=_connection)
            elif age_name == 'TEEN':
                for _ in range(4): _run_cheat("careers.promote highschool", sim_info, _connection=_connection)
        else:
            # Normale Karrieren fuer Erwachsene
            if hasattr(sim_info, 'career_tracker') and sim_info.career_tracker:
                for career in tuple(sim_info.career_tracker.careers.values()):
                    for _ in range(15):
                        try: career.promote()
                        except: pass
                        
        # Meilensteine abschliessen
        for _ in range(5): 
            _run_cheat("aspirations.complete_current_milestone", sim_info, _connection=_connection)

    # --- KRANKHEITS- & FLUCH-BUFFS ENTFERNEN (Hybrides System) ---
    removed_buffs = _clear_negative_buffs(sim_info)

    mg_logger.log(f"   [Stats] {skill_count} Skills max. Motive-Mode: {fill_mode} (Freeze: {freeze_motives}). {removed_buffs} negative Buffs entfernt.", is_debug=True, out=out, force_debug=force_debug)