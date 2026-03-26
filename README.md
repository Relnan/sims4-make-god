# **🌟 MakeGod Mod für Die Sims 4**

Willkommen bei **MakeGod**! Dies ist nicht einfach nur eine weitere Cheat-Mod - es ist ein extrem mächtiges, blitzschnelles und hochgradig anpassbares Werkzeug, um das Leben deiner Sims mit nur einem einzigen Klick komplett zu perfektionieren (oder zu ruinieren, je nachdem, was du in der Konfiguration einstellst!).
Egal, ob du einen unsterblichen Super-Vampir, ein absolutes Wunderkind oder einfach nur den perfekten Nachbarn erschaffen willst: MakeGod erledigt in einem Bruchteil einer Sekunde das, wofür du sonst stundenlang Cheats eintippen müsstest.

Der Mod ist ein Hobby-Projekt zum Kennenlernen der Modding-Funktionalität, und ich übernehme keine Gewähr auf Vollständigkeit.

Die Menü-Integration ist im Mod enthalten, kann aber je nach Spielversion, Package-Stand oder Load Order Probleme machen. Wenn das Menü nicht erscheint, nutze einfach die Cheat-Konsole.

** INFO: Der Mod wurde fast ausschließlich mit Unterstützung von KI (Gemini) erstellt **

## **📥 Installation**

Die Installation ist super einfach und erfordert nur zwei Schritte:

1. Lade dir die neueste Version von MakeGod herunter. Du erhältst zwei Dateien:
   * make_god.ts4script (Die Logik und das Gehirn der Mod)
   * Relnan_MakeGod_UI.package (Das Ingame-Menü)
2. Kopiere **beide Dateien** in deinen Die Sims 4 Mods-Ordner.
   * Standard-Pfad: Dokumente\Electronic Arts\Die Sims 4\Mods
3. **WICHTIG:** Gehe im Spiel in die Optionen unter "Weiteres" und stelle sicher, dass **"Benutzerdefinierte Inhalte und Mods aktivieren"** sowie **"Script-Mods erlaubt"** mit einem Häkchen versehen sind!

## **🚀 Schnellstart für Einsteiger (2 Minuten)**

Wenn du nur kopieren und einfache Dateien bearbeiten kannst, reicht das hier völlig:

1. Installiere die Mod wie oben beschrieben.
2. Starte das Spiel und lade einen Haushalt.
3. Öffne die Cheat-Konsole mit `Strg + Shift + C`.
4. Gib ein: `rmg.active`
5. Fertig. Dein aktuell ausgewählter Sim bekommt das Standard-Setup.

Wenn du den ganzen Haushalt auf einmal willst:

1. Öffne die Konsole mit `Strg + Shift + C`.
2. Gib ein: `rmg.all`

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

Drücke im Spiel Strg + Shift + C, um die Konsole zu öffnen. Die Mod bringt eigene Befehle mit, die du eintippen kannst:

* `rmg` - Zeigt die integrierte Hilfe in der Cheat-Konsole.
* `rmg.all [Set_ID|auto|option_xx] [debug]` - Wendet MakeGod auf den ganzen aktiven Haushalt an.
* `rmg.active [Set_ID|auto|option_xx] [debug]` - Wendet MakeGod auf den aktuell ausgewählten Sim an.
* `rmg.id <SimID> [Set_ID|auto|option_xx] [debug]` - Wendet MakeGod auf einen Sim über seine interne ID an.
* `rmg.name "Bella Grusel" [Set_ID|auto|option_xx] [debug]` - Sucht nach einem Sim per Name.
* `rmg auto` - Kurzbefehl für `rmg all auto`.
* `rmg.dump` oder `rmg.dump active` - Dump für den aktiven Sim.
* `rmg.dump all` - Dump für den kompletten Haushalt.
* `rmg.dump id <SimID>` - Dump für einen bestimmten Sim per ID.
* Für den Alltag reichen normalerweise `rmg.active` und `rmg.all`.
* Du kannst Optionen flexibel schreiben: `option_12`, `option12` oder `opt12` sind gleichwertig.
* Wenn ein Name mehrfach gefunden wird, bricht der Befehl mit einer klaren Fehlermeldung ab und zeigt eine Trefferliste mit Sim-IDs in der Konsole. Nutze dann `rmg.id`.
* *Tipp:* Mit `debug` bekommst du zusätzlich ausführlichere Ausgaben und Log-Einträge, z.B. `rmg.active 0 debug`.

