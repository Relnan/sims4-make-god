# Sims 4 Mod: Make God (Gott-Modus)

Dieses Skript ist ein modulares Werkzeug, um Sims in "Götter" zu verwandeln. Es maximiert Fähigkeiten, optimiert Traits (inkl. Mod-Support), pusht Karrieren und Beziehungen und verwaltet das Haushaltskonto – alles dynamisch konfigurierbar durch Profile (Sets)!

## 🚀 Features
* **Modulare Befehle:** Führe nur das aus, was du brauchst.
* **Auto-Profile:** Das Skript ordnet anhand von Geschlecht und Status (NPC/Playable) automatisch das richtige Profil (Set) zu.
* **JSON-Konfiguration:** Alle Werte, Traits und Exclude-Listen können während das Spiel läuft geändert werden.
* **Trait-Cleaner:** Entfernt automatisch nervige oder negative EA-Traits.
* **Debug-Logging:** Optionale `.txt` Log-Datei im Mods-Ordner für detailliertes Troubleshooting.

## 🛠️ Installation
1. Kopiere die Datei `make_god.ts4script` in deinen Sims 4 `Mods`-Ordner.
2. Kopiere die Datei `make_god_config.json` in den `Mods`-Ordner (oder lass das Skript beim ersten Start eine Vorlage erstellen).
3. Stelle sicher, dass in den Sims 4 Spieloptionen **Script-Mods erlaubt** sind.

## 🔓 Cheats aktivieren (Voraussetzung)
Damit die Konsole im Spiel funktioniert, musst du die Cheat-Konsole öffnen und den "Testing-Modus" aktivieren:
1. Drücke im Spiel gleichzeitig `Strg + Shift + C`.
2. Tippe oben in die weiße Leiste `testingcheats true` ein und drücke Enter.
3. Die Konsole bestätigt mit "Cheats are enabled".

## 💻 Konsolen-Befehle
* `make_god active` - Führt das aktive Profil auf den ausgewählten Sim aus.
* `make_god all` - Führt die Upgrades auf den gesamten Haushalt aus.
* `make_god_auto` - Analysiert den Sim (NPC/Gespielt, Geschlecht) und feuert das in der Config definierte Profil ab.
* `trait_god [mode] [set_id] [interest]` - Bearbeitet nur Merkmale. *Modi: `add_only`, `clean`, `remove_bad`.*
* `skill_god` - Setzt alle Fähigkeiten auf Level 10.
* `harmony_god` - Setzt Freundschafts- und Romantik-Beziehungen zu Haushaltsmitgliedern auf 100.
* `master_god` - Maximiert/kündigt die aktuelle Karriere; beendet das aktuelle Bestreben.
* `reload_god_config` - Lädt die `make_god_config.json` ohne Spiel-Neustart neu ein.
* `dump_traits_god` - Exportiert eine sortierte Liste aller im Spiel verfügbaren Traits in den Mods-Ordner.

---

## 🧪 Testszenario: Die Versuchskaninchen
Um alle Funktionen des Skripts fehlerfrei zu testen, empfehlen wir diesen Ablauf in einem neuen Spielstand.

### 1. Vorbereitung im CAS (Erstelle einen Sim)
Erstelle einen Haushalt mit diesen 3 Sims und platziere sie auf einem leeren Grundstück:
* **Sim 1: Arthur Anti-Gott (Männlich)**
  * **Zweck:** Test für `trait_god clean` und geschlechterspezifische Checks.
  * **Merkmale:** Böse, Faul, Hitzkopf (stehen auf der Exclude-Liste). Emotional: Hot-Headed, Lifestyle: Lazy, Social: Evil
* **Sim 2: Bella Basic (Weiblich)**
  * **Zweck:** Test für den Orchestrator `make_god active`.
  * **Merkmale:** Snob, Düster, Tollpatschig. Emotional: Gloomy, Emotional: Clumsy, Social: Snob
  * **Aufgabe vorab:** Gib ihr am Handy irgendeinen Job (z.B. Tellerwäscherin).
* **Sim 3: Chris Chaos (Egal welches Geschlecht)**
  * **Zweck:** Test für das smarte `make_god_auto` und Haushalts-Durchläufe.
  * **Merkmale:** Zufällig.

### 2. Durchführung im Spiel
Öffne die Cheat-Konsole (`Strg + Shift + C` -> `testingcheats true`).

**Test 1 (Arthur):**
* Wähle Arthur aus.
* Tippe: `trait_god remove_bad`
* *Ergebnis:* Seine schlechten Traits verschwinden sofort.
* Tippe: `harmony_god`
* *Ergebnis:* Die Beziehung zu Bella und Chris springt auf 100.

**Test 2 (Bella):**
* Wähle Bella aus.
* Tippe: `make_god active`
* *Ergebnis:* Das Skript heilt ihre negativen Traits, gibt ihr unzählige Gameplay-Vorteile, maximiert ihre Karriere, beendet ihr Bestreben, gibt ihr 11.000 Zufriedenheitspunkte und füllt das Haushaltskonto auf 9.999.999 Simoleons.

**Test 3 (Chris & Auto-Detect):**
* Wähle Chris aus.
* Tippe: `make_god_auto`
* *Ergebnis:* Die Konsole meldet `Auto-Detect (playable_male / playable_female): Set geladen: Default God`. Chris bekommt die exakten Götter-Eigenschaften zugewiesen.
* Schau anschließend in deinen Mods-Ordner: Öffne die `make_god_debug.txt`, um exakt zu sehen, was das Skript im Hintergrund alles geleistet hat!