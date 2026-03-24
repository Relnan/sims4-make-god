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

## ⚙️ Konfiguration (`make_god_config.json`)
Die komplette Steuerung laeuft ueber die Datei `make_god_config.json`.
Nach Aenderungen im Spiel immer `reload_god_config` ausfuehren, damit die Werte ohne Neustart uebernommen werden.

### 1) Globale Optionen
* `language`: Sprache fuer Konsolentexte (`de` oder `en`).
* `debug_log`: `true`/`false` fuer Log-Datei `make_god_debug.txt`.

### 2) Auto-Profile (`auto_profiles`)
`make_god_auto` waehlt ueber diese Zuordnung automatisch ein Set.

Beispiel:
* `option_1.playable_male = "0"` -> spielbarer maennlicher Sim bekommt Set `0`
* `option_1.npc_female = "1"` -> weiblicher NPC bekommt Set `1`

Du hast 3 Profile:
* `option_1`
* `option_2`
* `option_3`

Aufruf im Spiel:
* `make_god_auto 1` nutzt `option_1`
* `make_god_auto 2` nutzt `option_2`
* `make_god_auto 3` nutzt `option_3`

### 3) Sets (`sets`)
Jedes Set ist ein Profil mit eigener ID (`"0"`, `"1"`, `"2"`, ...).
Diese ID verwendest du in Befehlen wie `make_god active 0 auto` oder `trait_god clean 2 bi`.

#### Bedeutungen der Set-Felder
* `name`: Anzeigename in der Konsole.
* `harmony_friendship`: Zielwert Freundschaft (typisch 0 bis 100).
* `harmony_romance`: Zielwert Romantik (typisch 0 bis 100).
* `harmony_reduce`: 
  * `false` = Werte werden nur erhoeht (nie abgesenkt)
  * `true` = Werte duerfen auch abgesenkt werden
* `freeze_occult_motives`: Fuellt okkulte Motive und stoppt deren Verfall.
* `satisfaction_points`: Punkte pro Sim bei `make_god`/`make_god_auto`.
* `add_funds`: Betrag, der zum Haushalt hinzugefuegt wird.
* `max_funds`: Obergrenze fuer Haushaltsgeld.

#### Trait-Cleaning (entfernen)
Alle `exclude_*` Listen arbeiten ueber Teilstrings (case-insensitive).
Wenn ein Trait-Name den Text enthaelt, wird er entfernt.

* `exclude_all`: Fuer alle Sims.
* `exclude_sex_male`: Zusaetzlich fuer maennliche Sims.
* `exclude_sex_female`: Zusaetzlich fuer weibliche Sims.
* `exclude_interest_male`: Zusaetzlich bei Interesse `m`.
* `exclude_interest_female`: Zusaetzlich bei Interesse `f`.
* `exclude_interest_bi`: Zusaetzlich bei Interesse `bi`.

#### Traits und Flags (hinzufuegen)
* `traits_all`: Immer hinzufuegen.
* `traits_sex_male`: Nur fuer maennliche Sims.
* `traits_sex_female`: Nur fuer weibliche Sims.
* `flags_interest_male`: Bei Interesse `m`.
* `flags_interest_female`: Bei Interesse `f`.
* `flags_interest_bi`: Bei Interesse `bi`.

Hinweis:
Zusatzlich werden alle Gameplay-Traits dynamisch aus dem Spiel ermittelt und hinzugefuegt,
ausser sie matchen etwas in `exclude_all`.

### 4) Sicherer Workflow fuer Aenderungen
1. Datei `make_god_config.json` bearbeiten.
2. Im Spiel `reload_god_config` ausfuehren.
3. Mit `trait_god clean <set_id> auto` oder `make_god active <set_id> auto` testen.
4. Falls noetig, Log in `make_god_debug.txt` pruefen.