## **⚙️ Wie passe ich die Mod an? (Die Config-Datei)**

Das wahre Herzstück dieser Mod ist die **Konfigurationsdatei**.
Je nach Release kann bereits eine `make_god_config.json` mitgeliefert werden. Falls sie im Mods-Ordner fehlt, erzeugt die Mod beim Start automatisch eine Standard-Datei. Du kannst sie mit jedem Texteditor (wie dem normalen Windows Editor oder Notepad++) öffnen.

### **Einsteiger-Modus: Nur 3 Dinge ändern**

Wenn du möglichst wenig anfassen willst, ändere nur diese Punkte in `make_god_config.json`:

1. Unter `auto_profiles` festlegen, welches Set bei Option 1 / 2 / 3 verwendet wird.
2. Im gewünschten Set (`"0"`, `"1"`, `"10"` ...) nur `traits_all` anpassen.
3. Optional `add_funds` ändern, wenn du mehr oder weniger Geld geben willst.

Alles andere kannst du erstmal lassen.

### **Was sind "Sets"?**

In der Datei findest du einen Bereich namens "sets". Ein Set ist quasi ein Bauplan für einen Sim.
Ein Set kann unter anderem Traits hinzufügen oder entfernen, Skills maximieren, Karrieren pushen, Zufriedenheitspunkte vergeben, Bedürfnisse einfrieren, Beziehungen innerhalb des Haushalts setzen und Haushaltsgeld anpassen.
Standardmäßig gibt es z.B.:

* **Set 0 (Ultimate God):** Der Sim kriegt alle Fähigkeiten auf Maximum, alle Karrieren auf Stufe 10, maximale Zufriedenheitspunkte, Millionen von Simoleons, negative Merkmale (wie "Böse") werden gelöscht und seine Bedürfnisse frieren für immer auf Maximum ein.
* **Set 10 (Blessed Child):** Das perfekte Kinder-Profil. Karrieren werden ignoriert, aber die Kinder-Fähigkeiten (Motorik, Kreativität) werden gemaxt.

### **Was sind "Auto Profile"?**

Die Mod ist schlau! Wenn du im Spiel auf "Option 1" klickst, bekommt nicht jeder Sim einfach stur "Set 0" aufgedrückt.
In der Config unter "auto_profiles" ist geregelt, wer welchen Bauplan bekommt.

* *Beispiel:* Du hast Option 1 geklickt. Die Mod sieht: "Aha, das ist ein spielbarer Erwachsener, er bekommt **Set 0**." - "Oh, das daneben ist ein Kind, es bekommt automatisch **Set 10**."
  Du kannst die Zuweisungen für NPCs, Männer, Frauen und Kinder hier völlig frei anpassen!

### **So baust du eigene Sets:**

Die Datei enthält ein eingebautes Lexikon (_help_set_parameter). Hier ist kurz erklärt, wie die wichtigsten Parameter funktionieren:

* **Fähigkeiten (Skills):** `max_player_skills` und `max_npc_skills` steuern, ob Skills überhaupt maximiert werden. Mit `allowed_skills` begrenzt du das auf bestimmte Skill-Namen (z.B. ["fitness", "charisma"]). Lässt du `allowed_skills` leer, nutzt die Mod altersabhängige `fallback_skills`. Mit `allow_all_skills: true` werden wirklich alle verfügbaren Skills maximiert.
* **Traits hinzufügen/entfernen:** `traits_all`, `traits_sex_male`, `traits_sex_female`, `exclude_all`, `exclude_sex_male` und `exclude_sex_female` steuern globale und geschlechtsspezifische Trait-Filter.
* **Beziehungen im Haushalt:** `harmony_friendship`, `harmony_romance` und `target_relationship_status` setzen Freundschaft, Romantik und Beziehungsstatus für Mitglieder desselben Haushalts.
* **System / Logging:** `debug_log` und `log_mode` steuern die Datei `make_god_debug.txt`. `language` ist aktuell nur als Platzhalter vorbereitet.

