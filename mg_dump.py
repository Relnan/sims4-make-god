# mg_dump.py
import os
import re
from datetime import datetime
import sims4.commands
import sims4.resources
import services
import mg_config
import mg_utils
import mg_logger

def _sanitize_filename_part(value):
    cleaned = re.sub(r'[<>:"/\\|?*]+', '_', str(value or '').strip())
    return cleaned or 'unknown'

def _get_dump_filepath(targets, prefix="rmg_dump"):
    """Generiert einen sicheren Dateinamen. Bei mehreren Zielen wird es ein Household-Dump."""
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    os.makedirs(mg_config.MOD_FOLDER, exist_ok=True)
    
    if len(targets) > 1:
        return os.path.join(mg_config.MOD_FOLDER, f"{prefix}_Household_{timestamp}.md")
    elif len(targets) == 1:
        sim = targets[0]
        gender_str = _sanitize_filename_part(str(getattr(sim, 'gender', 'UNKNOWN')).split('.')[-1].lower())
        try:
            occult_types = mg_utils.get_occult_types(sim)
            occult_str = _sanitize_filename_part("_".join(occult_types))
        except:
            occult_str = "unknown"
        first_name = _sanitize_filename_part(getattr(sim, 'first_name', 'Unbekannt'))
        last_name = _sanitize_filename_part(getattr(sim, 'last_name', ''))
        return os.path.join(mg_config.MOD_FOLDER, f"{prefix}_{gender_str}_{occult_str}_{first_name}_{last_name}_{timestamp}.md")
    else:
        return os.path.join(mg_config.MOD_FOLDER, f"{prefix}_Empty_{timestamp}.md")

