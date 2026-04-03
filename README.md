# **🌟 MakeGod Mod für Die Sims 4**

Willkommen bei **MakeGod**! Dies ist nicht einfach nur eine weitere Cheat-Mod - es ist ein extrem mächtiges, blitzschnelles und hochgradig anpassbares Werkzeug, um das Leben deiner Sims mit nur einem einzigen Klick komplett zu perfektionieren (oder zu ruinieren, je nachdem, was du in der Konfiguration einstellst!).  
Egal, ob du einen unsterblichen Super-Vampir, ein absolutes Wunderkind oder einfach nur den perfekten Nachbarn erschaffen willst: MakeGod erledigt in einem Bruchteil einer Sekunde das, wofür du sonst stundenlang Cheats eintippen müsstest.  
*Der Mod ist ein Hobby-Projekt zum Kennenlernen der Modding-Funktionalität, und ich übernehme keine Gewähr auf Vollständigkeit.* *INFO: Der Mod wurde fast ausschließlich mit Unterstützung von KI (Gemini) erstellt.*

## **📥 Installation**

Die Installation ist super einfach und erfordert nur zwei Schritte:

1. Lade dir die neueste Version von MakeGod herunter. Du erhältst zwei Dateien:  
   * `make_god.ts4script` (Die Logik und das Gehirn der Mod)  
   * `Relnan_MakeGod_UI.package` (Das Ingame-Menü, falls verfügbar)  
2. Kopiere **beide Dateien** in deinen Die Sims 4 Mods-Ordner.  
   * Standard-Pfad: `Dokumente\Electronic Arts\Die Sims 4\Mods`  
3. **WICHTIG:** Gehe im Spiel in die Optionen unter "Weiteres" und stelle sicher, dass **"Benutzerdefinierte Inhalte und Mods aktivieren"** sowie **"Script-Mods erlaubt"** mit einem Häkchen versehen sind!

## **🚀 Schnellstart für Einsteiger (2 Minuten)**

Wenn du nur kopieren und einfache Dateien bearbeiten kannst, reicht das hier völlig:

1. Installiere die Mod wie oben beschrieben.  
2. Starte das Spiel und lade einen Haushalt.  
3. Öffne die Cheat-Konsole mit `Strg + Shift + C`.  
4. Gib ein: `rmg.active`  
5. **Fertig.** Dein aktuell ausgewählter Sim bekommt das ultimative "God-Setup" (Maximale Skills, Millionen Simoleons, keine schlechte Laune mehr, ewige Bedürfnisse).

Wenn du den **ganzen Haushalt** auf einmal upgraden willst:  
Gib in die Konsole einfach `rmg.all` ein.

## **🎮 Wie benutze ich die Mod im Spiel?**

Sobald du im Live-Modus bist, hast du zwei Möglichkeiten, die Mod zu nutzen: über das bequeme Klick-Menü oder über Profi-Textbefehle.

### **🖱️ Methode 1: Das Klick-Menü (Empfohlen für jeden)**

1. Klicke einfach auf irgendeinen Sim (egal ob es dein eigener ist oder ein fremder Townie auf der Straße).  
2. Gehe in das Menü **Aktionen**.  
3. Dort findest du nun die neuen Optionen:  
   * **Make God - Sim Option 1:** Wendet dein "Profil 1" (Standard: Absolute Perfektion) auf diesen einen Sim an.  
   * **Make God - Sim Option 2:** Wendet dein "Profil 2" auf diesen Sim an.  
   * **Make God - Sim Option 3:** Wendet dein "Profil 3" auf diesen Sim an.  
   * **Make God - Household:** *Dieser Button taucht nur bei deinen gespielten Sims auf!* Er wendet MakeGod blitzschnell auf den **kompletten Haushalt** an.

### **⌨️ Methode 2: Die Cheat-Konsole (einfach und zuverlässig)**

Drücke im Spiel `Strg + Shift + C`, um die Konsole zu öffnen. Die Mod bringt eigene Befehle mit, die du eintippen kannst:

