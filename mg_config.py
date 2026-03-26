import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.endswith('.ts4script') else CURRENT_DIR
CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')

DEFAULT_CONFIG = {
    "_comment_global": "MakeGod Mod Konfiguration. Alle Schluessel, die mit '_' beginnen, werden ignoriert.",
    
    "_help_language": "Sprache (aktuell Platzhalter fuer UI-Meldungen: 'de', 'en').",
    "language": "de",
    
    "_help_debug_log": "true: Schreibt jeden Schritt in die Log-Datei. false: Nur Fehler und Zusammenfassungen.",
    "debug_log": False,
    
    "_help_log_mode": "'append': Haengt neue Logs unten an. 'overwrite': Ueberschreibt die Log-Datei bei jedem Spielstart.",
    "log_mode": "overwrite",
    
    "_comment_sets": "=== DEINE SIMS-EINSTELLUNGEN (SETS) ===",
    "sets": {
        "_help_set_parameter": {
            "INFO": "Diese Hilfe wird vom Spiel ignoriert. Hier sind die Erklaerungen aller Set-Werte:",
            "luck": "value: 0-100 (Vanilla Max 100). locked: true/false (friert den Wert dauerhaft ein).",
            "allow_all_skills": "true/false. Wenn true, wird JEDE verfuegbare Faehigkeit auf das Max gesetzt.",
            "harmony_friendship": "0 bis 100 (Vanilla Max 100). Legt Freundschaft fuer alle Haushaltsmitglieder fest.",
            "harmony_romance": "0 bis 100. Legt Romantik fest.",
            "target_relationship_status": "Zulaessig: 'married', 'engaged', 'significant_other', 'woohoo_partner', 'best_friend', 'friend'.",
            "motives_to_freeze": "Welche Beduerfnisse maximiert und eingefroren werden sollen (Trennt nach Okkult-Typ).",
            "exclude_all": "ENTHAELT-Filter (Substring). Loescht z.B. bei 'evil' alles, was böse ist.",
            "traits_all": "MUSS der exakte EA/Mod Name sein."
        },
        
        "0": {
            "name": "Ultimate God (Standard Profil)",
            "luck": {"value": 100, "locked": True},
            "allow_all_skills": False,
            "max_player_skills": True,
            "max_npc_skills": False,
            "allowed_skills": [],
            "master_player_careers": True,
            "master_npc_careers": False,
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "target_relationship_status": "woohoo_partner",
            "satisfaction_points": 50000,
            "add_funds": 9999999,
            "max_funds": 9999999,
            "motives_to_freeze": {
                "vampire": ["commodity_motive_vampire_power", "commodity_motive_vampire_thirst", "motive_hygiene", "motive_social", "motive_fun"],
                "spellcaster": ["commodity_motive_witchoccult_charge", "motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "werewolf": ["commodity_motive_werewolf_fury", "motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "mermaid": ["motive_hydration", "motive_hunger", "motive_energy", "motive_bladder", "motive_social", "motive_fun"],
                "ghost": ["commodity_ghostpowers_stamina", "motive_social", "motive_fun"],
                "alien": ["motive_brainpower", "motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "human": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"]
            },
            "exclude_all": [
                "evil", "lazy", "hotheaded", "gloomy", "clumsy", "jealous", 
                "slob", "unflirty", "fear_death", "erratic", "squeamish", 
                "highmaintenance", "disgustedbyfood"
            ],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [
                "trait_Brave", "trait_Carefree", "trait_Savant", "trait_Beguiling", 
                "trait_GreatKisser", "trait_Player", "trait_ForeverFresh", 
                "trait_ForeverFull", "trait_NeverWeary", "trait_SteelBladder", 
                "trait_Antiseptic", "trait_Shameless", "trait_Observant", 
                "trait_ProfessionalSlacker", "trait_Alluring", "trait_Longevity"
            ],
            "traits_sex_male": [],
            "traits_sex_female": []
        },
        
        "1": {
            "name": "Mortal Lover (NPC Basis)",
            "luck": {"value": 50, "locked": False},
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
            "motives_to_freeze": {},
            "exclude_all": ["unflirty", "jealous", "evil", "mean"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": ["trait_GreatKisser", "trait_Alluring", "trait_Carefree"],
            "traits_sex_male": [],
            "traits_sex_female": []
        },

        "10": {
            "name": "Blessed Child (Gespieltes Kind)",
            "luck": {"value": 100, "locked": True},
            "allow_all_skills": False,
            "max_player_skills": True,
            "max_npc_skills": False,
            "allowed_skills": [],
            "master_player_careers": False,
            "master_npc_careers": False,
            "harmony_friendship": 100,
            "harmony_romance": 0,
            "target_relationship_status": "best_friend",
            "satisfaction_points": 5000,
            "add_funds": 0,
            "max_funds": 9999999,
            "motives_to_freeze": {
                "human": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"]
            },
            "exclude_all": ["mean", "gloomy", "erratic", "clumsy", "evil"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [
                "trait_Savant", "trait_Carefree", "trait_Brave", "trait_Top_Notch_Toddler",
                "trait_ScoutingAptitude", "trait_FreeServices"
            ],
            "traits_sex_male": [],
            "traits_sex_female": []
        },
        
        "11": {
            "name": "NPC Child (Normal)",
            "luck": {"value": 0, "locked": False},
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
            "motives_to_freeze": {},
            "exclude_all": ["mean", "evil"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [],
            "traits_sex_male": [],
            "traits_sex_female": []
        }
    },

    "_comment_system": "=== AB HIER SYSTEMEINSTELLUNGEN ===",
    
    "auto_profiles": {
        "option_1": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "1", "adult_npc_female": "1",
            "child_playable": "10", "child_npc": "11"
        },
        "option_2": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "1", "adult_npc_female": "1",
            "child_playable": "10", "child_npc": "11"
        },
        "option_3": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "1", "adult_npc_female": "1",
            "child_playable": "10", "child_npc": "11"
        }
    },

    "fallback_skills": {
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