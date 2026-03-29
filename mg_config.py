import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.endswith('.ts4script') else CURRENT_DIR
CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')

DEFAULT_CONFIG = {
    "_comment_global": "MakeGod Mod Konfiguration. Alle Schluessel, die mit '_' beginnen, werden ignoriert.",
    "language": "de",
    "debug_log": False,
    "log_mode": "overwrite",
    
    "_comment_sets": "=== DEINE SIMS-EINSTELLUNGEN (SETS) ===",
    "sets": {
        "0": {
            "name": "Ultimate God (Standard Profil)",
            "luck": {"value": 100},
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
            "fill_motives_mode": "all",
            "freeze_motives": True,
            "motives_to_fill": {
                "vampire": ["commodity_motive_vampire_power", "commodity_motive_vampire_thirst", "motive_hygiene", "motive_social", "motive_fun"],
                "spellcaster": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "werewolf": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "mermaid": ["motive_hydration", "motive_hunger", "motive_energy", "motive_bladder", "motive_social", "motive_fun"],
                "human": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"]
            },
            "exclude_all": [
                "trait_Evil", "trait_Lazy", "trait_HotHeaded", "trait_Gloomy", "trait_Clumsy", "trait_Jealous", 
                "trait_Slob", "trait_Unflirty", "trait_Insane", "trait_Squeamish", "trait_Mean"
            ],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
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
                "spellcaster": ["trait_Occult_WitchOccult_BloodlineAncient", "trait_Cauldron_Potion_Immortality"],
                "vampire": ["trait_TheKnack"], 
                "werewolf": ["trait_OccultWerewolf_Immortal", "trait_OccultWerewolf_Temperaments_Lunar_Resistance"], 
                "mermaid": [],
                "human": []
            }
        },
        
        "1": {
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

    "auto_profiles": {
        "option_1": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "1", "adult_npc_female": "1",
            "child_playable": "10", "child_npc": "11"
        },
        "option_2": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "2", "adult_npc_female": "2",
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