import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.endswith('.ts4script') else CURRENT_DIR
CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')

DEFAULT_CONFIG = {
    "_comment_global": "MakeGod Mod Konfiguration. Alle Schluessel, die mit '_' beginnen, werden ignoriert.",
    "_comment_setup": "Diese _Kommentare sind nur Einrichtungs-Hilfen. Du kannst sie beliebig loeschen, aendern oder erweitern.",
    "_comment_copy_sets": "Eigene Sets: vorhandenes Set kopieren, neue ID vergeben (z.B. '3', '12' oder 'boss_npc') und in auto_profiles zuweisen.",

    "_help_language": "Aktuell vorbereitet: 'de' oder 'en'. Standard ist 'de'.",
    "language": "de",

    "_help_debug_log": "true = detaillierte Logdatei schreiben, false = nur normale Infos/Fehler.",
    "debug_log": False,

    "_help_log_mode": "Erlaubt: 'overwrite' (pro Spielstart neu) oder 'append' (anhaengen).",
    "log_mode": "overwrite",
    
    "_comment_sets": "=== DEINE SIMS-EINSTELLUNGEN (SETS) ===",
    "sets": {
        "_comment_sets_intro": "Jeder Eintrag unter 'sets' ist ein Profil. Die ID links ist frei waehlbar und sollte als String gespeichert werden.",
        "_help_set_parameter": {
            "name": "Freier Anzeigename fuer UI, Debug und deine Orientierung.",
            "luck": {"value": "Typisch -100 bis 100. 100 = viel Glueck, 0 = neutral, -100 = Pech."},
            "allow_all_skills": "true/false. Wenn true, werden alle als sicher erkannten Skills maximiert; allowed_skills wird dann praktisch ignoriert.",
            "max_player_skills": "true/false. Gilt fuer Sims im aktiven Haushalt.",
            "max_npc_skills": "true/false. Gilt fuer Townies / NPCs ausserhalb des aktiven Haushalts.",
            "allowed_skills": "Liste mit Namens-Fragmenten, z.B. ['fitness', 'charisma', 'logic']. Leer [] = fallback_skills passend zum Alter verwenden.",
            "master_player_careers": "true/false. Karriere/Schule/Aspirationen fuer spielbare Sims maximieren.",
            "master_npc_careers": "true/false. Wie oben, aber fuer NPCs.",
            "harmony_friendship": "0 = nicht anfassen. Sonst typischer Bereich -100 bis 100.",
            "harmony_romance": "0 = nicht anfassen. Sonst typischer Bereich -100 bis 100.",
            "target_relationship_status": "Erlaubt: '', 'friend', 'best_friend', 'woohoo_partner', 'significant_other', 'engaged', 'married'. Romantische Statuswerte werden bei Minderjaehrigen/Familien nicht gesetzt.",
            "satisfaction_points": "Ganzzahl >= 0. 0 = keine Zusatzpunkte.",
            "add_funds": "Ganzzahl > 0. Nur positive Werte fuegen Geld hinzu.",
            "max_funds": "Obergrenze fuer das Haushaltsgeld nach add_funds.",
            "fill_motives_mode": "Erlaubt: 'all', 'config', 'none'.",
            "freeze_motives": "true/false. Stoppt den Verfall fuer die in motives_to_fill genannten Motive soweit moeglich.",
            "motives_to_fill": {
                "keys": "Empfohlene Keys: 'human', 'vampire', 'spellcaster', 'werewolf', 'mermaid'.",
                "values": "Je Key eine Liste exakter Motiv-/Commodity-Namen wie 'motive_hunger' oder 'commodity_motive_vampire_thirst'."
            },
            "exclude_all": "Traits immer entfernen. Am sichersten mit exaktem internen Namen, z.B. 'trait_Evil'.",
            "exclude_sex_male": "Wie exclude_all, aber nur fuer maennliche Sims.",
            "exclude_sex_female": "Wie exclude_all, aber nur fuer weibliche Sims.",
            "traits_all": "Traits immer hinzufuegen. Am sichersten mit exaktem internen Namen, z.B. 'trait_Savant'.",
            "traits_sex_male": "Zusatz-Traits nur fuer maennliche Sims.",
            "traits_sex_female": "Zusatz-Traits nur fuer weibliche Sims.",
            "traits_occult": {
                "keys": "Empfohlene Keys: 'human', 'vampire', 'spellcaster', 'werewolf', 'mermaid'.",
                "values": "Je Okkult-Typ eine Trait-Liste. Nicht benoetigte Keys koennen leer bleiben."
            }
        },
        "_comment_set_copy": "Zum Erstellen eigener Profile einfach einen vorhandenen Block kopieren und die Werte aendern.",
        "0": {
            "_comment_profile": "Beispiel fuer ein komplettes God-Set fuer spielbare Erwachsene.",
            "_comment_name": "Freier Anzeigename fuer dieses Set.",
            "name": "Ultimate God (Standard Profil)",
            "_comment_luck": "Typisch -100 bis 100. 100 = maximales Glueck, 0 = neutral.",
            "luck": {"value": 100},
            "_comment_skills": "allow_all_skills ueberschreibt die Filterung; bei leerer allowed_skills-Liste greifen fallback_skills.",
            "allow_all_skills": False,
            "max_player_skills": True,
            "max_npc_skills": False,
            "allowed_skills": [],
            "_comment_careers": "true = Karriere/Schule/Aspirationen forcieren.",
            "master_player_careers": True,
            "master_npc_careers": False,
            "_comment_relations": "Status erlaubt: '', friend, best_friend, woohoo_partner, significant_other, engaged, married.",
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "target_relationship_status": "woohoo_partner",
            "_comment_rewards": "Ganzzahlen. add_funds wirkt nur > 0; max_funds begrenzt das Ergebnis.",
            "satisfaction_points": 50000,
            "add_funds": 9999999,
            "max_funds": 9999999,
            "_comment_motives": "fill_motives_mode: 'all', 'config' oder 'none'. Bei 'config' werden nur die unten genannten Motive gezielt gefuellt.",
            "fill_motives_mode": "all",
            "freeze_motives": True,
            "motives_to_fill": {
                "_comment_occult_keys": "Empfohlen: human, vampire, spellcaster, werewolf, mermaid.",
                "vampire": ["commodity_motive_vampire_power", "commodity_motive_vampire_thirst", "motive_hygiene", "motive_social", "motive_fun"],
                "spellcaster": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "werewolf": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "mermaid": ["motive_hydration", "motive_hunger", "motive_energy", "motive_bladder", "motive_social", "motive_fun"],
                "human": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"]
            },
            "_comment_traits_remove": "Traits per internem Namen entfernen; leere Listen [] lassen den Bereich unveraendert.",
            "exclude_all": [
                "trait_Evil", "trait_Lazy", "trait_HotHeaded", "trait_Gloomy", "trait_Clumsy", "trait_Jealous", 
                "trait_Slob", "trait_Unflirty", "trait_Insane", "trait_Squeamish", "trait_Mean"
            ],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "_comment_traits_add": "Traits per internem Namen hinzufuegen; traits_occult wird nur beim passenden Okkult-Typ genutzt.",
            "traits_all": [
                "trait_AlwaysWelcome", "trait_Temperature_ColdAcclimation", "trait_GymRat", "trait_Temperature_HeatAcclimation",
                "trait_Observant", "trait_SpeedCleaner", "trait_Waterproof", "trait_NewInTown_InspiredExplorer",
                "trait_MorningPerson", "trait_NightOwl", "trait_SpeedReader", "trait_StormChaser",
                "trait_Mentor", "trait_FreeServices", "trait_Marketable", "trait_CreativeVisionary",
                "trait_Entrepreneurial", "trait_Frugal", "trait_Temperature_BurningMan", "trait_Temperature_IceMan",
                "trait_Independent", "trait_Shameless", "trait_SteelBladder", "trait_Beguiling",
                "trait_Antiseptic", "trait_Carefree", "trait_Connections", "trait_Fertile",
                "trait_GreatKisser", "trait_HardlyHungry", "trait_ProfessionalSlacker", "trait_Savant",
                "trait_SeldomSleepy", "trait_SuperGreenThumb", "trait_NeedsNoOne", "trait_Brave",
                "trait_ForeverFull", "trait_NeverWeary", "trait_Legendary", "trait_FreshChef", 
                "trait_OneWithNature", "trait_EpicPoet", "trait_Doctor_SicknessResistant", 
                "trait_HolidayTradition_FatherWinterBaby", "trait_CreativelyGifted", "trait_MentallyGifted", 
                "trait_PhysicallyGifted", "trait_SociallyGifted", "trait_ForeverFresh"
            ],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {
                "_comment_occult_trait_keys": "Nur passende Okkult-Typen befuellen; nicht benoetigte Keys duerfen leer bleiben.",
                "spellcaster": ["trait_Occult_WitchOccult_BloodlineAncient", "trait_Cauldron_Potion_Immortality"],
                "vampire": ["trait_TheKnack"], 
                "werewolf": ["trait_OccultWerewolf_Immortal", "trait_OccultWerewolf_Temperaments_Lunar_Resistance"], 
                "mermaid": [],
                "human": []
            }
        },
        
        "1": {
            "_comment_profile": "Beispiel fuer einen romantischen NPC-/Partner-Basisbauplan.",
            "name": "Mortal Lover (NPC Basis)",
            "luck": {"value": 0},
            "allow_all_skills": False,
            "max_player_skills": False,
            "max_npc_skills": False,
            "allowed_skills": ["fitness", "charisma", "logic"],
            "master_player_careers": False,
            "master_npc_careers": False,
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "target_relationship_status": "significant_other",
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 250000,
            "fill_motives_mode": "none",
            "freeze_motives": False,
            "motives_to_fill": {},
            "exclude_all": ["trait_Unflirty", "trait_Jealous", "trait_Evil", "trait_Mean"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": ["trait_GreatKisser", "trait_Carefree"],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {}
        },

        "2": {
            "_comment_profile": "Neutrales NPC-Profil ohne grosse Eingriffe.",
            "name": "Vanilla NPC",
            "luck": {"value": 0},
            "allow_all_skills": False,
            "max_player_skills": False,
            "max_npc_skills": False,
            "allowed_skills": [],
            "master_player_careers": False,
            "master_npc_careers": False,
            "harmony_friendship": 50,
            "harmony_romance": 0,
            "target_relationship_status": "friend",
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 50000,
            "fill_motives_mode": "none",
            "freeze_motives": False,
            "motives_to_fill": {},
            "exclude_all": [],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {}
        },

        "10": {
            "_comment_profile": "Kinderprofil fuer gespielte Haushaltskinder.",
            "name": "Blessed Child (Gespieltes Kind)",
            "luck": {"value": 100},
            "allow_all_skills": False,
            "max_player_skills": True,
            "max_npc_skills": False,
            "allowed_skills": [],
            "master_player_careers": True,
            "master_npc_careers": False,
            "harmony_friendship": 100,
            "harmony_romance": 0,
            "target_relationship_status": "best_friend",
            "satisfaction_points": 5000,
            "add_funds": 0,
            "max_funds": 9999999,
            "fill_motives_mode": "all",
            "freeze_motives": True,
            "motives_to_fill": {
                "human": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"]
            },
            "exclude_all": ["trait_Mean", "trait_Gloomy", "trait_Insane", "trait_Clumsy", "trait_Evil"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [
                "trait_Savant", "trait_Carefree", "trait_Brave", "trait_Top_Notch_Toddler",
                "trait_ScoutingAptitude", "trait_FreeServices", "trait_CreativelyGifted", 
                "trait_MentallyGifted", "trait_PhysicallyGifted", "trait_SociallyGifted"
            ],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {
                "spellcaster": ["trait_Occult_WitchOccult_BloodlineAncient"]
            }
        },
        
        "11": {
            "_comment_profile": "Normales Kinderprofil fuer NPC-Kinder.",
            "name": "NPC Child (Normal)",
            "luck": {"value": 0},
            "allow_all_skills": False,
            "max_player_skills": False,
            "max_npc_skills": False,
            "allowed_skills": [],
            "master_player_careers": False,
            "master_npc_careers": False,
            "harmony_friendship": 50,
            "harmony_romance": 0,
            "target_relationship_status": "friend",
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 250000,
            "fill_motives_mode": "none",
            "freeze_motives": False,
            "motives_to_fill": {},
            "exclude_all": ["trait_Mean", "trait_Evil"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {}
        }
    },

    "_comment_auto_profiles": "Ordnet die UI-/Cheat-Optionen den Set-IDs zu. Jeder Wert muss auf eine existierende ID aus 'sets' zeigen.",
    "auto_profiles": {
        "_comment_roles": "Rollen: adult_playable_male, adult_playable_female, adult_npc_male, adult_npc_female, child_playable, child_npc.",
        "option_1": {
            "_comment": "Standard fuer UI Option 1 sowie 'auto'.",
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "1", "adult_npc_female": "1",
            "child_playable": "10", "child_npc": "11"
        },
        "option_2": {
            "_comment": "Alternative fuer UI Option 2.",
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "2", "adult_npc_female": "2",
            "child_playable": "10", "child_npc": "11"
        },
        "option_3": {
            "_comment": "Alternative fuer UI Option 3.",
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "1", "adult_npc_female": "1",
            "child_playable": "10", "child_npc": "11"
        }
    },

    "_comment_fallback_skills": "Wird genutzt, wenn in einem Set 'allowed_skills': [] leer ist. Die Eintraege sind Namens-Fragmente, keine strengen Exakt-Treffer.",
    "fallback_skills": {
        "_comment_age_keys": "Erlaubte Alters-Keys: adult, child, toddler, infant.",
        "adult": [
            "adultmajor", "adultminor", "skill_fitness", "skill_archery", "skill_crossstitch", 
            "skill_dogtraining", "skill_retail", "skill_hidden_skating", "skill_hidden_vampirelore", 
            "woohoo_skill", "wickedwhims_skill", "skill_nls", "humanoidrobot", 
            "skill_child", "skill_toddler", "infant"
        ],
        "child": ["skill_child", "skill_toddler", "infant"],
        "toddler": ["skill_toddler", "infant"],
        "infant": ["infant"]
    }
}

ACTIVE_CONFIG = {}

def _strip_comments(data):
    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            if str(k).startswith('_'): continue
            cleaned[k] = _strip_comments(v)
        return cleaned
    elif isinstance(data, list):
        return [_strip_comments(item) for item in data]
    else:
        return data

def load_config():
    global ACTIVE_CONFIG
    raw_data = DEFAULT_CONFIG.copy()
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
        except Exception as e: pass 
    else:
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4)
        except: pass
            
    ACTIVE_CONFIG = _strip_comments(raw_data)

def get(key, default=None):
    return ACTIVE_CONFIG.get(key, default)