def _get_sim_data_md(sim_info):
    """Sammelt alle Daten eines einzelnen Sims fehlerresistent und formatiert sie als Markdown-String."""
    md_lines = []
    
    try:
        raw_blacklist = mg_config.get("dump_blacklist_keywords", [])
        if not raw_blacklist: raw_blacklist = []
        dump_blacklist = [str(b).lower() for b in raw_blacklist]
        
        first_name = getattr(sim_info, 'first_name', 'Unbekannt')
        last_name = getattr(sim_info, 'last_name', '')
        
        # --- HEADER ---
        md_lines.append(f"# Sim: {first_name} {last_name}")
        
        try:
            age_str = str(getattr(sim_info, 'age', 'UNKNOWN')).split('.')[-1]
            gender_str = str(getattr(sim_info, 'gender', 'UNKNOWN')).split('.')[-1]
            occult_types = mg_utils.get_occult_types(sim_info)
            occult_str = ", ".join(occult_types)
            sim_id = getattr(sim_info, 'sim_id', 'UNKNOWN')
            md_lines.append(f"**ID:** `{sim_id}` | **Alter:** {age_str} | **Geschlecht:** {gender_str} | **Okkult:** {occult_str}")
        except Exception as header_e:
            md_lines.append(f"**ID:** `{getattr(sim_info, 'sim_id', 'UNKNOWN')}` (Fehler beim Auslesen weiterer Basisdaten: {header_e})")
        
        md_lines.append("\n---")
        
        # --- TRAITS ---
        md_lines.append("\n## 🧬 Traits (Merkmale)")
        if hasattr(sim_info, 'trait_tracker') and sim_info.trait_tracker:
            t_list = []
            for t in sim_info.trait_tracker.equipped_traits:
                t_type = str(getattr(t, 'trait_type', 'UNKNOWN')).split('.')[-1]
                t_name = getattr(t, '__name__', str(t))
                t_list.append(f"- `[{t_type}]` {t_name}")
            t_list.sort()
            if t_list: md_lines.extend(t_list)
            else: md_lines.append("- *Keine Traits gefunden.*")
        else:
            md_lines.append("- *Trait-Tracker nicht verfügbar.*")

        # --- PERKS & BUCKS ---
        md_lines.append("\n## 🌟 Perks & Bucks (Okkult & Ruhm)")
        bucks_tracker = getattr(sim_info, 'bucks_tracker', None)
        if not bucks_tracker and hasattr(sim_info, 'get_bucks_tracker'):
            try: bucks_tracker = sim_info.get_bucks_tracker()
            except: pass

        if bucks_tracker:
            perks_list = []
            perk_manager = services.get_instance_manager(sims4.resources.Types.BUCKS_PERK) if hasattr(sims4.resources.Types, 'BUCKS_PERK') else None
            
            if perk_manager:
                for perk_inst in perk_manager.types.values():
                    try:
                        if bucks_tracker.is_perk_unlocked(perk_inst):
                            p_name = getattr(perk_inst, '__name__', str(perk_inst))
                            perks_list.append(f"- `[PERK]` {p_name}")
                    except: pass
                        
            perks_list.sort()
            if perks_list: md_lines.extend(perks_list)
            else: md_lines.append("- *Keine aktiven Perks gefunden.*")
        else:
            md_lines.append("- *Bucks-Tracker nicht verfügbar.*")

        # --- SPELLS & UNLOCKS ---
        md_lines.append("\n## 🔮 Zaubersprüche & Unlocks")
        spell_list = []
        
        potential_trackers = []
        for attr_name in dir(sim_info):
            if 'tracker' in attr_name.lower() or 'magic' in attr_name.lower():
                t_obj = getattr(sim_info, attr_name, None)
                if t_obj: potential_trackers.append(t_obj)
        
        if hasattr(sim_info, 'get_unlock_tracker'):
            try: potential_trackers.append(sim_info.get_unlock_tracker())
            except: pass

        if hasattr(sims4.resources.Types, 'SNIPPET'):
            snippet_manager = services.get_instance_manager(sims4.resources.Types.SNIPPET)
            if snippet_manager:
                for inst in snippet_manager.types.values():
                    u_name = getattr(inst, '__name__', '')
                    if 'spell' in u_name.lower() or 'magic' in u_name.lower():
                        for tracker in potential_trackers:
                            try:
                                if (hasattr(tracker, 'is_unlocked') and tracker.is_unlocked(inst)) or \
                                   (hasattr(tracker, 'has_unlock') and tracker.has_unlock(inst)) or \
                                   (hasattr(tracker, 'has_spell') and tracker.has_spell(inst)):
                                    spell_list.append(f"- `[SPELL]` {u_name}")
                                    break
                            except: pass
                            
        if hasattr(sims4.resources.Types, 'RECIPE'):
            recipe_manager = services.get_instance_manager(sims4.resources.Types.RECIPE)
            if recipe_manager:
                for inst in recipe_manager.types.values():
                    u_name = getattr(inst, '__name__', '')
                    if 'potion' in u_name.lower() or 'recipe_magic' in u_name.lower():
                        for tracker in potential_trackers:
                            try:
                                if (hasattr(tracker, 'is_unlocked') and tracker.is_unlocked(inst)) or \
                                   (hasattr(tracker, 'has_unlock') and tracker.has_unlock(inst)):
                                    spell_list.append(f"- `[POTION]` {u_name}")
                                    break
                            except: pass
                            
        spell_list = list(set(spell_list))
        spell_list.sort()
        
        if spell_list: md_lines.extend(spell_list)
        else: md_lines.append("- *Keine relevanten Zauber/Tränke gefunden.*")

        # --- SKILLS ---
        md_lines.append("\n## 📚 Skills (Fähigkeiten)")
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
                            try: current_val = int(stat_inst.get_value())
                            except: pass
                    
                    if current_val > 0:
                        s_list.append(f"- **[Level {current_val:02d}]** {s_name}")
            s_list.sort()
            if s_list: md_lines.extend(s_list)
            else: md_lines.append("- *Keine aktiven Skills gefunden.*")
        else:
            md_lines.append("- *Skill-Manager nicht verfügbar.*")

        # --- RELATIONSHIPS ---
        md_lines.append("\n## 💖 Beziehungen (Relationships)")
        tracker = getattr(sim_info, 'relationship_tracker', None)
        if tracker and skill_manager:
            f_track = skill_manager.get(16650)
            r_track = skill_manager.get(16651)
            r_list = []
            
            for target_id in tuple(tracker.target_sim_gen()):
                target_sim = mg_utils.get_sim_by_id(target_id)
                t_name = f"{getattr(target_sim, 'first_name', '')} {getattr(target_sim, 'last_name', '')}".strip() if target_sim else "Unbekannter Sim"

                bits = tuple(tracker.get_all_bits(target_id))
                bit_names = [getattr(b, '__name__', str(b)) for b in bits]
                
                f_score = tracker.get_relationship_score(target_id, f_track) if f_track else 0
                r_score = tracker.get_relationship_score(target_id, r_track) if r_track else 0
                
                r_list.append(f"- **{t_name}** (ID: `{target_id}`)")
                if bit_names:
                    r_list.append(f"  - *Bits:* `{'`, `'.join(bit_names)}`")
                r_list.append(f"  - *Werte:* Freundschaft: {f_score:.0f} | Romantik: {r_score:.0f}")
                
            if r_list: md_lines.extend(r_list)
            else: md_lines.append("- *Keine Beziehungen gefunden.*")
        else:
             md_lines.append("- *Relationship-Tracker nicht verfügbar.*")

        # --- STATS & COMMODITIES ---
        md_lines.append("\n## 📊 Statistiken & Commodities")
        stats_list = []
        if hasattr(sim_info, 'commodity_tracker') and sim_info.commodity_tracker:
            for stat in sim_info.commodity_tracker:
                try:
                    t = getattr(stat, 'stat_type', type(stat))
                    s_name = getattr(t, '__name__', str(t))
                    if not any(b in s_name.lower() for b in dump_blacklist):
                        val = stat.get_value()
                        stats_list.append(f"- `[COMMODITY]` {s_name} : **{val:.2f}**")
                except: pass
                
        if hasattr(sim_info, 'statistic_tracker') and sim_info.statistic_tracker:
            for stat in sim_info.statistic_tracker:
                try:
                    t = getattr(stat, 'stat_type', type(stat))
                    s_name = getattr(t, '__name__', str(t))
                    if not any(b in s_name.lower() for b in dump_blacklist):
                        val = stat.get_value()
                        stats_list.append(f"- `[STATISTIC]` {s_name} : **{val:.2f}**")
                except: pass
                
        stats_list.sort()
        if stats_list: md_lines.extend(stats_list)
        else: md_lines.append("- *Keine Stats gefunden.*")

    except Exception as e:
        md_lines.append(f"\n**[KRITISCHER FEHLER BEIM AUSLESEN DIESES SIMS]:** {e}\n")

    md_lines.append("\n<br>\n")
    return "\n".join(md_lines)

