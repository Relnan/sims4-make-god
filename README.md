# Sims 4 Mod: Make God

## 🇩🇪 Deutsch

### Was macht diese Mod?
Stell dir vor, du hast einen magischen Zauberstab für deine Sims. Mit nur einem einzigen Befehl kannst du deinen gesamten Haushalt (oder auch fremde Sims auf der Straße) in absolute "Götter" verwandeln. 
Dieses Skript optimiert deine Sims automatisch basierend auf einer Einstellungsdatei (`make_god_config.json`). 

**Was genau passiert?**
* **Perfektion:** Schlechte Eigenschaften werden gelöscht, gute hinzugefügt.
* **Bedürfnisse:** Die Bedürfnisse deiner Sims werden eingefroren (niemand muss mehr aufs Klo!). **Hinweis:** Dies passiert basierend auf deiner Einstellungsdatei. Standardmäßig ist es für Menschen und Okkulte Sims (wie Vampir-Durst oder Geister-Ausdauer) aktiviert, lässt sich aber pro Spezies abschalten.
* **Liebe & Freundschaft:** Alle im gespielten Haushalt lieben sich plötzlich und gehen eine feste Beziehung ("Romance") ein. Das Skript verhindert hier automatisch Ehen innerhalb des Haushalts, um Spielabstürze durch Mehrfachehen zu vermeiden. Fremde NPCs können jedoch sofort geheiratet werden!
* **Reichtum:** Das Haushaltskonto erhält eine massive (in der Datei konfigurierbare) Finanzspritze und Zufriedenheitspunkte werden vergeben.
* **Fähigkeiten & Karriere:** Alle Fähigkeiten werden auf das Maximum gesetzt und Karrieren sowie Bestreben werden sofort abgeschlossen.

### Installation
1. Lade die Datei `make_god.ts4script` herunter und kopiere sie in deinen Sims 4 `Mods`-Ordner.
2. Kopiere die Einstellungsdatei `make_god_config.json` in denselben Ordner.
3. Starte das Spiel, gehe in die Spieloptionen unter "Weiteres" und setze ein Häkchen bei **Script-Mods erlaubt**. Starte das Spiel danach einmal neu.

### So benutzt du die Mod (Die Befehle)
Öffne im Spiel die Cheat-Konsole (Drücke `Strg + Shift + C` auf der Tastatur) und tippe `testingcheats true` ein. Danach kannst du diese Befehle nutzen:

* **`make_god`**
  Der absolute Standard-Befehl. Er verwandelt **deinen gesamten, aktuell gespielten Haushalt** in perfekte Sims. (Tipp: Wenn du die `make_god_config.json` während des Spielens bearbeitest und speicherst, lädt dieser Befehl die neuen Einstellungen völlig automatisch!)
* **`make_god active`**
  Verwandelt **nur den Sim**, den du gerade angeklickt/ausgewählt hast.
* **`make_god name Vorname Nachname`** Du siehst einen Sim auf der Straße und willst ihn optimieren? Tippe einfach seinen Namen ein! (Beispiel: `make_god name Bella Grusel`). Der Sim wird sofort perfektioniert und baut eine volle Beziehung zu deinem gespielten Sim auf.
* **`make_god id 1234567890`** Gleiches Prinzip wie beim Namen, nur mit der genauen Sim-ID, falls du diese kennst.
* **`make_god_dump`**
  Ein Werkzeug für Neugierige. Wähle einen Sim aus und tippe diesen Befehl. Die Mod erstellt in deinem Mods-Ordner eine Textdatei, die dir genau anzeigt, welche versteckten Merkmale (Traits) und welchen "Okkult-Typ" das Spiel bei diesem Sim sieht.
* **Der Debug-Modus:**
  Wenn du wissen willst, was das Skript im Hintergrund genau macht, hänge einfach das Wort `debug` an deinen Befehl an (z. B. `make_god debug` oder `make_god name Bella Grusel debug`). Die Konsole zeigt dir dann jeden einzelnen Schritt an!

