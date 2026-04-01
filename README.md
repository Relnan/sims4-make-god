# **🌟 MakeGod Mod für Die Sims 4**

Willkommen bei **MakeGod**\! Dies ist nicht einfach nur eine weitere Cheat-Mod \- es ist ein extrem mächtiges, blitzschnelles und hochgradig anpassbares Werkzeug, um das Leben deiner Sims mit nur einem einzigen Klick komplett zu perfektionieren (oder zu ruinieren, je nachdem, was du in der Konfiguration einstellst\!).  
Egal, ob du einen unsterblichen Super-Vampir, ein absolutes Wunderkind oder einfach nur den perfekten Nachbarn erschaffen willst: MakeGod erledigt in einem Bruchteil einer Sekunde das, wofür du sonst stundenlang Cheats eintippen müsstest.  
*Der Mod ist ein Hobby-Projekt zum Kennenlernen der Modding-Funktionalität, und ich übernehme keine Gewähr auf Vollständigkeit.*  
*INFO: Der Mod wurde fast ausschließlich mit Unterstützung von KI (Gemini) erstellt.*

## **📥 Installation**

Die Installation ist super einfach und erfordert nur zwei Schritte:

1. Lade dir die neueste Version von MakeGod herunter. Du erhältst zwei Dateien:  
   * make\_god.ts4script (Die Logik und das Gehirn der Mod)  
   * Relnan\_MakeGod\_UI.package (Das Ingame-Menü, falls verfügbar)  
2. Kopiere **beide Dateien** in deinen Die Sims 4 Mods-Ordner.  
   * Standard-Pfad: Dokumente\\Electronic Arts\\Die Sims 4\\Mods  
3. **WICHTIG:** Gehe im Spiel in die Optionen unter "Weiteres" und stelle sicher, dass **"Benutzerdefinierte Inhalte und Mods aktivieren"** sowie **"Script-Mods erlaubt"** mit einem Häkchen versehen sind\!

## **🚀 Schnellstart für Einsteiger (2 Minuten)**

Wenn du nur kopieren und einfache Dateien bearbeiten kannst, reicht das hier völlig:

1. Installiere die Mod wie oben beschrieben.  
2. Starte das Spiel und lade einen Haushalt.  
3. Öffne die Cheat-Konsole mit Strg \+ Shift \+ C.  
4. Gib ein: rmg.active  
5. **Fertig.** Dein aktuell ausgewählter Sim bekommt das ultimative "God-Setup" (Maximale Skills, Millionen Simoleons, keine schlechte Laune mehr, ewige Bedürfnisse).

Wenn du den **ganzen Haushalt** auf einmal upgraden willst:  
Gib in die Konsole einfach rmg.all ein.

## **🎮 Wie benutze ich die Mod im Spiel?**

Sobald du im Live-Modus bist, hast du zwei Möglichkeiten, die Mod zu nutzen: über das bequeme Klick-Menü oder über Profi-Textbefehle.

### **🖱️ Methode 1: Das Klick-Menü (Empfohlen für jeden)**

1. Klicke einfach auf irgendeinen Sim (egal ob es dein eigener ist oder ein fremder Townie auf der Straße).  
2. Gehe in das Menü **Aktionen**.  
3. Dort findest du nun die neuen Optionen:  
   * **Make God \- Sim Option 1:** Wendet dein "Profil 1" (Standard: Absolute Perfektion) auf diesen einen Sim an.  
   * **Make God \- Sim Option 2:** Wendet dein "Profil 2" auf diesen Sim an.  
   * **Make God \- Sim Option 3:** Wendet dein "Profil 3" auf diesen Sim an.  
   * **Make God \- Household:** *Dieser Button taucht nur bei deinen gespielten Sims auf\!* Er wendet MakeGod blitzschnell auf den **kompletten Haushalt** an.

### **⌨️ Methode 2: Die Cheat-Konsole (einfach und zuverlässig)**

Drücke im Spiel Strg \+ Shift \+ C, um die Konsole zu öffnen. Die Mod bringt eigene Befehle mit, die du eintippen kannst:

* rmg \- Zeigt die integrierte Hilfe in der Cheat-Konsole.  
* rmg.all \[Set\_ID|auto|option\_xx\] \[debug\] \- Wendet MakeGod auf den ganzen aktiven Haushalt an.  
* rmg.active \[Set\_ID|auto|option\_xx\] \[debug\] \- Wendet MakeGod auf den aktuell ausgewählten Sim an.  
* rmg.id \<SimID\> \[Set\_ID|auto|option\_xx\] \[debug\] \- Wendet MakeGod auf einen Sim über seine interne ID an.  
* rmg.name "Bella Grusel" \[Set\_ID|auto|option\_xx\] \[debug\] \- Sucht nach einem Sim per Name.  
* rmg auto \- Kurzbefehl für rmg all auto.  
* rmg.dump active oder rmg.dump all \- Erstellt Export-Dateien deiner Sims (siehe unten).  
* rmg.dump reference \- Exportiert eine Master-Liste aller Spiel-Codes (siehe unten).

*Tipp:* Mit dem Zusatz debug (z.B. rmg.active 0 debug) bekommst du ausführlichere Ausgaben und Log-Einträge.

## **⚙️ Wie passe ich die Mod an? (Die Config-Datei)**

Das wahre Herzstück dieser Mod ist die **Konfigurationsdatei**.  
Startest du das Spiel mit der Mod, generiert sie automatisch eine make\_god\_config.json in deinem Mods-Ordner. Du kannst sie mit jedem Texteditor (wie dem normalen Windows Editor oder Notepad++) öffnen.

### **Einsteiger-Modus: Nur 3 Dinge ändern**

Wenn du möglichst wenig anfassen willst, ändere nur diese Punkte in make\_god\_config.json:

1. Unter auto\_profiles festlegen, welches Set bei Option 1 / 2 / 3 verwendet wird.  
2. Im gewünschten Set ("0", "1", "10" ...) nur traits\_all anpassen.  
3. Optional add\_funds ändern, wenn du mehr oder weniger Geld geben willst.

### **Was sind "Sets"?**

In der Datei findest du einen Bereich namens "sets". Ein Set ist quasi ein Bauplan für einen Sim.  
Ein Set kann unter anderem Traits hinzufügen oder entfernen, Abneigungen löschen, Skills maximieren, Karrieren pushen, Zufriedenheitspunkte vergeben, Bedürfnisse einfrieren, Beziehungen innerhalb des Haushalts setzen und Haushaltsgeld anpassen.  
Standardmäßig gibt es z.B.:

* **Set 0 (Ultimate God):** Der Sim kriegt alle Fähigkeiten auf Maximum, alle Karrieren auf Stufe 10, Millionen von Simoleons, negative Merkmale (wie "Böse" oder Abneigungen) werden gelöscht und seine Bedürfnisse frieren für immer auf Maximum ein. Zudem lernt er alle Zauber und Okkult-Perks.  
* **Set 10 (Blessed Child):** Das perfekte Kinder-Profil. Karrieren werden ignoriert, aber die Kinder-Fähigkeiten (Motorik, Kreativität) werden gemaxt.

### **Was sind "Auto Profile"?**

Die Mod ist schlau\! Wenn du im Spiel auf "Option 1" klickst, bekommt nicht jeder Sim einfach stur "Set 0" aufgedrückt.  
In der Config unter "auto\_profiles" ist geregelt, wer welchen Bauplan bekommt.

* *Beispiel:* Du hast Option 1 geklickt. Die Mod sieht: "Aha, das ist ein spielbarer Erwachsener, er bekommt **Set 0**." \- "Oh, das daneben ist ein Kind, es bekommt automatisch **Set 10**."  
  Du kannst die Zuweisungen für NPCs, Männer, Frauen und Kinder hier völlig frei anpassen\!

### **So baust du eigene Sets (Wichtige Parameter):**

Die Datei enthält ein eingebautes Lexikon (\_help\_set\_parameter). Hier ist kurz erklärt, wie die wichtigsten Parameter funktionieren:

* **Fähigkeiten (Skills):** max\_player\_skills und max\_npc\_skills steuern, ob Skills überhaupt maximiert werden. Mit allowed\_skills begrenzt du das auf bestimmte Skill-Namen. Mit allow\_all\_skills: true werden wirklich alle verfügbaren Skills maximiert.  
* **Traits & Abneigungen:** traits\_all und exclude\_all steuern globale Trait-Filter. Der mächtige Schalter "remove\_all\_dislikes": true entfernt vollautomatisch alle \[DISLIKE\] Merkmale (Abneigungen gegen Farben, Musik, Hobbys), sodass dein Sim niemals mehr grundlos schlechte Laune bekommt.  
* **Magie & Okkult-Vorteile:** Du kannst Perks (Ruhm & Okkult-Fähigkeiten) über perks\_all / perks\_occult und Zaubersprüche/Tränke über spells\_all / spells\_occult gezielt freischalten.  
* **Beziehungen im Haushalt:** harmony\_friendship, harmony\_romance und target\_relationship\_status setzen Freundschaft, Romantik und Beziehungsstatus für Mitglieder desselben Haushalts.