def execute_dump_to_file(targets, out):
    """Nimmt eine Liste von Sims, holt deren MD-Daten und schreibt sie in eine Datei."""
    if not targets: return
    
    try:
        log_msg = f"Starte Dump fuer {len(targets)} Sim(s)..."
        mg_logger.log(log_msg, is_debug=False, out=out)
        
        filepath = _get_dump_filepath(targets)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"\n")
            f.write(f"# 🗂️ MakeGod Dump Report\n")
            
            f.write(f"## 📋 Haushaltsübersicht ({len(targets)} Sims)\n")
            for sim in targets:
                try: 
                    occ_list = mg_utils.get_occult_types(sim)
                    occ = ", ".join(occ_list)
                except: 
                    occ = "unknown"
                first_name = getattr(sim, 'first_name', 'Unbekannt')
                last_name = getattr(sim, 'last_name', '')
                sim_id = getattr(sim, 'sim_id', 'UNKNOWN')
                f.write(f"- **{first_name} {last_name}** | ID: `{sim_id}` | Okkult: {occ}\n")
            f.write("\n---\n\n")
            
            for sim in targets:
                sim_md_data = _get_sim_data_md(sim)
                f.write(sim_md_data)
                
        mg_logger.log(f"Dump erfolgreich gespeichert: {filepath}", is_debug=True, out=out)
        out(f"Dump in Markdown-Format abgeschlossen. Siehe Mod-Ordner (.md Datei).")
    except Exception as e:
        mg_logger.log(f"[FEHLER] Dump fehlgeschlagen: {e}", is_debug=False, out=out)