### 5) Mini-Beispiel fuer ein neues Set
```json
"9": {
  "name": "Test Set",
  "harmony_friendship": 25,
  "harmony_romance": 75,
  "harmony_reduce": false,
  "freeze_occult_motives": false,
  "satisfaction_points": 5000,
  "add_funds": 10000,
  "max_funds": 250000,
  "exclude_all": ["mean", "jealous"],
  "exclude_sex_male": [],
  "exclude_sex_female": [],
  "exclude_interest_male": [],
  "exclude_interest_female": [],
  "exclude_interest_bi": [],
  "traits_all": ["trait_GreatKisser"],
  "traits_sex_male": [],
  "traits_sex_female": [],
  "flags_interest_male": ["trait_SexualOrientation_WooHooInterests_Female"],
  "flags_interest_female": ["trait_SexualOrientation_WooHooInterests_Male"],
  "flags_interest_bi": [
    "trait_SexualOrientation_WooHooInterests_Female",
    "trait_SexualOrientation_WooHooInterests_Male"
  ]
}
```

## 🔓 Cheats aktivieren (Voraussetzung)
Damit die Konsole im Spiel funktioniert, musst du die Cheat-Konsole öffnen und den "Testing-Modus" aktivieren:
1. Drücke im Spiel gleichzeitig `Strg + Shift + C`.
2. Tippe oben in die weiße Leiste `testingcheats true` ein und drücke Enter.
3. Die Konsole bestätigt mit "Cheats are enabled".

## 💻 Konsolen-Befehle
* `make_god [target_mode] [set_id] [interest]`
  * `target_mode`: `active`, `all` oder eine Sim-ID
  * `set_id`: Profil-ID aus `sets` (Standard: `0`)
  * `interest`: `auto`, `m`, `f`, `bi`
  * Beispiel: `make_god active 0 auto`
* `make_god_auto [option_id] [target_sim_id]`
  * `option_id`: `1`, `2`, `3` (liest `auto_profiles.option_x`)
  * Wählt je nach NPC/Playable + Geschlecht automatisch das passende Set.
* `trait_god [mode] [set_id] [interest] [target_sim_id]`
  * Modi: `add_only`, `clean`, `remove_bad`
  * Beispiel: `trait_god clean 0 bi`
* `skill_god [target_sim_id]` - Setzt alle Skills des Ziel-Sims auf Max.
* `harmony_god [set_id] [target_sim_id]` - Setzt Freundschaft/Romantik gemäß Set.
* `master_god [target_sim_id]` - Karrieren pushen + aktuelles Bestreben abschließen.
* `reload_god_config` - Lädt `make_god_config.json` im laufenden Spiel neu.
* `make_god_dump_stats` - Dump aller Statistics/Commodities des aktiven Sims.
* `make_god_dump_traits` - Dump aller ausgerüsteten Traits des aktiven Sims.
* `make_god_dump` - Führt beide Dumps nacheinander aus.

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
* Tippe: `harmony_god 0`
* *Ergebnis:* Die Beziehung zu Bella und Chris springt auf 100.

**Test 2 (Bella):**
* Wähle Bella aus.
* Tippe: `make_god active`
* *Ergebnis:* Das Skript heilt ihre negativen Traits, gibt ihr unzählige Gameplay-Vorteile, maximiert ihre Karriere, beendet ihr Bestreben, gibt ihr 11.000 Zufriedenheitspunkte und füllt das Haushaltskonto auf 9.999.999 Simoleons.

**Test 3 (Chris & Auto-Detect):**
* Wähle Chris aus.
* Tippe: `make_god_auto 1`
* *Ergebnis:* Die Konsole meldet `Auto-Detect (playable_male / playable_female): Set geladen: Default God`. Chris bekommt die exakten Götter-Eigenschaften zugewiesen.
* Schau anschließend in deinen Mods-Ordner: Öffne die `make_god_debug.txt`, um exakt zu sehen, was das Skript im Hintergrund alles geleistet hat!

### 3. Dump-Funktionen prüfen
* Wähle einen Sim aus.
* Tippe: `make_god_dump`
* *Ergebnis:* Zwei Dateien werden im Mod-Ordner erzeugt:
  * `god_dump_stats_<gender>_<occult>_<name>.txt`
  * `god_dump_traits_<gender>_<occult>_<name>.txt`