* `rmg` - Zeigt die integrierte Hilfe in der Cheat-Konsole.  
* `rmg.all [Set_ID|auto|option_xx] [debug]` - Wendet MakeGod auf den ganzen aktiven Haushalt an.  
* `rmg.active [Set_ID|auto|option_xx] [debug]` - Wendet MakeGod auf den aktuell ausgewählten Sim an.
* `rmg.add id <SimID>` - Verbindet einen Sim gezielt via ID mit deinem aktiven Sim (Freundschaft/Romantik).
* `rmg.add name <Name>` - Verbindet einen Sim via Name mit deinem aktiven Sim. (Bei mehreren Treffern gibt die Konsole die IDs aus).
* `rmg.id <SimID> [Set_ID|auto|option_xx] [debug]` - Wendet MakeGod auf einen Sim über seine interne ID an.  
* `rmg.name "Bella Grusel" [Set_ID|auto|option_xx] [debug]` - Sucht nach einem Sim per Name.  
* `rmg.bat <BatchName> [id "ID1,ID2"|name "Name1,Name2"|active] [Arg1] [Arg2] ...` - Führt eine automatisierte Liste von Befehlen nacheinander aus (unterstützt Platzhalter und Listen-Targeting).
* `rmg auto` - Kurzbefehl für `rmg all auto`.  
* `rmg.dump active` oder `rmg.dump all` - Erstellt Export-Dateien deiner Sims (siehe unten).  
* `rmg.dump reference` - Exportiert eine Master-Liste aller Spiel-Codes (siehe unten).

*Tipp:* Mit dem Zusatz `debug` (z.B. `rmg.active 0 debug`) bekommst du ausführlichere Ausgaben und Log-Einträge. Das Wort `debug` muss dabei immer am Ende des Befehls stehen.

### 🤖 **Das Batch-System (rmg.bat)**
Du kannst in der `make_god_config.json` unter dem Punkt `"batches"` eigene Listen von Befehlen definieren, die die Mod nacheinander abarbeiten soll. Das ist perfekt, wenn du bei einem neuen Spielstart immer wiederkehrende Szenarien aufbauen möchtest.

**Sims direkt anvisieren (Targeting):**
Du kannst einen Batch gezielt für eine Liste von Sims aufrufen:
* `rmg.bat <BatchName> id "12345, 67890"`
* `rmg.bat <BatchName> name "Yuki Behr, Bella Grusel"`
* `rmg.bat <BatchName> active`

**Kontext-Platzhalter für die anvisierten Sims:**
In deinen Batch-Befehlen kannst du Platzhalter verwenden, die automatisch mit den Daten des gerade verarbeiteten Sims gefüllt werden:
* `[sim_id]` - Die interne ID des Sims
* `[sim_first]` - Der Vorname
* `[sim_last]` - Der Nachname
* `[sim_name]` - Der komplette Name (inkl. Anführungszeichen)

**Dynamische Templates (Positions-Platzhalter):**
Du kannst auch Platzhalter wie `{0}`, `{1}` verwenden. Beim Aufruf des Batches übergibst du die entsprechenden Werte einfach am Ende als Parameter. 
*Wichtig:* Wenn du einen Vor- und Nachnamen als ein einziges Argument übergeben willst, musst du ihn zwingend in Anführungszeichen setzen!

*Beispiel in der Config:*
```json
"setup_npc": [
    "rmg.add id [sim_id]",
    "rmg.id [sim_id] 3"
]
```

Eingabe im Spiel: `rmg.bat setup_npc name "Yuki Behr, Bella Grusel"`

(Achtung: Wenn du sehr viele Sims in einem einzigen Batch verarbeitest, kann das Spiel für einige Sekunden einfrieren, da die Engine alle Befehle nacheinander verarbeiten muss.)

## **⚙️ Wie passe ich die Mod an? (Die Config-Datei)**