def execute_reference_dump(out):
    """Liest alle verfügbaren Traits, Perks und Zauber direkt aus der Engine aus."""
    mg_logger.log("Starte Reference-Dump aller Engine-Daten...", is_debug=False, out=out)
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filepath = os.path.join(mg_config.MOD_FOLDER, f"rmg_reference_dump_{timestamp}.md")

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"\n")
            f.write("# 🗂️ MakeGod Master Reference Dump\n")
            f.write("Dieses Dokument enthält **ALLE** aktuell im Spiel geladenen Traits, Perks und Spells (inkl. Mods).\n\n")

            # TRAITS
            if hasattr(sims4.resources.Types, 'TRAIT'):
                trait_manager = services.get_instance_manager(sims4.resources.Types.TRAIT)
                if trait_manager:
                    f.write("## 🧬 Alle Merkmale (Traits)\n")
                    traits = []
                    for inst in trait_manager.types.values():
                        t_name = getattr(inst, '__name__', str(inst))
                        t_type = str(getattr(inst, 'trait_type', 'UNKNOWN')).split('.')[-1]
                        traits.append(f"- `[{t_type}]` {t_name}")
                    traits.sort()
                    f.write("\n".join(traits) + "\n\n")

            # PERKS
            if hasattr(sims4.resources.Types, 'BUCKS_PERK'):
                perk_manager = services.get_instance_manager(sims4.resources.Types.BUCKS_PERK)
                if perk_manager:
                    f.write("## 🌟 Alle Okkult- & Ruhm-Vorteile (Perks)\n")
                    perks = []
                    for inst in perk_manager.types.values():
                        p_name = getattr(inst, '__name__', str(inst))
                        perks.append(f"- `[PERK]` {p_name}")
                    perks.sort()
                    f.write("\n".join(perks) + "\n\n")

            # SPELLS
            f.write("## 🔮 Alle Zauber & Tränke (Recipes / Spells)\n")
            spells = []
            if hasattr(sims4.resources.Types, 'RECIPE'):
                recipe_manager = services.get_instance_manager(sims4.resources.Types.RECIPE)
                if recipe_manager:
                    for inst in recipe_manager.types.values():
                        name = getattr(inst, '__name__', str(inst))
                        if 'spell' in name.lower() or 'potion' in name.lower() or 'magic' in name.lower() or 'recipe' in name.lower():
                            spells.append(f"- `[RECIPE]` {name}")
            
            if hasattr(sims4.resources.Types, 'SNIPPET'):
                snippet_manager = services.get_instance_manager(sims4.resources.Types.SNIPPET)
                if snippet_manager:
                    for inst in snippet_manager.types.values():
                        name = getattr(inst, '__name__', str(inst))
                        if 'spell' in name.lower():
                            spells.append(f"- `[SNIPPET]` {name}")
                            
            spells.sort()
            f.write("\n".join(spells) + "\n\n")

        mg_logger.log(f"Reference-Dump erfolgreich: {filepath}", is_debug=True, out=out)
        out(f"Reference Dump abgeschlossen! Master-Datei liegt im Mod-Ordner.")
    except Exception as e:
        mg_logger.log(f"[FEHLER] Reference-Dump fehlgeschlagen: {e}", is_debug=False, out=out)

# --- COMMAND REGISTRIERUNG ---
@sims4.commands.Command('rmg.dump', 'make_god_dump', command_type=sims4.commands.CommandType.Live)
def cmd_rmg_dump(*args, _connection=None):
    out = sims4.commands.CheatOutput(_connection)
    client = services.client_manager().get(_connection)
    if not client: return
    
    if args and str(args[0]).lower() in ['reference', 'all_traits', 'master']:
        execute_reference_dump(out)
        return
        
    targets = []
    active_sim = getattr(client.active_sim, 'sim_info', None) if client.active_sim else None
    
    if not args or str(args[0]).lower() == 'active':
        if active_sim: targets.append(active_sim)
    elif str(args[0]).lower() == 'all':
        if active_sim and getattr(active_sim, 'household', None):
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
        
    execute_dump_to_file(targets, out)