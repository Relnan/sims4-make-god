# **Projektübersicht: MakeGod Mod (Microservice Architektur)**

**Zielsetzung:**  
Entwicklung einer modularen, hochkonfigurierbaren Sims 4 Mod ("MakeGod") zur gezielten Manipulation von Sims (Traits, Skills, Beziehungen, Finanzen). Ausführung über Konsolenbefehle sowie Vorbereitung für Picker-Menü (Loot Actions) via .package Datei.

## **1\. Architektur (Microservices)**

Anstatt eines monolithischen Skripts teilen wir die Logik in fokussierte, kleine Python-Dateien auf, die zusammen im make\_god.ts4script Archiv landen.

* mg\_main.py: Einstiegspunkt. Registriert die Konsolenbefehle, fängt den Loot-Aufruf vom Picker-Menü ab und orchestriert die Queue.  
* mg\_config.py: Lädt die make\_god\_config.json. Enthält den Pre-Processor, der // und /\* \*/ Kommentare filtert, und stellt die Fallback-Werte (Template) bereit.  
* mg\_logger.py: Zentrales Logging-Modul (Standard vs. Append, plus ausführlicher Debug-Modus).  
* mg\_queue.py: Das Herzstück für die Performance. Verwaltet die abzuarbeitenden Sims asynchron mit Error-Handling, um Lag-Spikes (Spiel-Einfrieren) zu verhindern.  
* mg\_utils.py: Helferfunktionen (Globale vs. Haushalts-Namenssuche, Sim-ID Auflösung, Occult-Check).  
* **Feature-Module (Worker):**  
  * mg\_feat\_traits.py: Add/Remove von Traits (unter Berücksichtigung von Geschlecht, Sexualität, Excludes).  
  * mg\_feat\_stats.py: Skills maximieren, Zufriedenheitspunkte, Motives (Motive einfrieren, Luck).  
  * mg\_feat\_relations.py: Beziehungen setzen (inklusive Vorab-Prüfung auf bestehende/höherwertige Verbindungen und Incest/Age-Sicherheit).  
  * mg\_feat\_wealth.py: Haushaltskasse anpassen.

## **2\. Ablaufplan / Milestones**

### **Phase 1: Fundament & Infrastruktur**

* Erstellung von mg\_config.py (inkl. JSON-Kommentar-Workaround) und dem Logging-System.  
* Erstellung des Grundgerüsts von mg\_main.py (Konsolen-Registrierung) und Such-Logik (mg\_utils.py), damit die Befehle all, active, id und name sauber aufgelöst werden. Bei multiplen Namenstreffern erfolgt nur eine Log-/Konsolenausgabe der IDs.

### **Phase 2: Performance & Queueing**

* Entwicklung der mg\_queue.py. Jeder Sim wird als separater "Task" in die Schlange gelegt.  
* Implementierung der Fehlerbehandlung (Try/Catch-Blöcke), damit ein Fehler bei einem Sim nicht den ganzen Haushalt abbricht.

### **Phase 3: Feature-Entwicklung (Die "God"-Kräfte)**

* **Traits:** Logik für exclude, include und Abgleich mit Interest/Sex.  
* **Relations:** Die intelligente Beziehungs-Logik (Verheiratet \-\> Verlobt \-\> ...) inkl. Check, ob die bestehende Beziehung bereits gleich- oder höherwertig ist.  
* **Stats & Occult:** Skill-Maximierung, Einfrieren von spezifizierten Commodities (z.B. Vampir-Energie) anhand der Konfigurations-Sets.

### **Phase 4: Dump & UI-Bridge**

* Neuschreiben der Dump-Funktion (Traits, Commodities, Infos), aufgeteilt für aktiven Sim, gewählten Sim oder ganzen Haushalt.  
* Vorbereitung der "Hidden Loot Action" in mg\_main.py, die später von der .package (dem Kuchen-Menü am Sim) aufgerufen wird.

## **3\. Wichtige Konstanten & Regeln**

1. **Python-Version:** Sims 4 nutzt Python 3.7.0. Keine Features aus neueren Versionen (wie Walrus-Operator := oder match/case) verwenden.  
2. **Sicherheit zuerst:** Bevor eine sim\_info manipuliert wird, muss zwingend geprüft werden, ob sie valide und instanziiert ist.  
3. **Fehler in der Queue:** Wenn ein Sim in der Queue einen Fehler wirft, wird dies vom Logger (mg\_logger.py) dokumentiert, der Prozess läuft aber für die restlichen Sims weiter.  
4. **Logging:** Bei aktivem Debug-Modus in der Config wird *jede* Zuweisung (welcher Trait, welche Beziehung, etc.) exakt dokumentiert. Sonst nur ein "Erfolgreich für X Sims"-Zusammenfassungslog.