Das wahre Herzstück dieser Mod ist die **Konfigurationsdatei**.  
Startest du das Spiel mit der Mod, generiert sie automatisch eine make_god_config.json in deinem Mods-Ordner. Du kannst sie mit jedem Texteditor (wie dem normalen Windows Editor oder Notepad++) öffnen.

### **Einsteiger-Modus: Nur 3 Dinge ändern**

Wenn du möglichst wenig anfassen willst, ändere nur diese Punkte in make_god_config.json:

1. Unter auto_profiles festlegen, welches Set bei Option 1 / 2 / 3 verwendet wird.  
2. Im gewünschten Set ("0", "1", "10" ...) nur traits_all anpassen.  
3. Optional add_funds ändern, wenn du mehr oder weniger Geld geben willst.

### **Was sind "Sets"?**

In der Datei findest du einen Bereich namens "sets". Ein Set ist quasi ein Bauplan für einen Sim.  
Ein Set kann unter anderem Traits hinzufügen oder entfernen, Abneigungen löschen, Skills maximieren, Karrieren pushen, Zufriedenheitspunkte vergeben, Bedürfnisse einfrieren, Beziehungen innerhalb des Haushalts setzen und Haushaltsgeld anpassen.  
Standardmäßig gibt es z.B.:

* **Set 0 (Ultimate God):** Der Sim kriegt alle Fähigkeiten auf Maximum, alle Karrieren auf Stufe 10, Millionen von Simoleons, negative Merkmale (wie "Böse" oder Abneigungen) werden gelöscht und seine Bedürfnisse frieren für immer auf Maximum ein. Zudem lernt er alle Zauber und Okkult-Perks.  
* **Set 10 (Blessed Child):** Das perfekte Kinder-Profil. Karrieren werden ignoriert, aber die Kinder-Fähigkeiten (Motorik, Kreativität) werden gemaxt.

### **📊 Standard-Sets im Überblick**

| Set-ID | Name | Zielgruppe | Kernfunktionen |
|--------|------|------------|----------------|
| `0` | Ultimate God | Spielbarer Erwachsener | Alle Skills + Karrieren max., 9,9 Mio. Simoleons, Bedürfnisse einfrieren, negative Traits entfernen, WickedWhims-Traits |
| `1` | Mortal Lover | NPC-Partner | Freundschaft + Romantik 100, Status "Bedeutende/r Andere/r", wenige Trait-Korrekturen |
| `2` | Vanilla NPC | Neutraler Townie | Freundschaft 50, keinerlei Geld- oder Skill-Eingriff |
| `3` | Enhanced NPC | Weibliche Roommates/NPCs | MCCC/WW Flags, Unsterblichkeit, diverse positive Traits, keine negativen Traits |
| `10` | Blessed Child | Spielbares Kind / Kleinkind | Altersgerechte Skills, Bedürfnisse einfrieren, Kindheits-Boni |
| `11` | NPC Child | NPC-Kind | Nur „Gemein" und „Böse" entfernen – sonst kein Eingriff |

Eigene Sets anlegen: Kopiere einen vorhandenen Block in der `make_god_config.json`, vergib eine neue ID (z. B. `"5"` oder `"boss_npc"`) und trage sie in `auto_profiles` ein.

### **Was sind "Auto Profile"?**

Die Mod ist schlau! Wenn du im Spiel auf "Option 1" klickst, bekommt nicht jeder Sim einfach stur "Set 0" aufgedrückt.  
In der Config unter "auto_profiles" ist geregelt, wer welchen Bauplan bekommt.

* *Beispiel:* Du hast Option 1 geklickt. Die Mod sieht: "Aha, das ist ein spielbarer Erwachsener, er bekommt **Set 0**." - "Oh, das daneben ist ein Kind, es bekommt automatisch **Set 10**."  
  Du kannst die Zuweisungen für NPCs, Männer, Frauen und Kinder hier völlig frei anpassen!

### **So baust du eigene Sets (Wichtige Parameter):**

Die Datei enthält ein eingebautes Lexikon (_help_set_parameter). Hier ist kurz erklärt, wie die wichtigsten Parameter funktionieren:

* **Fähigkeiten (Skills):** max_player_skills und max_npc_skills steuern, ob Skills überhaupt maximiert werden. Mit allowed_skills begrenzt du das auf bestimmte Skill-Namen. Mit allow_all_skills: true werden wirklich alle verfügbaren Skills maximiert.  
* **Traits & Abneigungen:** traits_all und exclude_all steuern globale Trait-Filter. Der mächtige Schalter "remove_all_dislikes": true entfernt vollautomatisch alle [DISLIKE] Merkmale (Abneigungen gegen Farben, Musik, Hobbys), sodass dein Sim niemals mehr grundlos schlechte Laune bekommt.  
* **Magie & Okkult-Vorteile:** Du kannst Perks (Ruhm & Okkult-Fähigkeiten) über perks_all / perks_occult gezielt freischalten.  
* **Beziehungen im Haushalt:** harmony_friendship, harmony_romance und target_relationship_status setzen Freundschaft, Romantik und Beziehungsstatus für Haushaltsmitglieder. Über remove_negative_relations, remove_negative_relations_household und remove_negative_relations_scope lassen sich außerdem Feindschaften, Groll und Angst-Bits gezielt im gesamten weltweiten Beziehungsnetz entfernen.

### **Okkulte Sims (Vampire, Werwölfe, Magier)**

MakeGod behandelt okkulte Sims völlig automatisch korrekt! In der Konfiguration (unter "motives_to_fill") weiß das Spiel genau, dass ein Vampir keine "Blase" hat, die eingefroren werden muss, sondern "Durst" und "Vampir-Energie".

## **📖 Vollständige Konfigurations-Referenz**

Alle verfübaren Parameter auf einen Blick. Die `_help_set_parameter`-Sektion in der `make_god_config.json` enthält dieselben Beschreibungen direkt im Mod-Ordner.

### Globale Einstellungen

| Schlüssel | Typ | Standard | Bedeutung |
|-----------|-----|----------|-----------| 
| `language` | String | `"de"` | Sprache der eingebauten Hilfetexte (`"de"` oder `"en"`). |
| `debug_log` | Boolean | `false` | `true` = jede Aktion wird detailliert geloggt und im Spiel angezeigt (bei `debug`-Befehl). |
| `log_mode` | String | `"overwrite"` | `"overwrite"` = Log-Datei bei jedem Start neu erstellen; `"append"` = Einträge anhängen. |
| `include_roommates_in_all` | Boolean | `true` | Bei `rmg.all` oder dem "Household"-Button werden offizielle Mitbewohner mit einbezogen. |
| `include_keyholders_in_all` | Boolean | `true` | Bei `rmg.all` werden auch Freunde mit einem Haustürschlüssel berücksichtigt. |
| `dump_blacklist_keywords` | Liste | *(technische Strings)* | Teilstrings, die beim Sim-Dump aus der Statistik-Ausgabe herausgefiltert werden, z. B. `"_high"`, `"caspartid"`. |
| `manual_add_settings` -> `friendship` | Zahl | `100` | Freundschaftswert, der bei `rmg.add` zugewiesen wird (`-999` ignoriert). |
| `manual_add_settings` -> `romance` | Zahl | `-999` | Romantikwert, der bei `rmg.add` zugewiesen wird (`-999` ignoriert). |
| `manual_add_settings` -> `spawn_sim` | Boolean| `false` | `true` = Bei `rmg.add` wird der Sim physisch zu deinem aktiven Sim teleportiert. Löst das MCCC-Flags Problem! |

### Skills & Karriere

| Schlüssel | Typ | Bedeutung |
|-----------|-----|-----------|
| `allow_all_skills` | Boolean | `true` = Alle sicher erkannten Skills maximieren; überschreibt die Filterung durch `allowed_skills`. |
| `max_player_skills` | Boolean | Skills für Sims im gespielten Haushalt maximieren. |
| `max_npc_skills` | Boolean | Skills für NPCs und Townies maximieren. |
| `allowed_skills` | Liste | Namens-Fragmente erlaubter Skills (z. B. `["fitness", "logic"]`). Leer = `fallback_skills` greift. |
| `master_player_careers` | Boolean | Alle aktiven Karrieren promoten, Schule pushen und den aktuellen Bestrebungs-Meilenstein abschließen (gespielte Sims). |
| `master_npc_careers` | Boolean | Wie oben, aber für NPCs. |