### **Okkulte Sims (Vampire, Werwölfe, Magier)**

MakeGod behandelt okkulte Sims völlig automatisch korrekt\! In der Konfiguration (unter "motives\_to\_fill") weiß das Spiel genau, dass ein Vampir keine "Blase" hat, die eingefroren werden muss, sondern "Durst" und "Vampir-Energie".

## **🕵️‍♀️ Für Tech-Freaks & Modder: Das Dump-System**

Du willst deinem Set Merkmale aus anderen Mods (wie *WickedWhims* oder *Basemental*) hinzufügen, kennst aber den internen Namen nicht? Die Mod bringt ein mächtiges Auslese-Werkzeug mit\!

### **1\. Der Reference-Dump (Der Heilige Gral)**

Öffne die Cheat-Konsole im Spiel und tippe:  
rmg.dump reference  
Die Mod durchsucht in Sekundenschnelle die tiefste Code-Ebene der Spiel-Engine und exportiert dir eine saubere Markdown-Datei (.md) in deinen Mod-Ordner.  
Diese Datei enthält eine **vollständige, alphabetische Liste aller Traits, Zauber, Tränke und Perks, die das Spiel gerade geladen hat (inklusive ALLER Mods\!)**. Kopiere die Namen einfach heraus und füge sie in deine make\_god\_config.json ein. Du bist nie wieder auf Wiki-Seiten angewiesen\!

### **2\. Der Sim- & Haushalts-Dump**

Willst du wissen, welche internen System-Werte ein bestimmter Sim gerade hat?  
Tippe rmg.dump all (für den ganzen Haushalt) oder rmg.dump active.  
Die Mod exportiert ein sauberes Dokument, das dir nicht nur Traits und Skills auflistet, sondern auch verborgene System-Werte (Commodities), okkulte Perks, freigeschaltete Zauber sowie Beziehungs-Werte und verborgene Beziehungs-Bits zu anderen Sims.  
*(Tipp: Über den Punkt dump\_blacklist\_keywords in der Config filtert die Mod automatisch uninteressanten System-Junk aus diesen Reports heraus).*

## **❓ Häufige Fragen (FAQ)**

**Das "Make God" Menü taucht im Spiel nicht auf\!**

* Vergewissere dich, dass du beide Dateien (.ts4script und .package) in deinem Mods-Ordner hast.  
* Prüfe, ob du "Script-Mods" in den Spieloptionen aktiviert hast.  
* Versteckt sich die Option vielleicht unter "Aktionen" \-\> "Mehr Auswahl..."?  
* Falls das Menü durch andere Mods blockiert wird, funktionieren die Text-Befehle (rmg.active) über die Konsole trotzdem immer zu 100%\!

**Der Button "Haushalt" fehlt bei einigen Sims\!**

* Das ist pure Absicht als Schutzmaßnahme. Der Haushalt-Button wird bei NPCs (Townies, Briefträger etc.) absichtlich versteckt, damit du nicht versehentlich Familien, die du nicht spielst, in Götter verwandelst.

**Mein Kleinkind hat nicht die Fähigkeit "Fitness" bekommen\!**

* Auch das ist Absicht\! Die Mod schützt Kinder und Kleinkinder davor, unpassende Erwachsenen-Skills zu erhalten. Die Mod maximiert stattdessen automatisch ihre altersgerechten Fähigkeiten (wie Motorik oder das Töpfchengehen).

**Ich habe die make\_god\_config.json zerschossen und das Spiel lädt sie nicht mehr\!**

* Keine Panik\! Lösche die .json Datei einfach aus deinem Mods-Ordner. Wenn du das Spiel das nächste Mal startest, generiert die Mod automatisch eine frische Standard-Datei.

**Wo finde ich Logs oder Debug-Infos?**

* Die Mod schreibt in make\_god\_debug.txt im Mods-Ordner.  
* Mit debug\_log: true in der Config und dem Konsolen-Zusatz debug bekommst du deutlich mehr Details.

**Ich bin unsicher beim Bearbeiten der Config. Was ist der sichere Weg?**

* Vor dem Bearbeiten kurz eine Kopie der Datei machen (z.B. make\_god\_config\_backup.json).  
* Danach nur kleine Änderungen machen und testen.  
* Wenn etwas kaputt ist: make\_god\_config.json löschen, Spiel neu starten, neue Standard-Datei erzeugen lassen.

*Viel Spaß beim Erschaffen deiner perfekten Sims-Welt\!*