### **Okkulte Sims (Vampire, Werwölfe, Magier)**

MakeGod behandelt okkulte Sims völlig automatisch korrekt! In der Konfiguration (unter "motives_to_freeze") weiß das Spiel genau, dass ein Vampir keine "Blase" hat, die eingefroren werden muss, sondern "Durst" und "Vampir-Energie".

## **🕵️‍♀️ Optional: Dump-Funktion (Wie finde ich die richtigen Namen?)**

Wenn du ein bestimmtes Merkmal oder einen neuen Skill zu deinem Set hinzufügen willst, brauchst du den exakten internen Namen von Electronic Arts oder einem anderen Mod (z.B. `trait_GreatKisser`). Aber wie findet man den heraus?
**Die Lösung:** Erstelle den Sim einfach einmal normal im Spiel und gib ihm das Merkmal. Öffne dann die Cheat-Konsole (Strg + Shift + C) und tippe ein:

rmg.dump

Die Mod erstellt dann **drei** Textdateien pro Sim in deinem Mods-Ordner:

* `rmg_dump_stats_...txt` für Statistiken und Bedürfnisse
* `rmg_dump_traits_...txt` für Traits
* `rmg_dump_skills_...txt` für alle gefundenen Skills inklusive aktuellem Level

Diese Namen kannst du direkt in deine `make_god_config.json` übernehmen.
*(Tipp: Mit `rmg.dump all` kannst du den kompletten Haushalt auf einmal durchleuchten, mit `rmg.dump id <SimID>` einen ganz bestimmten Sim.)*

## **❓ Häufige Fragen (FAQ)**

**Das "Make God" Menü taucht im Spiel nicht auf!**

* Vergewissere dich, dass du beide Dateien (.ts4script und .package) in deinem Mods-Ordner hast.
* Prüfe, ob du "Script-Mods" in den Spieloptionen aktiviert hast.
* Versteckt sich die Option vielleicht unter "Aktionen" -> "Mehr Auswahl..."?

**Ich habe die make_god_config.json zerschossen und das Spiel lädt sie nicht mehr!**

* Keine Panik! Lösche die `.json` Datei einfach aus deinem Mods-Ordner. Wenn du das Spiel das nächste Mal startest, generiert die Mod automatisch eine frische Standard-Datei.

**Wo finde ich Logs oder Debug-Infos?**

* Die Mod schreibt in `make_god_debug.txt` im Mods-Ordner.
* Mit `debug_log: true` in der Config und dem Konsolen-Zusatz `debug` bekommst du deutlich mehr Details.

**Ich bin unsicher beim Bearbeiten der Config. Was ist der sichere Weg?**

* Vor dem Bearbeiten kurz eine Kopie der Datei machen (z.B. `make_god_config_backup.json`).
* Danach nur kleine Änderungen machen und testen.
* Wenn etwas kaputt ist: `make_god_config.json` löschen, Spiel neu starten, neue Standard-Datei erzeugen lassen.

**Der Button "Haushalt" fehlt bei einigen Sims!**

* Das ist pure Absicht als Schutzmaßnahme. Der Haushalt-Button wird bei NPCs (Townies, Briefträger etc.) absichtlich versteckt, damit du nicht versehentlich Familien, die du nicht spielst, in Götter verwandelst.

**Mein Kleinkind hat nicht die Fähigkeit "Fitness" bekommen!**

* Auch das ist Absicht! Die Mod schützt Kinder und Kleinkinder davor, unpassende Erwachsenen-Skills zu erhalten. Die Mod maximiert stattdessen automatisch ihre altersgerechten Fähigkeiten (wie Motorik oder das Töpfchengehen).

*Viel Spaß beim Erschaffen deiner perfekten Sims-Welt!*

---

# MakeGod Mod for The Sims 4