Die Config enthält zusätzlich den Abschnitt `"fallback_skills"`, der pro Altersgruppe (`adult`, `child`, `toddler`, `infant`) festlegt, welche Skills maximiert werden, wenn `allowed_skills` leer ist. Für Kinder und Kleinkinder greift immer eine altersgerechte Gruppe – unabhängig vom gewählten Set.

### Luck, Belohnungen & Geld

| Schlüssel | Typ | Bedeutung |
|-----------|-----|-----------|
| `luck` → `value` | Zahl | Glückswert: `-100` (Pech) bis `100` (Glück); `0` = nicht verändern. |
| `satisfaction_points` | Zahl | Zufriedenheitspunkte hinzufügen. `0` = kein Eingriff. |
| `add_funds` | Zahl | Simoleons dem Haushalt hinzufügen. Pro Haushalt nur einmal pro Run ausgeführt. `0` = kein Eingriff. |
| `max_funds` | Zahl | Obergrenze des Haushaltsvermögens nach dem Hinzufügen. |

### Bedürfnisse & Motive

| Schlüssel | Typ | Bedeutung |
|-----------|-----|-----------|
| `fill_motives_mode` | String | `"all"` = EA-Cheat für alle Motive; `"config"` = nur die in `motives_to_fill` genannten; `"none"` = kein Eingriff. |
| `freeze_motives` | Boolean | Setzt den Verfalls-Modifier der in `motives_to_fill` genannten Commodities auf `0`. Der Sim verliert diese Bedürfnisse dann nicht mehr automatisch. |
| `motives_to_fill` | Objekt | Schlüssel: Okkult-Typ (`"human"`, `"vampire"`, `"spellcaster"`, `"werewolf"`, `"mermaid"`). Wert: Liste exakter Commodity-Namen, z. B. `"motive_hunger"` oder `"commodity_motive_vampire_thirst"`. |

### Traits & Perks

| Schlüssel | Typ | Bedeutung |
|-----------|-----|-----------|
| `remove_all_dislikes` | Boolean | `true` = Alle `[DISLIKE]`-Merkmale (Farb-/Musik-Abneigungen) werden automatisch erkannt und entfernt. |
| `exclude_all` | Liste | Traits immer entfernen – gilt für alle Sims dieses Sets. |
| `exclude_sex_male` | Liste | Traits nur bei männlichen Sims entfernen. |
| `exclude_sex_female` | Liste | Traits nur bei weiblichen Sims entfernen. |
| `traits_all` | Liste | Traits immer hinzufügen – gilt für alle Sims dieses Sets. |
| `traits_sex_male` | Liste | Traits nur bei männlichen Sims hinzufügen. |
| `traits_sex_female` | Liste | Traits nur bei weiblichen Sims hinzufügen. |
| `traits_occult` | Objekt | Okkult-Typ → Trait-Liste. Nur der Typ des aktuellen Sims wird berücksichtigt. |
| `perks_all` | Liste | Okkult-/Ruhm-Perks für alle Sims freischalten (über den internen Bucks-Tracker). |
| `perks_occult` | Objekt | Perks nach Okkult-Typ (`"vampire"`, `"spellcaster"`, `"werewolf"`). |

### Beziehungen bereinigen & setzen

