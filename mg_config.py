import os
import json
import sims4.commands

MODULE_PATH = os.path.abspath(__file__)
CURRENT_DIR = os.path.dirname(MODULE_PATH)
MOD_FOLDER = os.path.dirname(CURRENT_DIR) if CURRENT_DIR.lower().endswith('.ts4script') else CURRENT_DIR

CONFIG_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json')
TEMPLATE_FILE = os.path.join(MOD_FOLDER, 'make_god_config.json.template')

_config_data = None

DEFAULT_CONFIG_STR = """{
    "_comment_global": "MakeGod Mod Konfiguration. Alle Schluessel, die mit '_' beginnen, werden ignoriert.",
    "language": "de",
    "debug_level": "normal",
    "_comment_debug": "Level: 'none' (Aus), 'normal' (Nur Text-Log), 'all' (Text-Log + Vorher/Nachher-Dump).",
    "debug_alarm_delay": 5.0,
    "log_mode": "overwrite",
    "include_roommates_in_all": true,
    "include_keyholders_in_all": true,
    "include_woohoo_partners_in_all": true,
    "include_best_friends_in_all": true,
    "include_significant_others_in_all": true,
    "include_engaged_in_all": true,
    "include_married_in_all": true,

    "buffs_exclude_from_clear": [
        "buff_WitchOccult_MyPowerGrows",
        "buff_Motives_Werewolf_Fury",
        "buff_Vampire_Sunlight_Debuff",
        "buff_Vampire_Thirst_Debuff"
    ],

    "relationship_system": {
        "global_rules": {
            "allow_downgrade": false,
            "allow_incest": false,
            "allow_teen_adult_romance": false
        },
        "status_definitions": {
            "friend": {
                "add_bits": ["friendship-friend", "relbit_Friend"],
                "remove_conflicts": ["enemy", "despised", "bit_NoLongerFriends"]
            },
            "best_friend": {
                "add_bits": ["friendship-bff", "relbit_BestFriends"],
                "remove_conflicts": ["enemy", "despised", "bit_NoLongerFriends"]
            },
            "woohoo_partner": {
                "add_bits": ["relBit_SexualORientation_WooHooPartners", "RomanticCombo_WoohooPartners"],
                "remove_conflicts": ["RomanticCombo_Soulmates", "RomanticCombo_Married", "enemy", "despised"]
            },
            "significant_other": {
                "add_bits": ["RomanticCombo_SignificantOther"],
                "remove_conflicts": ["RomanticCombo_Soulmates", "RomanticCombo_Married", "enemy", "relbit_SocialContext_Awkwardness_Casual"]
            },
            "engaged": {
                "add_bits": ["RomanticCombo_Engaged"],
                "remove_conflicts": ["RomanticCombo_Married", "enemy"]
            },
            "married": {
                "add_bits": ["RomanticCombo_Married"],
                "remove_conflicts": ["enemy"]
            }
        }
    },

    "manual_add_settings": {
        "_comment": "Einstellungen fuer den Befehl rmg.add. Werte -999 ignorieren die Zuweisung.",
        "friendship": 100,
        "romance": -999,
        "spawn_sim": true
    },

    "batches": {
        "_comment": "Befehlslisten. Platzhalter wie {0}, {1} werden durch zusaetzliche Parameter ersetzt (z.B. rmg.bat setup_npc \\"yuki behr\\\").",
        "test_batch": [
            "rmg.dump all",
            "rmg.all",
            "rmg.dump all"
        ],
        "deb": [
            "rmg.dump",
            "rmg.active debug",
            "rmg.dump",
            "rmg.active debug",
            "rmg.dump"
        ],
        "setup_npc": [
            "rmg.add name {0}",
            "rmg.name {0} 3"
        ],
        "setup_couple": [
            "rmg.add name {0}",
            "rmg.name {0} 3",
            "rmg.add name {1}",
            "rmg.name {1} 1"
        ],
        "setup_custom_npc": [
            "rmg.add id [sim_id]",
            "sims.give_satisfaction_points {0} [sim_id]",
            "rmg.id [sim_id] {1}"
        ],
        "setup_my_npcs": [
            "rmg.add name Morgan Fyres",
            "rmg.name Morgan Fyres 3",
            "rmg.add name Baby Ariel",
            "rmg.name Baby Ariel 3",
            "rmg.add name Holly Alto",
            "rmg.name Holly Alto 3",
            "rmg.add name Kayla Flemming",
            "rmg.name Kayla Flemming 3",
            "rmg.add name Olivia Hand",
            "rmg.name Olivia Hand 3",
            "rmg.add name Titania Summerdream",
            "rmg.name Titania Summerdream 3",
            "rmg.add name Sofia Bjergsen",
            "rmg.name Sofia Bjergsen 3",
            "rmg.add name Luna Villareal",
            "rmg.name Luna Villareal 3",
            "rmg.add name Yuki Behr",
            "rmg.name Yuki Behr 3",
            "rmg.add name Jade Rosa",
            "rmg.name Jade Rosa 3",
            "rmg.add name Miko Ojo",
            "rmg.name Miko Ojo 3",
            "rmg.add name Alice Martin",
            "rmg.name Alice Martin 3",
            "rmg.add name Marra Summerdream",
            "rmg.name Marra Summerdream 3",
            "rmg.add name Sienna Grove"
        ]
    },

    "_comment_macros": "=== UI MACRO SYSTEM ===",
    "_help_macros": "Hier definierst du, was die Buttons im Klick-Menue tun. Nutze [sim_id] als Platzhalter fuer den angeklickten Sim.",
    "macros": {
        "ui_playable_01": [
            "rmg.id [sim_id] option_1"
        ],
        "ui_playable_02": [
            "sims.give_satisfaction_points 10000 [sim_id]"
        ],
        "ui_playable_03": [
            "rmg.dump id [sim_id]"
        ],
        "ui_playable_04": [],
        "ui_playable_05": [],

        "ui_npc_01": [
            "rmg.id [sim_id] 1"
        ],
        "ui_npc_02": [
            "rmg.id [sim_id] 5"
        ],
        "ui_npc_03": [
            "rmg.id [sim_id] 4"
        ],
        "ui_npc_04": [],
        "ui_npc_05": [
            "rmg.add id [sim_id]",
            "sims.give_satisfaction_points 5000 [sim_id]",
            "rmg.id [sim_id] 3",
            "rmg.dump id [sim_id]"
        ]
    },
    
    "_comment_dump": "Filtert technische Statistiken heraus, um den Dump sauber zu halten.",
    "dump_blacklist_keywords": ["_error", "_high", "_low", "caspartid", "index_0", "index_1", "index_2", "index_3"],
    
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
            "harmony_friendship": "-999 = nicht anfassen. Sonst typischer Bereich -100 bis 100.",
            "harmony_romance": "-999 = nicht anfassen. Sonst typischer Bereich -100 bis 100.",
            "target_relationship_status": "Erlaubt: '', 'friend', 'best_friend', 'woohoo_partner', 'significant_other', 'engaged', 'married'. Kann auch als Liste uebergeben werden, z.B. ['best_friend', 'woohoo_partner'].",
            "remove_negative_relations": "true/false. Aktiviert die Bereinigung negativer Beziehungs-Bits (Feinde, Groll, Aengste).",
            "remove_negative_relations_household": "true/false. Wenn true, werden negative Beziehungen zu Sims im selben Haushalt IMMER geloescht.",
            "remove_negative_relations_scope": "Liste von Beziehungs-Keywords. Weltweite Sims werden nur bereinigt, wenn sie eines dieser Bits haben.",
            "harmony_extended_network": "Erweiterte Beziehungs-Matrix. Unterscheidet nach source_male/female und Alter. -999 bedeutet ignorieren.",
            "satisfaction_points": "Ganzzahl >= 0. 0 = keine Zusatzpunkte.",
            "add_funds": "Ganzzahl > 0. Nur positive Werte fuegen Geld hinzu.",
            "max_funds": "Obergrenze fuer das Haushaltsgeld nach add_funds.",
            "fill_motives_mode": "Erlaubt: 'all', 'config', 'none'.",
            "freeze_motives": "true/false. Stoppt den Verfall fuer die in motives_to_fill genannten Motive soweit moeglich.",
            "remove_all_dislikes": "true/false. Entfernt vollautomatisch alle [DISLIKE] Merkmale vom Sim.",
            "exclude_all": "Traits immer entfernen. Am sichersten mit exaktem internen Namen.",
            "traits_all": "Traits immer hinzufuegen. Am sichersten mit exaktem internen Namen.",
            "remove_unlisted_perks": "true/false. Sperrt (lock_perk) alle Perks, die der Sim hat, aber nicht in perks_occult aufgelistet sind.",
            "perks_exclude_all": "Perks, die explizit gesperrt werden sollen.",
            "perks_occult": "Perks aufgeschluesselt nach Okkult-Typ (z.B. 'vampire', 'spellcaster')."
        },
        
        "0": {
            "name": "Ultimate God (Standard Profil)",
            "luck": {"value": 100},
            "allow_all_skills": true,
            "max_player_skills": true,
            "max_npc_skills": false,
            "allowed_skills": [],
            "master_player_careers": true,
            "master_npc_careers": false,
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "target_relationship_status": ["best_friend", "woohoo_partner"],
            "remove_negative_relations": true,
            "remove_negative_relations_household": true,
            "remove_negative_relations_scope": ["roommate", "key", "friend", "romantic", "woohoo", "married", "significant"],
            "harmony_extended_network": {
                "enabled": true,
                "scopes": ["family", "romantic", "roommate", "key"],
                "source_male": {
                    "target_female": { 
                        "Infant": {"friendship": 20, "romance": -999},
                        "Toddler": {"friendship": 20, "romance": -999},
                        "Child": {"friendship": 20, "romance": -999},
                        "Teen": {"friendship": 20, "romance": -999},
                        "Young_Adult": {"friendship": 20, "romance": -999},
                        "Adult": {"friendship": 20, "romance": -999},
                        "Elder": {"friendship": -999, "romance": -999}
                    },
                    "target_male": { 
                        "Infant": {"friendship": -999, "romance": -999},
                        "Toddler": {"friendship": -999, "romance": -999},
                        "Child": {"friendship": -999, "romance": -999},
                        "Teen": {"friendship": -999, "romance": -999},
                        "Young_Adult": {"friendship": -999, "romance": -999},
                        "Adult": {"friendship": -999, "romance": -999},
                        "Elder": {"friendship": -999, "romance": -999}
                    }
                },
                "source_female": {
                    "target_female": { 
                        "Infant": {"friendship": 20, "romance": -999},
                        "Toddler": {"friendship": 20, "romance": -999},
                        "Child": {"friendship": 20, "romance": -999},
                        "Teen": {"friendship": 20, "romance": -999},
                        "Young_Adult": {"friendship": 20, "romance": -999},
                        "Adult": {"friendship": 20, "romance": -999},
                        "Elder": {"friendship": -999, "romance": -999}
                    },
                    "target_male": { 
                        "Infant": {"friendship": -999, "romance": -999},
                        "Toddler": {"friendship": -999, "romance": -999},
                        "Child": {"friendship": -999, "romance": -999},
                        "Teen": {"friendship": -999, "romance": -999},
                        "Young_Adult": {"friendship": -999, "romance": -999},
                        "Adult": {"friendship": -999, "romance": -999},
                        "Elder": {"friendship": -999, "romance": -999}
                    }
                }
            },
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
                "Deaderpool_MCCC_Trait_FlagFreezePhysique",
                "Deaderpool_MCCC_Trait_FlagNoRelCull",
                "trait_MTS_Deaderpool_McCommander_NoCullFlag",
                "Deaderpool_MCCC_Trait_FlagNoJealousy",
                "Deaderpool_MCCC_Trait_FlagMultiSpouse",
                "trait_MTS_Deaderpool_McCommander_ImmortalFlag",
                "trait_MTS_Deaderpool_McCommander_NoAgeFlag",
                "TURBODRIVER:WickedWhims_Trait_Attractiveness_Reward_UniqueLooks",
                "TURBODRIVER:WickedWhims_Trait_Exhibitionist",
                "TURBODRIVER:WickedWhims_Trait_Nudity_NoSweat_Reward",
                "TURBODRIVER:WickedWhims_Trait_Sex_SexuallyAlluring",
                "TURBODRIVER:WickedWhims_Trait_Sex_AlwaysAccept",
                "TURBODRIVER:WickedWhims_Trait_Sex_Attribute_GenerousLover",
                "TURBODRIVER:WickedWhims_Trait_Relationships_Poly",
                "TURBODRIVER:WickedWhims_Trait_STD_BladderBurn_Resistant",
                "TURBODRIVER:WickedWhims_Trait_BodyHair_STD_NoCrabs",
                "TURBODRIVER:WickedWhims_Trait_NudityEnthusiast"
            ],
            "traits_sex_male": [],
            "traits_sex_female": [
                "TURBODRIVER:WickedWhims_Trait_Improved_Absorbency"
            ],
            "traits_occult": {
                "spellcaster": ["trait_Occult_WitchOccult_BloodlineAncient", "trait_Cauldron_Potion_Immortality"],
                "vampire": ["trait_TheKnack"], 
                "werewolf": ["trait_OccultWerewolf_Immortal", "trait_OccultWerewolf_Temperaments_Lunar_Resistance"], 
                "mermaid": [],
                "human": []
            },
            "remove_unlisted_perks": true,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {
                "spellcaster": [
                    "witchPerks_Alchemy_1_BlenderArm", "witchPerks_Alchemy_2_FrugalCombinations", "witchPerks_Alchemy_3_ExtraChemistry", "witchPerks_Alchemy_4_MixMaster", "witchPerks_Alchemy_5_PotentPotables",
                    "witchPerks_Prowess_1_KnowledgeIsMagic", "witchPerks_Prowess_2_MoteHound", "witchPerks_Prowess_3_ChargeControl", "witchPerks_Prowess_4_Hexproof", "witchPerks_Prowess_5_MagicalResonance",
                    "witchPerks_Spellcasting_1_Discharge", "witchPerks_Spellcasting_2_PowerShunt", "witchPerks_Spellcasting_3_SpectralReach", "witchPerks_Spellcasting_4_MasterCaster", "witchPerks_Spellcasting_5_MasterDuelist",
                    "witchPerks_Open_1A_IncredibleForager", "witchPerks_Open_1B_Experimenter", "witchPerks_Open_2A_InsightfulEye", "witchPerks_Open_2B_WitchSocialite", "witchPerks_Open_3A_MischiefMaster", 
                    "witchPerks_Open_3B_TameTheUntameable", "witchPerks_Open_3C_PracticedPracticality", "witchPerks_Open_4A_NaturalMentor", "witchPerks_Open_4B_MagicalDiscounts"
                ],
                "vampire": [
                    "vampirePerks_MindPowers_AlluringVisage_Level1", "vampirePerks_MindPowers_AlluringVisage_Level2", "vampirePerks_MindPowers_AlluringVisage_Level3",
                    "vampirePerks_MindPowers_Command", "vampirePerks_MindPowers_DetectPersonality", "vampirePerks_MindPowers_Mesmerize",
                    "vampirePerks_PersonaPowers_GarlicImmunity", "vampirePerks_PersonaPowers_LoseHumanity_Hygiene", 
                    "vampirePerks_PersonaPowers_ResistanceSolis_Level1", "vampirePerks_PersonaPowers_ResistanceSolis_Level2", "vampirePerks_PersonaPowers_ResistanceSolis_Level3",
                    "vampirePerks_PersonaPowers_TameTheThirst",
                    "vampirePerks_PersonaPowers_VampiricSlumber_Level1", "vampirePerks_PersonaPowers_VampiricSlumber_Level2", "vampirePerks_PersonaPowers_VampiricSlumber_Level3",
                    "vampirePerks_SpiritPowers_AlwaysWelcome", "vampirePerks_SpiritPowers_BatForm", "vampirePerks_SpiritPowers_MistForm", "vampirePerks_SpiritPowers_VampireRun"
                ],
                "werewolf": [
                    "werewolfPerks_EnhancedSenses", "werewolfPerks_Hunter", "werewolfPerks_ImmortalWolf", "werewolfPerks_LunarResistance", 
                    "werewolfPerks_NaturalHealing", "werewolfPerks_Nightvision", "werewolfPerks_PersonalGrooming", "werewolfPerks_TheWillToResist", "werewolfPerks_WolfNap"
                ],
                "fairy": [
                    "fairyPerks_BloomPlant", "fairyPerks_CureAilment", "fairyPerks_DetectHarvestables", "fairyPerks_FairyInsight", "fairyPerks_PlantGrowth", "fairyPerks_ResistSpilloverBuffs"
                ],
                "ghost": [
                    "ghostPowersPerks_GhostlyMovement", "ghostPowersPerks_ImproveLife", "ghostPowersPerks_InstantMaintenance", "ghostPowersPerks_InstantMaintenance_2", "ghostPowersPerks_InstantMaintenance_3", 
                    "ghostPowersPerks_NurtureLife", "ghostPowersPerks_PositivePresence", "ghostPowersPerks_SaveALife", "ghostPowersPerks_StrongerStamina", "ghostPowersPerks_WarmEmbrace"
                ]
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
            "harmony_extended_network": {"enabled": false},
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
            "remove_unlisted_perks": false,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {}
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
            "harmony_romance": -999,
            "target_relationship_status": "friend",
            "remove_negative_relations": false,
            "remove_negative_relations_household": false,
            "remove_negative_relations_scope": [],
            "harmony_extended_network": {"enabled": false},
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
            "remove_unlisted_perks": false,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {}
        },
        "3": {
            "name": "Perfect Woohoo NPC (Female)",
            "luck": {"value": 50},
            "allow_all_skills": false,
            "max_player_skills": false,
            "max_npc_skills": true,
            "allowed_skills": ["fitness", "charisma", "cooking"],
            "master_player_careers": false,
            "master_npc_careers": true,
            "harmony_friendship": 100,
            "harmony_romance": 100,
            "target_relationship_status": "woohoo_partner",
            "remove_negative_relations": true,
            "remove_negative_relations_household": true,
            "remove_negative_relations_scope": ["roommate", "key"],
            "harmony_extended_network": {"enabled": false},
            "satisfaction_points": 5000,
            "add_funds": 100000,
            "max_funds": 1500000,
            "fill_motives_mode": "all",
            "freeze_motives": true,
            "motives_to_fill": {
                "human": ["motive_hunger", "motive_energy", "motive_hygiene", "motive_fun"]
            },
            "remove_all_dislikes": true,
            "exclude_all": [
                "trait_Unflirty", 
                "trait_Jealous", 
                "trait_Evil", 
                "trait_Mean", 
                "trait_Squeamish"
            ],
            "traits_all": [
                "trait_GreatKisser", 
                "trait_Carefree", 
                "trait_Shameless",
                "trait_MTS_Deaderpool_McCommander_NoAgeFlag",
                "trait_MTS_Deaderpool_McCommander_ImmortalFlag",
                "trait_MTS_Deaderpool_McCommander_NoOffspringFlag",
                "Deaderpool_MCCC_Trait_FlagNoJealousy",
                "Deaderpool_MCCC_Trait_FlagNoAgeFlag",
                "TURBODRIVER:WickedWhims_Trait_STD_BladderBurn_Resistant",
                "TURBODRIVER:WickedWhims_Trait_BodyHair_STD_NoCrabs",
                "TURBODRIVER:WickedWhims_Trait_Sex_AlwaysAccept",
                "TURBODRIVER:WickedWhims_Trait_Sex_SexuallyAlluring",
                "TURBODRIVER:WickedWhims_Trait_Nudity_NoSweat_Reward",
                "TURBODRIVER:WickedWhims_Trait_Relationships_Poly"
            ],
            "traits_sex_female": [
                "TURBODRIVER:WickedWhims_Trait_Improved_Absorbency"
            ],
            "traits_occult": {},
            "remove_unlisted_perks": false,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {}
        },
        "4": {
            "name": "Dark Occult (Boese)",
            "luck": {"value": -50},
            "allow_all_skills": false,
            "max_player_skills": false,
            "max_npc_skills": false,
            "allowed_skills": [],
            "master_player_careers": false,
            "master_npc_careers": false,
            "harmony_friendship": 0,
            "harmony_romance": -999,
            "target_relationship_status": "",
            "remove_negative_relations": false,
            "remove_negative_relations_household": false,
            "remove_negative_relations_scope": [],
            "harmony_extended_network": {"enabled": false},
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 50000,
            "fill_motives_mode": "none",
            "freeze_motives": false,
            "motives_to_fill": {},
            "remove_all_dislikes": false,
            "exclude_all": ["trait_Good", "trait_Friendly", "trait_Carefree", "trait_Cheerful"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": ["trait_Evil", "trait_Mean"],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {},
            "remove_unlisted_perks": false,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {
                "spellcaster": ["witchPerks_Prowess_5_MagicalResonance", "witchPerks_Spellcasting_5_MasterDuelist"],
                "vampire": ["vampirePerks_MindPowers_EmotionalBurst_Level1", "vampirePerks_MindPowers_EmotionalBurst_Level2", "vampirePerks_MindPowers_EmotionalBurst_Level3", "vampirePerks_MindPowers_Hallucinate", "vampirePerks_MindPowers_IrresistibleSlumber", "vampirePerks_SpiritPowers_ManipulateLifeSpirit"],
                "fairy": ["fairyPerks_PlayWithLuck_1", "fairyPerks_PlayWithLuck_2", "fairyPerks_PlayWithTheirMood", "fairyPerks_ProjectMyMood", "fairyPerks_InfluenceRelationship_1", "fairyPerks_InfluenceRelationship_2", "fairyPerks_InfluenceSentiment_1", "fairyPerks_InfluenceSentiment_2"],
                "ghost": ["ghostPowersPerks_FearTheNight", "ghostPowersPerks_RemoveMaterial", "ghostPowersPerks_GhostlyMovement", "ghostPowersPerks_SpookyWoohoo"]
            }
        },

        "5": {
            "name": "Blessed Occult NPC (Gut)",
            "luck": {"value": 50},
            "allow_all_skills": false,
            "max_player_skills": false,
            "max_npc_skills": false,
            "allowed_skills": [],
            "master_player_careers": false,
            "master_npc_careers": false,
            "harmony_friendship": 50,
            "harmony_romance": -999,
            "target_relationship_status": "",
            "remove_negative_relations": false,
            "remove_negative_relations_household": false,
            "remove_negative_relations_scope": [],
            "harmony_extended_network": {"enabled": false},
            "satisfaction_points": 0,
            "add_funds": 0,
            "max_funds": 50000,
            "fill_motives_mode": "none",
            "freeze_motives": false,
            "motives_to_fill": {},
            "remove_all_dislikes": false,
            "exclude_all": ["trait_Evil", "trait_Mean"],
            "exclude_sex_male": [],
            "exclude_sex_female": [],
            "traits_all": ["trait_Good", "trait_Friendly"],
            "traits_sex_male": [],
            "traits_sex_female": [],
            "traits_occult": {},
            "remove_unlisted_perks": false,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {
                "spellcaster": ["witchPerks_Prowess_1_KnowledgeIsMagic", "witchPerks_Spellcasting_1_Discharge"],
                "vampire": ["vampirePerks_PersonaPowers_GarlicImmunity", "vampirePerks_PersonaPowers_ResistanceSolis_Level1", "vampirePerks_PersonaPowers_ResistanceSolis_Level2", "vampirePerks_PersonaPowers_ResistanceSolis_Level3", "vampirePerks_PersonaPowers_TameTheThirst", "vampirePerks_PersonaPowers_VampiricSlumber_Level1", "vampirePerks_PersonaPowers_VampiricSlumber_Level2", "vampirePerks_PersonaPowers_VampiricSlumber_Level3"],
                "werewolf": ["werewolfPerks_ImmortalWolf", "werewolfPerks_LunarResistance", "werewolfPerks_NaturalHealing", "werewolfPerks_WolfNap", "werewolfPerks_TheWillToResist"],
                "fairy": ["fairyPerks_BloomPlant", "fairyPerks_CureAilment", "fairyPerks_FairyInsight", "fairyPerks_PlantGrowth", "fairyPerks_ResistSpilloverBuffs"],
                "ghost": ["ghostPowersPerks_ImproveLife", "ghostPowersPerks_InstantMaintenance", "ghostPowersPerks_InstantMaintenance_2", "ghostPowersPerks_InstantMaintenance_3", "ghostPowersPerks_NurtureLife", "ghostPowersPerks_PositivePresence", "ghostPowersPerks_SaveALife"]
            }
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
            "harmony_romance": -999,
            "target_relationship_status": "best_friend",
            "remove_negative_relations": true,
            "remove_negative_relations_household": true,
            "remove_negative_relations_scope": ["roommate", "key", "friend", "romantic", "woohoo", "married", "significant"],
            "harmony_extended_network": {"enabled": false},
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
            "remove_unlisted_perks": false,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {}
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
            "harmony_romance": -999,
            "target_relationship_status": "friend",
            "remove_negative_relations": false,
            "remove_negative_relations_household": false,
            "remove_negative_relations_scope": [],
            "harmony_extended_network": {"enabled": false},
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
            "remove_unlisted_perks": false,
            "perks_exclude_all": [],
            "perks_exclude_occult": {},
            "perks_all": [],
            "perks_occult": {}
        }
    },

    "auto_profiles": {
        "option_1": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "2", "adult_npc_female": "3",
            "child_playable": "10", "child_npc": "11"
        },
        "option_2": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "2", "adult_npc_female": "2",
            "child_playable": "10", "child_npc": "11"
        },
        "option_3": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "2", "adult_npc_female": "1",
            "child_playable": "10", "child_npc": "11"
        },
        "option_4": {
            "adult_playable_male": "0", "adult_playable_female": "0", 
            "adult_npc_male": "2", "adult_npc_female": "5",
            "child_playable": "10", "child_npc": "11"
        }
    },

    "fallback_skills": {
        "adult": [
            "adultmajor", "adultminor", "skill_fitness", "skill_archery", "skill_crossstitch", 
            "skill_dogtraining", "skill_retail", "skill_hidden_skating", "skill_hidden_vampirelore", 
            "woohoo_skill", "humanoidrobot", "skill_child", "skill_toddler", "infant"
        ],
        "child": ["skill_child", "skill_toddler", "infant"],
        "toddler": ["skill_toddler", "infant"],
        "infant": ["infant"]
    }
}"""

def _update_dict_recursively(d, u):
    for k, v in u.items():
        if isinstance(v, dict) and k in d and isinstance(d[k], dict):
            _update_dict_recursively(d[k], v)
        else:
            d[k] = v

def load_config():
    global _config_data
    try:
        with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONFIG_STR)
    except: pass

    default_data = json.loads(DEFAULT_CONFIG_STR)

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
            
            _update_dict_recursively(default_data, user_data)
            _config_data = default_data
            
            try:
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(_config_data, f, indent=4)
            except: pass
            return
        except Exception:
            try:
                import shutil
                shutil.copy(CONFIG_FILE, CONFIG_FILE + ".corrupted")
            except: pass
            _config_data = default_data
            return
            
    try:
        _config_data = default_data
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            f.write(DEFAULT_CONFIG_STR)
    except Exception:
        _config_data = default_data

def get(key, default=None):
    global _config_data
    if _config_data is None:
        load_config()
    return _config_data.get(key, default)