### Die Einstellungsdatei (`make_god_config.json`) anpassen
Keine Angst vor dieser Datei! Du kannst sie einfach mit dem Windows-Editor (Notepad) öffnen. Hier kannst du die Regeln für deine "Götter" ändern.
Ein paar einfache Beispiele:
* `"harmony_partnership": "marriage"` -> Ändere "marriage" (Hochzeit) zu "romance" (Feste Beziehung) oder "none" (Nichts), wenn fremde Sims nicht sofort heiraten sollen.
* `"add_funds": 1000000` -> Bestimmt, wie viele Simoleons das Haushaltskonto bei Ausführung des Befehls dazu bekommt.
* `"occult_settings"` -> Hier kannst du für Vampire, Meerjungfrauen, Feen etc. einstellen, ob ihre Spezial-Bedürfnisse eingefroren werden sollen (`"freeze_motives": true` oder `false`).

---

## 🧪 So testest du die Mod (Tutorial)
Wenn du sofort sehen willst, wie die Mod funktioniert, kannst du unser fertiges Test-Szenario ausprobieren. 

**Tipp:** Du musst die Sims nicht selbst erstellen! Suche in der Sims 4 Galerie einfach nach dem Haushalt **make_god Test** von der EA-ID **Relnan** und platziere ihn auf einem leeren Grundstück.

### Der Standard-Test
Dieser Test-Haushalt enthält 3 Sims:
1. **Arthur Anti-Gott:** Er ist böse, faul und ein Hitzkopf.
2. **Bella Basic:** Sie ist tollpatschig und düster. Gib ihr am besten am Handy vorher noch schnell irgendeinen Job (z.B. Tellerwäscherin).
3. **Chris Chaos:** Völlig zufällig generiert.

**Probier es aus:**
1. Wähle **Bella** aus.
2. Öffne die Konsole und tippe `make_god active debug`.
3. **Beobachte die Magie:** Die Konsole zeigt dir, wie Bella plötzlich ihre Karriere meistert, negative Eigenschaften verliert, massig neue Fähigkeiten lernt und zur perfekten Simin wird.
4. Tippe nun einfach `make_god` ein. Nun werden auch Arthur und Chris zu Göttern und alle drei haben plötzlich eine perfekte Liebes- und Freundschaftsbeziehung zueinander!

### Der Okkult-Test (Wenn du Erweiterungen hast)
Du besitzt Packs wie *Vampire*, *Werwölfe*, *Reich der Magie* oder *Life & Death*? Das Skript ist darauf vorbereitet!
1. Füge dem Haushalt einfach einen Okkulten Sim hinzu (z. B. einen Geist aus dem Life & Death Pack, einen Vampir oder einen Werwolf).
2. Wähle den Sim aus und tippe `make_god active`.
3. **Das Ergebnis:** Das Skript erkennt automatisch die "Spezies" deines Sims. Es friert die richtigen Spezial-Bedürfnisse ein (z. B. die Geister-Ausdauer oder den Vampir-Durst) und verteilt passende Belohnungsmerkmale, ohne dass das Spiel Fehler wirft.

***

# Sims 4 Mod: Make God

## 🇬🇧 English

### What does this mod do?
Imagine having a magic wand for your Sims. With just one simple command, you can turn your entire household (or even random Sims on the street) into absolute "Gods".
This script automatically optimizes your Sims based on a simple settings file (`make_god_config.json`).

**What exactly happens?**
* **Perfection:** Bad traits are deleted, and amazing ones are added.
* **Needs:** Your Sims' needs are frozen completely (no more bathroom breaks!). **Note:** This depends on your settings file. By default, it is enabled for humans and Occult Sims (like freezing Vampire Thirst or Ghost Stamina), but it can be toggled per species.
* **Love & Friendship:** Everyone in the played household will instantly love each other and enter a committed relationship ("Romance"). The script automatically prevents marriages *inside* the household to protect your game from polygamy crashes. However, foreign NPCs can be married instantly!
* **Wealth:** Your household receives a massive (configurable) injection of funds, and satisfaction points are granted.
* **Skills & Career:** All skills are instantly maxed out, careers are promoted to the top, and aspirations are completed.

