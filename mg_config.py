import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.endswith('.ts4script') else CURRENT_DIR
CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')

DEFAULT_CONFIG = {
    "_comment_global": "MakeGod Mod Konfiguration. Alle Schluessel, die mit '_' beginnen, werden ignoriert.",
    "language": "de",
    "debug_log": True,
    "log_mode": "append",
    
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
    
    "sets": {
        "0": {
            "name": "Ultimate God (Adult Test Case)",
            "luck": {"value": 100, "locked": True},
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
                "vampire": ["commodity_motive_vampire_power", "commodity_motive_vampire_thirst"],
                "spellcaster": ["commodity_motive_witchoccult_charge"],
                "werewolf": ["commodity_motive_werewolf_fury"],
                "mermaid": ["motive_hydration"],
                "ghost": ["commodity_ghostpowers_stamina"],
                "alien": ["motive_brainpower"],
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
                "trait_ProfessionalSlacker", "trait_Alluring", "trait_Longevity",
                "trait_MTS_Deaderpool_McCommander_ImmortalFlag", 
                "trait_MTS_Deaderpool_McCommander_NoAgeFlag", 
                "trait_MTS_Deaderpool_McCommander_NoCullFlag", 
                "Deaderpool_MCCC_Trait_FlagNoJealousy", 
                "Deaderpool_MCCC_Trait_FlagMultiSpouse"
            ],
            "traits_sex_male": [],
            "traits_sex_female": ["TURBODRIVER:WickedWhims_Trait_Improved_Absorbency"]
        },
        "1": {
            "name": "Mortal Lover (NPC Adult)",
            "luck": {"value": 50, "locked": False},
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
            "name": "Blessed Child (Minor Test Case)",
            "luck": {"value": 100, "locked": True},
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
            "name": "NPC Child (Minor)",
            "luck": {"value": 0, "locked": False},
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