| Schlüssel | Typ | Bedeutung |
|-----------|-----|-----------|
| `harmony_friendship` | Zahl | Freundschaftswert für alle Haushaltsmitglieder setzen. `0` = nicht anfassen. |
| `harmony_romance` | Zahl | Romantikwert setzen (nur für Sims ab Teen-Alter). `0` = nicht anfassen. |
| `target_relationship_status` | String | Beziehungsstatus erzwingen. Erlaubt: `"friend"`, `"best_friend"`, `"woohoo_partner"`, `"significant_other"`, `"engaged"`, `"married"`. |
| `remove_negative_relations` | Boolean | `true` = Scannt alle weltweiten Beziehungen. Sims, die ein Bit aus `remove_negative_relations_scope` tragen, werden von **allen** negativen Bits befreit. |
| `remove_negative_relations_household` | Boolean | `true` = Haushaltsmitglieder werden **immer** bereinigt – unabhängig vom Scope. |
| `remove_negative_relations_scope` | Liste | Bit-Namens-Fragmente (z. B. `"friend"`, `"romantic"`, `"married"`), die einem weltweiten Sim Kandidaten-Status verleihen. Als negativ gelten Bits wie `enemy`, `grudge`, `divorced`, `breakup`, `hostile`, `fear`. |
| `harmony_extended_network` | Objekt | Eine erweiterte Matrix, um alters- und geschlechtsabhängig Beziehungen zu Freunden/Familie weltweit aufzubauen. (`enabled`: true/false, `scopes`: [...]) |

**Beispiel:** `"remove_negative_relations": true` mit `"remove_negative_relations_scope": ["friend", "romantic", "married"]`  
→ Alle Freunde, Partner und Haushaltsmitglieder werden von Groll, Feindschaft und Angst befreit. Unbekannte Townies ohne Beziehung bleiben unberührt.

## **🕵️‍♀️ Für Tech-Freaks & Modder: Das Dump-System**

Du willst deinem Set Merkmale aus anderen Mods (wie *WickedWhims* oder *Basemental*) hinzufügen, kennst aber den internen Namen nicht? Die Mod bringt ein mächtiges Auslese-Werkzeug mit!

### **1. Der Reference-Dump (Der Heilige Gral)**

Öffne die Cheat-Konsole im Spiel und tippe:  
rmg.dump reference  
Die Mod durchsucht in Sekundenschnelle die tiefste Code-Ebene der Spiel-Engine und exportiert dir eine saubere Markdown-Datei (.md) in deinen Mod-Ordner.  
Diese Datei enthält eine **vollständige, alphabetische Liste aller Traits, Zauber, Tränke und Perks, die das Spiel gerade geladen hat (inklusive ALLER Mods!)**. Kopiere die Namen einfach heraus und füge sie in deine make_god_config.json ein. Du bist nie wieder auf Wiki-Seiten angewiesen!

### **2. Der Sim- & Haushalts-Dump**

Willst du wissen, welche internen System-Werte ein bestimmter Sim gerade hat?  
Tippe rmg.dump all (für den ganzen Haushalt) oder rmg.dump active.  
Die Mod exportiert ein sauberes Dokument, das dir nicht nur Traits und Skills auflistet, sondern auch verborgene System-Werte (Commodities), okkulte Perks, freigeschaltete Zauber sowie Beziehungs-Werte und verborgene Beziehungs-Bits zu anderen Sims.  
*(Tipp: Über den Punkt dump_blacklist_keywords in der Config filtert die Mod automatisch uninteressanten System-Junk aus diesen Reports heraus).*

### **3. Dump eines bestimmten Sims per ID**

Mit dem Befehl rmg.dump id <SimID> (z. B. rmg.dump id 12345678) kannst du gezielt einen einzelnen Sim exportieren – auch wenn er nicht in deinem aktiven Haushalt ist. Die SimID findest du entweder im Sim-Abschnitt eines vorherigen Dumps (Feld **ID**) oder über rmg.name "Vorname" in der Konsole (gibt bei mehreren Treffern alle IDs aus).

## **❓ Häufige Fragen (FAQ)**

**Das "Make God" Menü taucht im Spiel nicht auf!**

