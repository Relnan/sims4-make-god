# **🌟 MakeGod Mod für Die Sims 4**

Willkommen bei **MakeGod**\! Dies ist nicht einfach nur eine weitere Cheat-Mod – es ist ein extrem mächtiges, blitzschnelles und hochgradig anpassbares Werkzeug, um das Leben deiner Sims mit nur einem einzigen Klick komplett zu perfektionieren (oder zu ruinieren, je nachdem, was du in der Konfiguration einstellst\!).  
Egal, ob du einen unsterblichen Super-Vampir, ein absolutes Wunderkind oder einfach nur den perfekten Nachbarn erschaffen willst: MakeGod erledigt in einem Bruchteil einer Sekunde das, wofür du sonst stundenlang Cheats eintippen müsstest.

Aktuell ist die Menü Integration noch nicht funktionsfähig.

## **📥 Installation**

Die Installation ist super einfach und erfordert nur zwei Schritte:

1. Lade dir die neueste Version von MakeGod herunter. Du erhältst zwei Dateien:  
   * make\_god.ts4script (Die Logik und das Gehirn der Mod)  
   * Relnan\_MakeGod\_UI.package (Das Ingame-Menü)  
2. Kopiere **beide Dateien** in deinen Die Sims 4 Mods-Ordner.  
   * Standard-Pfad: Dokumente\\Electronic Arts\\Die Sims 4\\Mods  
3. **WICHTIG:** Gehe im Spiel in die Optionen unter "Weiteres" und stelle sicher, dass **"Benutzerdefinierte Inhalte und Mods aktivieren"** sowie **"Script-Mods erlaubt"** mit einem Häkchen versehen sind\!

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

### **⌨️ Methode 2: Die Cheat-Konsole (Für Profis)**

Drücke im Spiel Strg \+ Shift \+ C, um die Konsole zu öffnen. Die Mod bringt eigene Befehle mit, die du eintippen kannst:

* rmg.active \- Wendet MakeGod (Option 1\) auf deinen aktuell ausgewählten Sim an.  
* rmg.all \- Wendet MakeGod automatisch auf deinen ganzen Haushalt an.  
* rmg.name "Bella Grusel" \- Sucht nach Bella Grusel und wendet die Mod auf sie an, egal wo sie gerade ist.  
* *Tipp:* Du kannst hinter jeden Befehl eine Zahl anhängen (z.B. rmg.all 5), um ein ganz bestimmtes "Set" (siehe unten) zu erzwingen.

## **⚙️ Wie passe ich die Mod an? (Die Config-Datei)**

Das wahre Herzstück dieser Mod ist die **Konfigurationsdatei**.  
Sobald du das Spiel mit der Mod zum ersten Mal startest, generiert die Mod automatisch eine Datei namens make\_god\_config.json in deinem Mods-Ordner. Du kannst diese Datei mit jedem Texteditor (wie dem normalen Windows Editor oder Notepad++) öffnen.

### **Was sind "Sets"?**

In der Datei findest du einen Bereich namens "sets". Ein Set ist quasi ein Bauplan für einen Sim.  
Standardmäßig gibt es z.B.:

* **Set 0 (Ultimate God):** Der Sim kriegt alle Fähigkeiten auf Maximum, alle Karrieren auf Stufe 10, maximale Zufriedenheitspunkte, Millionen von Simoleons, negative Merkmale (wie "Böse") werden gelöscht und seine Bedürfnisse frieren für immer auf Maximum ein.  
* **Set 10 (Blessed Child):** Das perfekte Kinder-Profil. Karrieren werden ignoriert, aber die Kinder-Fähigkeiten (Motorik, Kreativität) werden gemaxt.

### **Was sind "Auto Profile"?**

Die Mod ist schlau\! Wenn du im Spiel auf "Option 1" klickst, bekommt nicht jeder Sim einfach stur "Set 0" aufgedrückt.  
In der Config unter "auto\_profiles" ist geregelt, wer welchen Bauplan bekommt.

