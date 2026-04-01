import os
import json
import sims4.commands

# In einer gepackten `.ts4script`-Datei zeigt `__file__` auf den Pfad *im* Archiv.
# Config, Logs und Dumps muessen aber in den echten Mods-Ordner geschrieben werden.
MODULE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(MODULE_PATH)
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.lower().endswith('.ts4script') else CURRENT_DIR
CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')

_config_data = None

# Fallback-Konfiguration als String, damit die Formatierung erhalten bleibt
DEFAULT_CONFIG_STR = """{
    "_comment_global": "MakeGod Mod Konfiguration. Alle Schluessel, die mit '_' beginnen, werden ignoriert.",
    "language": "de",
    "debug_log": false,
    "log_mode": "overwrite",
    
    "_comment_dump": "Filtert technische Statistiken heraus, um den Dump sauber zu halten.",
    "dump_blacklist_keywords": ["_error", "_high", "_low", "caspartid", "index_0", "index_1", "index_2", "index_3", "ww_"],
    
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
            "target_relationship_status": "Erlaubt: '', 'friend', 'best_friend', 'woohoo_partner', 'significant_other', 'engaged', 'married'.",
            "remove_negative_relations": "true/false. Aktiviert die Bereinigung negativer Beziehungs-Bits (Feinde, Groll, Aengste).",
            "remove_negative_relations_household": "true/false. Wenn true, werden negative Beziehungen zu Sims im selben Haushalt IMMER geloescht.",
            "remove_negative_relations_scope": "Liste von Beziehungs-Keywords (z.B. 'friend', 'romantic'). Weltweite Sims werden nur bereinigt, wenn sie eines dieser Bits haben.",
            "satisfaction_points": "Ganzzahl >= 0. 0 = keine Zusatzpunkte.",
            "add_funds": "Ganzzahl > 0. Nur positive Werte fuegen Geld hinzu.",
            "max_funds": "Obergrenze fuer das Haushaltsgeld nach add_funds.",
            "fill_motives_mode": "Erlaubt: 'all', 'config', 'none'.",
            "freeze_motives": "true/false. Stoppt den Verfall fuer die in motives_to_fill genannten Motive soweit moeglich.",
            "motives_to_fill": {
                "keys": "Empfohlene Keys: 'human', 'vampire', 'spellcaster', 'werewolf', 'mermaid'.",
                "values": "Je Key eine Liste exakter Motiv-/Commodity-Namen wie 'motive_hunger' oder 'commodity_motive_vampire_thirst'."
            },
            "remove_all_dislikes": "true/false. Entfernt vollautomatisch alle [DISLIKE] Merkmale vom Sim (z.B. Abneigung gegen Farben/Musik).",
            "exclude_all": "Traits immer entfernen. Am sichersten mit exaktem internen Namen, z.B. 'trait_Evil'.",
            "traits_all": "Traits immer hinzufuegen. Am sichersten mit exaktem internen Namen, z.B. 'trait_Savant'.",
            "traits_occult": "Je Okkult-Typ eine Trait-Liste.",
            "perks_all": "Perks (Okkulte Faehigkeiten/Ruhm) immer hinzufuegen.",
            "perks_occult": "Perks aufgeschluesselt nach Okkult-Typ (z.B. 'vampire', 'spellcaster').",
            "spells_all": "Zaubersprueche und Traenke immer hinzufuegen.",
            "spells_occult": "Zaubersprueche aufgeschluesselt nach Okkult-Typ."
        },
        
        "0": {
            "_comment_profile": "Ultimate God (Standard Profil) - Inklusive WickedWhims God-Tier und Bestrebungs-Boni",
            "name": "Ultimate God (Standard Profil)",
            "luck": {"value": 100},
            "allow_all_skills": false,
            "max_player_skills": true,
            "max_npc_skills": false,
            "allowed_skills": [],
            "master_player_careers": true,
            "master_npc_careers": false,
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "target_relationship_status": "woohoo_partner",
            "remove_negative_relations": true,
            "remove_negative_relations_household": true,
            "remove_negative_relations_scope": ["roommate", "key", "friend", "romantic", "woohoo", "married", "significant"],
            "satisfaction_points": 50000,
            "add_funds": 9999999,
            "max_funds": 9999999,
            "fill_motives_mode": "all",
            "freeze_motives": true,
            "motives_to_fill": {
                "vampire": ["commodity_motive_vampire_power", "commodity_motive_vampire_thirst", "motive_hygiene", "motive_social", "motive_fun"],
                "spellcaster": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "werewolf": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"],
                "mermaid": ["motive_hydration", "motive_hunger", "motive_energy", "motive_bladder", "motive_social", "motive_fun"],
                "human": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"]
            },
            "remove_all_dislikes": true,
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
                "trait_PhysicallyGifted", "trait_SociallyGifted", "trait_ForeverFresh",
                "trait_Quick_Learner", "trait_High_Metabolism", "trait_EssenceOfFlavor", "trait_Alluring", 
                "trait_Gregarious", "trait_Muser", "trait_HomeTurf", "trait_Collector", "trait_FamilySim",
                "TURBODRIVER:WickedWhims_Trait_Attractiveness_Reward_UniqueLooks",
                "TURBODRIVER:WickedWhims_Trait_BodyHair_STD_NoCrabs",
                "TURBODRIVER:WickedWhims_Trait_Exhibitionist",
                "TURBODRIVER:WickedWhims_Trait_Nudity_NoSweat_Reward",
                "TURBODRIVER:WickedWhims_Trait_STD_BladderBurn_Resistant",
                "TURBODRIVER:WickedWhims_Trait_Sex_SexuallyAlluring"
            ],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {
                "spellcaster": ["trait_Occult_WitchOccult_BloodlineAncient", "trait_Cauldron_Potion_Immortality"],
                "vampire": ["trait_TheKnack"], 
                "werewolf": ["trait_OccultWerewolf_Immortal", "trait_OccultWerewolf_Temperaments_Lunar_Resistance"], 
                "mermaid": [],
                "human": []
            },
            "perks_all": [],
            "perks_occult": {
                "spellcaster": [],
                "vampire": [],
                "werewolf": []
            },
            "spells_all": [],
            "spells_occult": {
                "spellcaster": []
            }
        },
        
        "1": {
            "name": "Mortal Lover (NPC Basis)",
            "luck": {"value": 0},
            "allow_all_skills": false,
            "max_player_skills": false,
            "max_npc_skills": false,
            "allowed_skills": ["fitness", "charisma", "logic"],
            "master_player_careers": false,
            "master_npc_careers": false,
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "target_relationship_status": "significant_other",
            "remove_negative_relations": false,
            "remove_negative_relations_household": false,
            "remove_negative_relations_scope": [],
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 250000,
            "fill_motives_mode": "none",
            "freeze_motives": false,
            "motives_to_fill": {},
            "remove_all_dislikes": false,
            "exclude_all": ["trait_Unflirty", "trait_Jealous", "trait_Evil", "trait_Mean"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": ["trait_GreatKisser", "trait_Carefree"],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {},
            "perks_all": [],
            "perks_occult": {},
            "spells_all": [],
            "spells_occult": {}
        },

        "2": {
            "name": "Vanilla NPC",
            "luck": {"value": 0},
            "allow_all_skills": false,
            "max_player_skills": false,
            "max_npc_skills": false,
            "allowed_skills": [],
            "master_player_careers": false,
            "master_npc_careers": false,
            "harmony_friendship": 50,
            "harmony_romance": 0,
            "target_relationship_status": "friend",
            "remove_negative_relations": false,
            "remove_negative_relations_household": false,
            "remove_negative_relations_scope": [],
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 50000,
            "fill_motives_mode": "none",
            "freeze_motives": false,
            "motives_to_fill": {},
            "remove_all_dislikes": false,
            "exclude_all": [],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {},
            "perks_all": [],
            "perks_occult": {},
            "spells_all": [],
            "spells_occult": {}
        },

        "10": {
            "name": "Blessed Child (Gespieltes Kind)",
            "luck": {"value": 100},
            "allow_all_skills": false,
            "max_player_skills": true,
            "max_npc_skills": false,
            "allowed_skills": [],
            "master_player_careers": true,
            "master_npc_careers": false,
            "harmony_friendship": 100,
            "harmony_romance": 0,
            "target_relationship_status": "best_friend",
            "remove_negative_relations": true,
            "remove_negative_relations_household": true,
            "remove_negative_relations_scope": ["roommate", "key", "friend", "romantic", "woohoo", "married", "significant"],
            "satisfaction_points": 5000,
            "add_funds": 0,
            "max_funds": 9999999,
            "fill_motives_mode": "all",
            "freeze_motives": true,
            "motives_to_fill": {
                "human": ["motive_hunger", "motive_energy", "motive_bladder", "motive_hygiene", "motive_social", "motive_fun"]
            },
            "remove_all_dislikes": true,
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
            },
            "perks_all": [],
            "perks_occult": {},
            "spells_all": [],
            "spells_occult": {}
        },
        
        "11": {
            "name": "NPC Child (Normal)",
            "luck": {"value": 0},
            "allow_all_skills": false,
            "max_player_skills": false,
            "max_npc_skills": false,
            "allowed_skills": [],
            "master_player_careers": false,
            "master_npc_careers": false,
            "harmony_friendship": 50,
            "harmony_romance": 0,
            "target_relationship_status": "friend",
            "remove_negative_relations": false,
            "remove_negative_relations_household": false,
            "remove_negative_relations_scope": [],
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 250000,
            "fill_motives_mode": "none",
            "freeze_motives": false,
            "motives_to_fill": {},
            "remove_all_dislikes": false,
            "exclude_all": ["trait_Mean", "trait_Evil"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": [],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {},
            "perks_all": [],
            "perks_occult": {},
            "spells_all": [],
            "spells_occult": {}
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
}"""

def load_config():
    """Laedt die Konfiguration. Erstellt eine frische Datei, falls sie fehlt oder fehlerhaft ist."""
    global _config_data
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                _config_data = json.load(f)
            return
        except Exception as e:
            # Falls die Datei kaputt ist (z.B. falsches JSON Format), fangen wir den Fehler ab
            pass
            
    # Falls Datei nicht existiert oder defekt ist, nutzen wir den Standard
    try:
        _config_data = json.loads(DEFAULT_CONFIG_STR)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONFIG_STR)
    except Exception as e:
        # Als absoluter Notfall (falls der Mod-Ordner schreibgeschützt ist etc.)
        _config_data = json.loads(DEFAULT_CONFIG_STR)

def get(key, default=None):
    """Gibt einen Wert aus der Konfiguration zurueck."""
    global _config_data
    if _config_data is None:
        load_config()
    
    return _config_data.get(key, default)