* Vergewissere dich, dass du beide Dateien (.ts4script und .package) in deinem Mods-Ordner hast.  
* Prüfe, ob du "Script-Mods" in den Spieloptionen aktiviert hast.  
* Versteckt sich die Option vielleicht unter "Aktionen" -> "Mehr Auswahl..."?  
* Falls das Menü durch andere Mods blockiert wird, funktionieren die Text-Befehle (rmg.active) über die Konsole trotzdem immer zu 100%!

**Mein Batch-Skript / rmg.name setzt keine Flags bei Townies (z.B. MCCC/WickedWhims)!**

* Drittanbieter-Mods registrieren Trait-Änderungen oft nur, wenn der Sim als "Instanced" (physisch auf dem Grundstück geladen) markiert ist. Befindet sich der Townie "schlafend" in seinem Haus, speichert EA zwar das Trait, aber Mods wie MCCC blockieren das Update in ihrer Datenbank.
* **Die Lösung:** Aktiviere `"spawn_sim": true` in deiner `make_god_config.json` unter `"manual_add_settings"`. Rufst du den NPC in deinem Batch nun zuerst über `rmg.add` auf, teleportiert das Skript ihn sofort physisch zu deinem Sim. Anschließend funktioniert die Zuweisung über `rmg.name` fehlerfrei!

**Wie vergebe ich Schluessel automatisch im Batch?**
* Schluessel sind in der Sims-Engine zickig. Am stabilsten funktioniert es, wenn du den Trait `trait_HasKey` direkt in die `traits_all` oder `traits_sex_female` Liste deines Wunsch-Sets (z.B. Set 3) einträgst. 
* Wenn du dann in deinem Skript `rmg.add id [sim_id]` (Teleport) gefolgt von `rmg.id [sim_id] 3` ausführst (via `rmg.bat setup_npc name "Yuki Behr"`), bekommt sie den Schluessel garantiert.

**Der Button "Haushalt" fehlt bei einigen Sims!**

* Das ist pure Absicht als Schutzmaßnahme. Der Haushalt-Button wird bei NPCs (Townies, Briefträger etc.) absichtlich versteckt, damit du nicht versehentlich Familien, die du nicht spielst, in Götter verwandelst.

**Mein Kleinkind hat nicht die Fähigkeit "Fitness" bekommen!**

* Auch das ist Absicht! Die Mod schützt Kinder und Kleinkinder davor, unpassende Erwachsenen-Skills zu erhalten. Die Mod maximiert stattdessen automatisch ihre altersgerechten Fähigkeiten (wie Motorik oder das Töpfchengehen).

**Ich habe die make_god_config.json zerschossen und das Spiel lädt sie nicht mehr!**

* Keine Panik! Lösche die .json Datei einfach aus deinem Mods-Ordner. Wenn du das Spiel das nächste Mal startest, generiert die Mod automatisch eine frische Standard-Datei.

**Wo finde ich Logs oder Debug-Infos?**

* Die Mod schreibt in make_god_debug.txt im Mods-Ordner.  
* Mit debug_log: true in der Config und dem Konsolen-Zusatz debug bekommst du deutlich mehr Details.

**Ich bin unsicher beim Bearbeiten der Config. Was ist der sichere Weg?**

* Vor dem Bearbeiten kurz eine Kopie der Datei machen (z.B. make_god_config_backup.json).  
* Danach nur kleine Änderungen machen und testen.  
* Wenn etwas kaputt ist: make_god_config.json löschen, Spiel neu starten, neue Standard-Datei erzeugen lassen.

**Perks oder Zauber werden nicht freigeschaltet, obwohl die Namen korrekt wirken!**

* Die Namen müssen exakt mit dem internen `__name__`-Attribut der Engine übereinstimmen – nicht mit dem Anzeigenamen im Spiel.
* Nutze rmg.dump reference, um die korrekten Namen direkt aus dem laufenden Spiel zu exportieren.
* Okkult-Perks (Vampire, Magier, Werwölfe) können nur freigeschaltet werden, wenn der Sim den entsprechenden Okkult-Typ bereits hat.
* **Wichtig für gespielte Sims:** Das Spiel initialisiert den internen Perk-Tracker oft erst, wenn das entsprechende Menü angesehen wird. Öffne das Vorteil-/Perk-Fenster deines Sims (z. B. Vampirkräfte oder Magier-Vorteile) mindestens einmal manuell im Spiel, bevor du MakeGod ausführst, damit das Skript die Perks erfolgreich eintragen kann.