* *Beispiel:* Du hast Option 1 geklickt. Die Mod sieht: "Aha, das ist ein spielbarer Erwachsener, er bekommt **Set 0**." \- "Oh, das daneben ist ein Kind, es bekommt automatisch **Set 10**."  
  Du kannst die Zuweisungen für NPCs, Männer, Frauen und Kinder hier völlig frei anpassen\!

### **So baust du eigene Sets:**

Die Datei enthält ein eingebautes Lexikon (\_help\_set\_parameter). Hier ist kurz erklärt, wie die Filter funktionieren:

* **Fähigkeiten (Skills):** Du kannst in "allowed\_skills" genau aufschreiben, was der Sim können soll (z.B. \["fitness", "charisma"\]). Lässt du es leer, füllt die Mod den Sim automatisch mit allen logischen Hauptfähigkeiten für sein Alter auf. Nutzt du "allow\_all\_skills": true, wird gnadenlos **jede** Fähigkeit des Spiels auf Maximum gesetzt.  
* **Der clevere Filter (Merkmale löschen):** Unter "exclude\_all" kannst du Merkmale eintragen, die du weghaben willst. Trag einfach "evil" ein, und die Mod löscht alles, was böse ist (egal ob das Spiel es intern trait\_evil oder trait\_Vampire\_evil nennt).

### **Okkulte Sims (Vampire, Werwölfe, Magier)**

MakeGod behandelt okkulte Sims völlig automatisch korrekt\! In der Konfiguration (unter "motives\_to\_freeze") weiß das Spiel genau, dass ein Vampir keine "Blase" hat, die eingefroren werden muss, sondern "Durst" und "Vampir-Energie".

## **🕵️‍♀️ Für Profis: Die Dump-Funktion (Wie finde ich die richtigen Namen?)**

Wenn du ein bestimmtes Merkmal oder einen neuen Skill zu deinem Set hinzufügen willst, brauchst du den exakten internen Namen von Electronic Arts (z.B. trait\_GreatKisser). Aber wie findet man den heraus?  
**Die Lösung:** Erstelle den Sim einfach einmal normal im Spiel und gib ihm das Merkmal. Öffne dann die Cheat-Konsole (Strg \+ Shift \+ C) und tippe ein:  
rmg.dump  
Die Mod durchleuchtet deinen aktiven Sim nun komplett und erstellt dir eine ordentliche .txt-Datei in deinem Mods-Ordner. Dort stehen fein säuberlich aufgelistet alle internen Namen seiner aktuellen Fähigkeiten, Merkmale und Bedürfnisse drin. Du kannst diese Namen dann einfach kopieren und in deine make\_god\_config.json einfügen\!  
*(Tipp: Mit rmg.dump all kannst du den kompletten Haushalt auf einmal durchleuchten).*

## **❓ Häufige Fragen (FAQ)**

**Das "Make God" Menü taucht im Spiel nicht auf\!**

* Vergewissere dich, dass du beide Dateien (.ts4script und .package) in deinem Mods-Ordner hast.  
* Prüfe, ob du "Script-Mods" in den Spieloptionen aktiviert hast.  
* Versteckt sich die Option vielleicht unter "Aktionen" \-\> "Mehr Auswahl..."?

**Ich habe die make\_god\_config.json zerschossen und das Spiel lädt sie nicht mehr\!**

* Keine Panik\! Lösche die .json Datei einfach aus deinem Mods-Ordner. Wenn du das Spiel das nächste Mal startest, generiert die Mod automatisch eine frische, funktionierende Standard-Datei.

**Der Button "Haushalt" fehlt bei einigen Sims\!**

* Das ist pure Absicht als Schutzmaßnahme. Der Haushalt-Button wird bei NPCs (Townies, Briefträger etc.) absichtlich versteckt, damit du nicht versehentlich Familien, die du nicht spielst, in Götter verwandelst.

**Mein Kleinkind hat nicht die Fähigkeit "Fitness" bekommen\!**

* Auch das ist Absicht\! Die Mod schützt Kinder und Kleinkinder davor, unpassende Erwachsenen-Skills zu erhalten. Die Mod maximiert stattdessen automatisch ihre altersgerechten Fähigkeiten (wie Motorik oder das Töpfchengehen).

*Viel Spaß beim Erschaffen deiner perfekten Sims-Welt\!*