### Installation
1. Download the file `make_god.ts4script` and place it in your Sims 4 `Mods` folder.
2. Place the settings file `make_god_config.json` in the exact same folder.
3. Start the game, go to your Game Options under "Other", and check the box for **Script Mods Allowed**. Restart your game once.

### How to use the Mod (The Commands)
Open the cheat console in-game (Press `Ctrl + Shift + C` on your keyboard) and type `testingcheats true`. After that, you can use these commands:

* **`make_god`**
  The easiest command. It turns your **entire currently played household** into perfect Sims. (Tip: If you edit and save your `make_god_config.json` while playing, this command will automatically load the new settings!)
* **`make_god active`**
  Transforms **only the Sim** you currently have selected.
* **`make_god name Firstname Lastname`** See a random Sim on the street and want to optimize them? Just type their name! (Example: `make_god name Bella Goth`). They will instantly become perfect and build a full relationship with your active Sim.
* **`make_god id 1234567890`** Same principle as the name command, but uses the exact Sim ID if you know it.
* **`make_god_dump`**
  A tool for the curious. Select a Sim and type this command. The mod will create a text file in your Mods folder showing exactly which hidden traits and "Occult Type" the game detects for this Sim.
* **The Debug Mode:**
  If you want to see exactly what the script is doing behind the scenes, just add the word `debug` to your command (e.g., `make_god debug` or `make_god name Bella Goth debug`). The console will tell you every single step it takes!

### Tweaking the Settings File (`make_god_config.json`)
Don't be afraid of this file! You can open it easily with a simple text editor like Notepad. Here you can change the rules for your "Gods".
Some easy examples:
* `"harmony_partnership": "marriage"` -> Change "marriage" to "romance" (boyfriend/girlfriend) or "none" if you don't want foreign Sims to marry instantly.
* `"add_funds": 1000000` -> Determines how many Simoleons are added to the household account when the command is run.
* `"occult_settings"` -> Here you can configure if Vampires, Mermaids, Ghosts, etc., should have their special needs frozen (`"freeze_motives": true` or `false`).

---

## 🧪 How to test the Mod (Tutorial)
If you want to see how the mod works immediately, you can play our ready-made test scenario. 

**Tip:** You don't have to create the Sims yourself! Just search the Sims 4 Gallery for the household name **make_god Test** by the EA-ID **Relnan** and place them on an empty lot.

### The Standard Test
This test household contains 3 Sims:
1. **Arthur Anti-God:** He is evil, lazy, and a hothead.
2. **Bella Basic:** She is clumsy and gloomy. (Give her a quick job on her phone before starting, like dishwasher).
3. **Chris Chaos:** Completely randomly generated.

**Try it out:**
1. Select **Bella**.
2. Open the console and type `make_god active debug`.
3. **Watch the magic:** The console will show you exactly how Bella instantly masters her career, loses negative traits, gains max skills, and becomes a perfect Sim.
4. Now simply type `make_god`. Arthur and Chris will also become Gods, and all three will suddenly have a perfect, flawless romantic and friendly relationship with each other!

### The Occult Test (If you own Expansions)
Do you own packs like *Vampires*, *Werewolves*, *Realm of Magic*, or *Life & Death*? The script is ready for them!
1. Just add an Occult Sim to the household (e.g., a Ghost from the Life & Death pack, a Vampire, or a Werewolf).
2. Select the Sim and type `make_god active`.
3. **The Result:** The script automatically detects the "species" of your Sim. It safely freezes the correct special needs (like Ghost Stamina or Vampire Thirst) and hands out fitting reward traits without causing any game errors.