**rmg.name findet den Sim nicht!**

* Gib den Vor- oder Nachnamen exakt ein (Groß-/Kleinschreibung wird ignoriert).
* Bei mehreren Treffern gibt die Mod alle Kandidaten mit ID in der Konsole aus – verwende dann rmg.id <SimID>.
* Sims, die nicht im Spielspeicher geladen sind (z. B. Townies aus weit entfernten Welten), werden möglicherweise nicht gefunden.

**Ich habe rmg.add benutzt, aber die Beziehungswerte stimmen nicht / ändern sich nicht!**

* *Wichtig:* Sims, die aktuell nicht aktiv im Level geladen sind ("Hidden"), können einige Beziehungs-Updates teilweise ignorieren oder das Update schlägt stumm fehl. Nutze auch hier `"spawn_sim": true` in der Config, um den Sim für das Update zuverlässig zu dir zu rufen.

**Beziehungen oder Geld werden nach einem Spielupdate zurückgesetzt!**

* Das ist kein Mod-Bug – EAs "Relationship Culling" löscht ältere Freundschaften bei bestimmten Ereignissen automatisch.
* Abhilfe: MC Command Center (MCCC) installieren und die No-Cull-Flags aktivieren. Diese Flags lassen sich auch direkt über MakeGod verteilen, z. B. Deaderpool_MCCC_Trait_FlagNoRelCull in traits_all.

**Karrieren werden nicht gepusht!**

* Karrieren können nur befördert werden, wenn der Sim bereits in einer Karriere ist. MakeGod weist keine neue Karriere zu – nur vorhandene werden gepusht.
* Schule (gradeschool / highschool) wird für Kinder und Teens automatisch erkannt und braucht nicht konfiguriert zu werden.

## ⚠️ Wichtige Hinweise zur Performance (Freezes & Lags)

Wenn du das Kommando `rmg.all` oder Beziehungs-Updates bei Sims mit sehr vielen Bekanntschaften ausführst, kann es passieren, dass **das Spiel für einige Sekunden (bis hin zu einer Minute) komplett einfriert**.

**Keine Panik, das Spiel ist nicht abgestürzt!**
Dieses Verhalten ist eine technische Limitierung der *Die Sims 4*-Engine. 
Das Skript arbeitet im Hintergrund hochkomplexe Matrizen ab: Es scannt das gesamte erweiterte soziale Netzwerk deines Sims, bereinigt versteckte negative Tracker, ignoriert Kompatibilitäts-Konflikte und passt Freundschafts- sowie Romantikwerte nach Alter und Geschlecht an. Da die Engine diese Berechnungen auf dem sogenannten "Main-Thread" (Hauptprozess) erzwingt, pausiert die Bildausgabe, bis das Skript fertig ist.

**Was du tun solltest:**
1. **Abwarten:** Lass das Spiel einfach rechnen. Wenn du das Ingame-Cheatfenster (Strg+Shift+C) geöffnet hast, kannst du live mitlesen, welchen Sim das Skript gerade bearbeitet.
2. **Verzögerte Anzeige im Spiel:** Wenn das Skript fertig ist und das Spiel weiterläuft, **kann es einen kurzen Moment dauern, bis die neuen Beziehungswerte im UI (Beziehungs-Panel) sichtbar sind.** Die Engine aktualisiert die visuelle Anzeige der Freundschaften etwas verzögert im Hintergrund.

**Tipp:** Wenn du die Beziehungs-Funktionen (wie `harmony_extended_network`) in deiner Konfiguration deaktivierst oder auf `-999` setzt, läuft das Skript deutlich schneller durch.

*Viel Spaß beim Erschaffen deiner perfekten Sims-Welt!*