import os
from datetime import datetime
import sims4.commands
import sims4.resources
import services
import mg_config
import mg_utils
import mg_logger

def _get_dump_filepath(sim_info, prefix):
    """Erstellt einen sauberen Dateinamen fuer den Dump."""
    gender_str = str(sim_info.gender).split('.')[-1].lower()
    occult_str = mg_utils.get_occult_type(sim_info)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"{prefix}_{gender_str}_{occult_str}_{sim_info.first_name}_{sim_info.last_name}_{timestamp}.txt"
    return os.path.join(mg_config.MOD_FOLDER, filename)

def execute_dump(sim_info, out):
    """Liest alle Traits, Commodities und Skills aus und speichert sie."""
    if not sim_info: return
    
    mg_logger.log(f"Starte Dump fuer {sim_info.first_name} {sim_info.last_name}...", is_debug=False, out=out)
    
    # 1. Stats & Commodities Dump
    try:
        stats_path = _get_dump_filepath(sim_info, "god_dump_stats")
        with open(stats_path, 'w', encoding='utf-8') as f:
            f.write(f"=== STATISTIC & COMMODITY DUMP FUER {sim_info.first_name} {sim_info.last_name} ===\n")
            f.write("-" * 60 + "\n\n")
            stats_list = []
            
            if hasattr(sim_info, 'commodity_tracker') and sim_info.commodity_tracker:
                for stat in sim_info.commodity_tracker:
                    try:
                        t = getattr(stat, 'stat_type', type(stat))
                        val = stat.get_value()
                        stats_list.append(f"[COMMODITY] {getattr(t, '__name__', str(t))} : {val}")
                    except: pass
                    
            if hasattr(sim_info, 'statistic_tracker') and sim_info.statistic_tracker:
                for stat in sim_info.statistic_tracker:
                    try:
                        t = getattr(stat, 'stat_type', type(stat))
                        val = stat.get_value()
                        stats_list.append(f"[STATISTIC] {getattr(t, '__name__', str(t))} : {val}")
                    except: pass
                    
            stats_list.sort()
            for line in stats_list: f.write(line + "\n")
        mg_logger.log(f"Stats-Dump gespeichert: {stats_path}", is_debug=True)
    except Exception as e:
        mg_logger.log(f"[FEHLER] Stats-Dump fehlgeschlagen: {e}", is_debug=False, out=out)

    # 2. Traits Dump
    try:
        traits_path = _get_dump_filepath(sim_info, "god_dump_traits")
        with open(traits_path, 'w', encoding='utf-8') as f:
            f.write(f"=== TRAITS DUMP FUER {sim_info.first_name} {sim_info.last_name} ===\n")
            f.write("-" * 60 + "\n\n")
            
            if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker:
                t_list = []
                for t in sim_info.trait_tracker.equipped_traits:
                    t_type = str(getattr(t, 'trait_type', 'UNKNOWN')).split('.')[-1]
                    t_name = getattr(t, '__name__', str(t))
                    t_list.append(f"[{t_type}] {t_name}")
                t_list.sort()
                for line in t_list: f.write(line + "\n")
        mg_logger.log(f"Traits-Dump gespeichert: {traits_path}", is_debug=True)
    except Exception as e:
        mg_logger.log(f"[FEHLER] Traits-Dump fehlgeschlagen: {e}", is_debug=False, out=out)

    # 3. NEU: Skills Dump (Gibt ALLE verfuegbaren Skills der Engine aus)
    try:
        skills_path = _get_dump_filepath(sim_info, "god_dump_skills")
        with open(skills_path, 'w', encoding='utf-8') as f:
            f.write(f"=== ALLE SKILLS DER ENGINE ===\n")
            f.write(f"Werte in Klammern = Aktuelles Level von {sim_info.first_name}\n")
            f.write("-" * 60 + "\n\n")
            
            skill_manager = services.get_instance_manager(sims4.resources.Types.STATISTIC)
            if skill_manager:
                s_list = []
                for stat_type in tuple(skill_manager.types.values()):
                    if hasattr(stat_type, 'is_skill') and stat_type.is_skill:
                        s_name = getattr(stat_type, '__name__', str(stat_type))
                        
                        current_val = 0
                        tracker = sim_info.get_tracker(stat_type)
                        if tracker:
                            stat_inst = tracker.get_statistic(stat_type)
                            if stat_inst:
                                try:
                                    current_val = int(stat_inst.get_value())
                                except:
                                    pass
                                
                        s_list.append(f"[Level {current_val:02d}] {s_name}")
                
                s_list.sort()
                for line in s_list: f.write(line + "\n")
        mg_logger.log(f"Skills-Dump gespeichert: {skills_path}", is_debug=True)
    except Exception as e:
        mg_logger.log(f"[FEHLER] Skills-Dump fehlgeschlagen: {e}", is_debug=False, out=out)

@sims4.commands.Command('make_god_dump', command_type=sims4.commands.CommandType.Live)
def cmd_make_god_dump(*args, _connection=None):
    """
    Erstellt Dumps fuer Sims.
    Nutzung: make_god_dump [active | all | id <SimID>]
    """
    out = sims4.commands.CheatOutput(_connection)
    client = services.client_manager().get(_connection)
    if not client: return
    
    targets = []
    active_sim = client.active_sim.sim_info if client.active_sim else None
    
    if not args or str(args[0]).lower() == 'active':
        if active_sim: targets.append(active_sim)
    elif str(args[0]).lower() == 'all':
        if active_sim and active_sim.household:
            targets = list(active_sim.household)
    elif str(args[0]).lower() == 'id' and len(args) > 1:
        try:
            sim_id = int(args[1])
            found_sim = mg_utils.get_sim_by_id(sim_id)
            if found_sim: targets.append(found_sim)
        except: pass
        
    if not targets:
        out("[FEHLER] Kein Ziel fuer den Dump gefunden.")
        return
        
    for sim in targets:
        execute_dump(sim, out)
        
    out(f"Dump fuer {len(targets)} Sim(s) abgeschlossen. Siehe Mod-Ordner.")