Welcome to MakeGod! This is not just another cheat mod. It is an extremely powerful, fast, and highly customizable tool that can completely perfect your Sims' lives with a single click, or ruin them, depending on how you configure it.
Whether you want to create an immortal super vampire, an absolute prodigy, or simply the perfect neighbor, MakeGod does in a fraction of a second what would otherwise take hours of typing cheats manually.

This mod is a hobby project created to learn more about modding functionality, and I do not guarantee completeness.

The menu integration is included in the mod, but depending on game version, package state, or load order it may not always show up reliably. If the menu is missing, use the cheat console instead.

INFO: This mod was created almost entirely with AI assistance (Gemini).

## Installation

Installation is simple and only requires two steps:

1. Download the latest version of MakeGod. You will get two files:
   - make_god.ts4script (the logic and brain of the mod)
   - Relnan_MakeGod_UI.package (the in-game menu)
2. Copy both files into your The Sims 4 Mods folder.
   - Default path: Documents\Electronic Arts\The Sims 4\Mods
3. IMPORTANT: In the game options under "Other", make sure that both "Enable Custom Content and Mods" and "Script Mods Allowed" are checked.

## Beginner Quick Start (2 minutes)

If you only know how to copy files and edit simple text files, this is enough:

1. Install the mod as described above.
2. Start the game and load a household.
3. Open the cheat console with `Ctrl + Shift + C`.
4. Type: `rmg.active`
5. Done. Your currently selected Sim gets the default setup.

If you want to apply it to the whole household:

1. Open the console with `Ctrl + Shift + C`.
2. Type: `rmg.all`

## How do I use the mod in game?

Once you are in Live Mode, you have two ways to use the mod: through the convenient click menu or via text commands.

### Method 1: The click menu (recommended)

1. Click on any Sim, whether it is your own Sim or an NPC walking around.
2. Open the Actions menu.
3. You will find these new options there:
   - Make God - Sim Option 1: Applies your "Profile 1" (default: absolute perfection) to that Sim.
   - Make God - Sim Option 2: Applies your "Profile 2" to that Sim.
   - Make God - Sim Option 3: Applies your "Profile 3" to that Sim.
   - Make God - Household: This button only appears for Sims in your active household. It applies MakeGod to the entire household.

### Method 2: The cheat console (simple and reliable)

Press Ctrl + Shift + C in game to open the cheat console. The mod provides its own commands:

- `rmg` - Shows the built-in help in the cheat console.
- `rmg.all [Set_ID|auto|option_xx] [debug]` - Applies MakeGod to the entire active household.
- `rmg.active [Set_ID|auto|option_xx] [debug]` - Applies MakeGod to the currently selected Sim.
- `rmg.id <SimID> [Set_ID|auto|option_xx] [debug]` - Applies MakeGod to a Sim by internal ID.
- `rmg.name "Bella Goth" [Set_ID|auto|option_xx] [debug]` - Searches a Sim by name.
- `rmg auto` - Shortcut for `rmg all auto`.
- `rmg.dump` or `rmg.dump active` - Creates a dump for the active Sim.
- `rmg.dump all` - Creates a dump for the whole household.
- `rmg.dump id <SimID>` - Creates a dump for one specific Sim by ID.
- For normal use, `rmg.active` and `rmg.all` are usually enough.
- You can write options flexibly: `option_12`, `option12`, or `opt12` all work the same.
- If a name matches multiple Sims, the command aborts with a clear error message and prints a match list with Sim IDs in the console. In that case, use `rmg.id`.
- Tip: Add `debug` for more detailed console and log output, for example `rmg.active 0 debug`.

## How do I customize the mod? The config file

The real heart of this mod is the configuration file.
Depending on the release, a `make_god_config.json` may already be shipped with the mod. If it is missing from your Mods folder, the mod automatically creates a default file on startup. You can open it with any text editor such as Notepad or Notepad++.

### Beginner mode: only change 3 things

If you want to keep it simple, only change these fields in `make_god_config.json`:

1. In `auto_profiles`, select which set each button option uses.
2. In the set you use (`"0"`, `"1"`, `"10"` ...), only edit `traits_all`.
3. Optionally adjust `add_funds` if you want more or less money.

You can leave everything else untouched at first.

### What are sets?

In the file you will find a section called "sets". A set is essentially a blueprint for a Sim.
Among other things, a set can add or remove traits, max skills, push careers, grant satisfaction points, freeze motives, change household relationships, and adjust household funds.
By default there are, for example:

- Set 0 (Ultimate God): The Sim gets all skills maxed out, all careers at level 10, maximum satisfaction points, millions of Simoleons, negative traits such as "Evil" are removed, and motives are frozen at maximum forever.
- Set 10 (Blessed Child): The perfect child profile. Careers are ignored, but child-specific skills such as Motor and Creativity are maxed.

### What are auto profiles?

The mod is smart. If you click "Option 1" in game, not every Sim just gets "Set 0" forced onto them.
In the config under "auto_profiles", the rules determine which blueprint is assigned to which Sim.

- Example: You click Option 1. The mod sees: "This is a playable adult, so assign Set 0." Then it sees: "That Sim is a child, so assign Set 10 automatically."
  You can freely customize these assignments for NPCs, men, women, and children.

### Building your own sets

The file contains a built-in reference section called _help_set_parameter. Here is a short explanation of the most important parameters:

- Skills: `max_player_skills` and `max_npc_skills` determine whether skills are maxed at all. `allowed_skills` limits that to specific skill names, for example ["fitness", "charisma"]. If `allowed_skills` is empty, the mod uses age-based `fallback_skills`. If you set `allow_all_skills: true`, all available skills will be maxed.
- Trait include/exclude filters: `traits_all`, `traits_sex_male`, `traits_sex_female`, `exclude_all`, `exclude_sex_male`, and `exclude_sex_female` control global and gender-specific trait handling.
- Household relationships: `harmony_friendship`, `harmony_romance`, and `target_relationship_status` set friendship, romance, and relationship status for Sims within the same household.
- System and logging: `debug_log` and `log_mode` control the `make_god_debug.txt` log file. `language` currently exists as a placeholder.

### Occult Sims: vampires, werewolves, spellcasters

MakeGod automatically handles occult Sims correctly. In the configuration, especially under "motives_to_freeze", the game knows that a vampire does not have "Bladder" to freeze, but instead has "Thirst" and "Vampire Energy".

## Optional: The dump feature

If you want to add a specific trait or a new skill to your set, you need the exact internal Electronic Arts or modded name, for example `trait_GreatKisser`. How do you find that?
The solution is simple: create the Sim normally in game and give them the trait first. Then open the cheat console with Ctrl + Shift + C and type:

rmg.dump

The mod will then create **three** text files per Sim in your Mods folder:

- `rmg_dump_stats_...txt` for statistics and motives
- `rmg_dump_traits_...txt` for traits
- `rmg_dump_skills_...txt` for all detected skills including the current level

You can copy those names directly into your `make_god_config.json`.

Tip: Use `rmg.dump all` for the entire household or `rmg.dump id <SimID>` for one specific Sim.

## FAQ

### The "Make God" menu does not appear in game

- Make sure both files, the .ts4script and the .package, are in your Mods folder.
- Check whether script mods are enabled in the game options.
- The option may be hidden under Actions -> More Choices.

### I broke make_god_config.json and the game no longer loads it

- No problem. Delete the `.json` file from your Mods folder. The next time you start the game, the mod will automatically generate a fresh default file.

### Where can I find logs or debug information

- The mod writes to `make_god_debug.txt` in your Mods folder.
- Set `debug_log: true` in the config and use the `debug` console flag for much more detailed output.

### I am not confident editing config files. What is the safe path?

- Make a quick copy first (for example `make_god_config_backup.json`).
- Change only a few lines at a time and test.
- If something breaks: delete `make_god_config.json`, restart the game, and let the mod generate a fresh default file.

### The "Household" button is missing for some Sims

- This is intentional as a safety measure. The household button is hidden for NPCs such as townies or service Sims so you do not accidentally turn unplayed families into gods.

### My toddler did not get the "Fitness" skill

- This is also intentional. The mod prevents children and toddlers from receiving unsuitable adult skills. Instead, it automatically maximizes age-appropriate abilities such as Motor or Potty.

Have fun creating your perfect Sims world.
