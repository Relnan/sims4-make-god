# **🌟 MakeGod Mod für Die Sims 4**

Willkommen bei **MakeGod**\! Das ist keine gewöhnliche Cheat-Mod, sondern ein schnelles und anpassbares Werkzeug, um deine Sims mit wenigen Klicks oder Befehlen massiv zu verändern.  
Egal, ob du einen unsterblichen Super-Vampir, ein Wunderkind oder einfach nur den perfekten Nachbarn erschaffen willst: MakeGod spart dir eine Menge Einzel-Cheats und wiederholte Handarbeit.  
**Hinweis:** Der Mod ist ein Hobby-Projekt zum Kennenlernen der Modding-Funktionalität. Es gibt keine Gewähr auf Vollständigkeit. Große Teile wurden mit Unterstützung von KI (Gemini) erstellt.

## **⚙️ Voraussetzungen & Empfehlungen**

Für das volle MakeGod-Erlebnis und alle UI-Funktionen beachte bitte die folgenden Voraussetzungen und optionalen Ergänzungen:

### **🔴 Zwingend erforderlich**

* [**XML Injector**](https://scumbumbomods.com/xml-injector) **(von Scumbumbo / Triplis):**  
  Für das Shift-Klick-Menü ist dieses Skript erforderlich. Ohne den XML Injector kann das MakeGod-Menü im Spiel nicht geladen werden. Stelle also sicher, dass die Dateien korrekt im Mods-Ordner liegen.

### **🟡 Dringend empfohlen (für das Profil „Ultimate God“)**

Fehlen die folgenden Mods, sollten die zugehörigen Spezialzuweisungen in der Regel einfach übersprungen werden. Mit ihnen kann Set 0 jedoch deutlich mehr Zusatz-Features anwenden:

* **MC Command Center (von Deaderpool):** MakeGod nutzt spezielle MCCC-Flags, um deinen Sim vor dem EA-Lösch-Algorithmus zu schützen, seine Muskeln/Statur einzufrieren und ihm bei Bedarf Eifersucht zu nehmen oder Polyamorie zu erlauben.  
* **WickedWhims (von TURBODRIVER):** Nutzt zusätzliche WW-Traits wie „Unique Looks“ oder „Generous Lover“ sowie weitere passende WickedWhims-Eigenschaften aus der Konfiguration.

### **🟢 Nützliche Ergänzungen (Perfekt für eigene Macros)**

Diese Mods sind für das MakeGod-Skript nicht erforderlich, harmonieren aber perfekt mit dem God-Mode-Spielstil und deinen eigenen Erweiterungen in der make\_god\_config.json:

* **AllCheats (von TwistedMexi):** MakeGod braucht eigentlich keinen Cheat-Unlocker. Wenn du jedoch in der Config-Datei eigene Batches und Menü-Optionen (Macros) baust und dort tiefgreifende, von EA eigentlich gesperrte Entwickler-Cheats eintragen möchtest, schaltet AllCheats diese für dich frei.  
* **UI Cheats Extension (von weerbesu):** Die perfekte Ergänzung zu unserem Shift-Klick-Menü. Es erlaubt dir das direkte Verändern von UI-Elementen (wie Linksklick auf Bedürfnisbalken, Finanzen oder Uhrzeiten) ganz ohne Menü-Navigation.

## **📥 Installation**

Die Installation ist unkompliziert und in wenigen Minuten erledigt:

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

Im Live-Modus hast du zwei Möglichkeiten: über das Ingame-Menü oder über die Cheat-Konsole.

### **🖱️ Methode 1: Das Klick-Menü**

Je nach UI-Version findest du die Einträge entweder über **Aktionen** oder per **Shift+Klick \> MakeGod**. Standardmäßig sind vor allem **Option 1 bis 3** belegt; zusätzlich lassen sich bis zu **5 Makro-Buttons** über die Config definieren.

1. Klicke auf einen Sim.  
2. Öffne das Menü **MakeGod** bzw. **Aktionen**.  
3. Wähle eine passende Aktion:  
   * **Option 1 / 2 / 3:** Führt das jeweils zugewiesene Profil bzw. Makro aus.  
   * **Option 4 / 5:** Optional frei belegbare Zusatzaktionen über macros.  
   * **Household:** Nur bei spielbaren Sims sichtbar; wendet MakeGod auf den aktiven Haushalt an.

### **⌨️ Methode 2: Die Cheat-Konsole**

Drücke im Spiel Strg \+ Shift \+ C, um die Konsole zu öffnen. Die Mod bringt eigene Befehle mit, die du direkt eintippen kannst:

* rmg – Zeigt die integrierte Hilfe in der Cheat-Konsole.  
* rmg.all \[Set\_ID|auto|option\_1\] \[override\] \[debug\] – Wendet MakeGod auf den aktiven Haushalt an.  
* rmg.active \[Set\_ID|auto|option\_1\] \[override\] \[debug\] – Wendet MakeGod auf den aktuell ausgewählten Sim an.  
* rmg.add id \<SimID\> – Verbindet einen Sim gezielt via ID mit deinem aktiven Sim (Freundschaft/Romantik).  
* rmg.add name \<Name\> – Verbindet einen Sim via Name mit deinem aktiven Sim. Bei mehreren Treffern listet die Konsole die IDs auf.  
* rmg.id \<SimID\> \[Set\_ID|auto|option\_1\] \[override\] \[debug\] – Wendet MakeGod auf einen Sim über seine interne ID an.  
* rmg.name "Bella Grusel" \[Set\_ID|auto|option\_1\] \[override\] \[debug\] – Sucht nach einem Sim per Name und wendet das Set an.  
* rmg.bat \<BatchName\> \[id "ID1,ID2"|name "Name1,Name2"|active\] \[Arg0\] \[Arg1\] ... – Führt eine automatisierte Liste von Befehlen nacheinander aus.  
* rmg.dump oder rmg.dump active – Erstellt Export-Dateien für den aktiven Sim.  
* rmg.dump all – Erstellt Export-Dateien für den ganzen Haushalt.  
* rmg.dump reference – Exportiert eine Master-Liste aller geladenen Traits, Zauber, Tränke und Perks.

*Tipp:* Mit dem Zusatz debug oder debug\_all (z.B. rmg.active 0 debug\_all) bekommst du ausführlichere Ausgaben und Log-Einträge. Der Debug-Befehl muss dabei immer am Ende stehen.

### **🤖 Das Batch-System (rmg.bat)**

Du kannst in der make\_god\_config.json unter dem Punkt "batches" eigene Listen von Befehlen definieren, die die Mod nacheinander abarbeiten soll. Das ist perfekt, wenn du bei einem neuen Spielstart immer wiederkehrende Szenarien aufbauen möchtest.  
**Sims direkt anvisieren (Targeting):**  
Du kannst einen Batch gezielt für eine Liste von Sims aufrufen:

* rmg.bat \<BatchName\> id "12345, 67890"  
* rmg.bat \<BatchName\> name "Yuki Behr, Bella Grusel"  
* rmg.bat \<BatchName\> active

**Kontext-Platzhalter für die anvisierten Sims:**  
In deinen Batch-Befehlen kannst du Platzhalter verwenden, die automatisch mit den Daten des gerade verarbeiteten Sims gefüllt werden:

* \[sim\_id\] \- Die interne ID des Sims  
* \[sim\_first\] \- Der Vorname  
* \[sim\_last\] \- Der Nachname  
* \[sim\_name\] \- Der komplette Name (inkl. Anführungszeichen)

**Dynamische Templates (Positions-Platzhalter):**  
Du kannst auch Platzhalter wie {0}, {1} verwenden. Beim Aufruf des Batches übergibst du die entsprechenden Werte einfach am Ende als Parameter.  
*Wichtig:* Wenn du einen Vor- und Nachnamen als ein einziges Argument übergeben willst, musst du ihn zwingend in Anführungszeichen setzen\!  
*Beispiel in der Config:*  
"setup\_npc": \[  
    "rmg.add id \[sim\_id\]",  
    "rmg.id \[sim\_id\] 3"  
\]

Eingabe im Spiel: rmg.bat setup\_npc name "Yuki Behr, Bella Grusel"  
(Achtung: Wenn du sehr viele Sims in einem einzigen Batch verarbeitest, kann das Spiel für einige Sekunden im Hintergrund asynchron arbeiten. Es kommt zu keinen langen Freezes, aber die Effekte treten nach und nach ein.)

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

### **📊 Standard-Sets im Überblick**

| Set-ID | Name | Zielgruppe | Kernfunktionen |
| :---- | :---- | :---- | :---- |
| 0 | Ultimate God | Spielbarer Erwachsener | Alle Skills \+ Karrieren max., 9,9 Mio. Simoleons, Bedürfnisse einfrieren, negative Traits entfernen, WickedWhims-Traits |
| 1 | Mortal Lover | NPC-Partner | Freundschaft \+ Romantik 100, Status "Bedeutende/r Andere/r", wenige Trait-Korrekturen |
| 2 | Vanilla NPC | Neutraler Townie | Freundschaft 50, keinerlei Geld- oder Skill-Eingriff |
| 3 | Enhanced NPC | Weibliche Roommates/NPCs | MCCC/WW Flags, Unsterblichkeit, diverse positive Traits, keine negativen Traits |
| 10 | Blessed Child | Spielbares Kind / Kleinkind | Altersgerechte Skills, Bedürfnisse einfrieren, Kindheits-Boni |
| 11 | NPC Child | NPC-Kind | Nur „Gemein" und „Böse" entfernen – sonst kein Eingriff |

Eigene Sets anlegen: Kopiere einen vorhandenen Block in der make\_god\_config.json, vergib eine neue ID (z. B. "5" oder "boss\_npc") und trage sie in auto\_profiles ein.

### **Was sind Auto-Profile?**

Die Mod ordnet die UI-Optionen automatisch passenden Sets zu. Ein Klick auf **Option 1** muss also nicht bei jedem Sim dasselbe Ergebnis liefern: Ein spielbarer Erwachsener kann z. B. **Set 0** erhalten, während ein Kind automatisch **Set 10** bekommt.  
Die Zuordnung steuerst du in make\_god\_config.json unter auto\_profiles – getrennt nach spielbaren Sims, NPCs, Geschlecht und Alter.

### **Das UI-Makro-System (Klick-Menü anpassen)**

Die Buttons im Ingame-Menü sind nicht fest an ein Profil gebunden. In make\_god\_config.json gibt es dafür den Bereich macros.  
Dort definierst du für ui\_playable\_01 bis ui\_playable\_05 bzw. ui\_npc\_01 bis ui\_npc\_05, welche Befehle beim Klick tatsächlich ausgeführt werden. Je nach UI-Pack erscheinen diese Aktionen im MakeGod-Untermenü.  
Nutze den Platzhalter \[sim\_id\], damit der hinterlegte Befehl exakt auf den angeklickten Sim angewendet wird.  
*Beispiel aus der Config:*  
"macros": {  
    "ui\_playable\_01": \[  
        "rmg.id \[sim\_id\] option\_1"  
    \],  
    "ui\_playable\_02": \[  
        "sims.give\_satisfaction\_points 10000 \[sim\_id\]"  
    \],  
    "ui\_npc\_01": \[  
        "rmg.id \[sim\_id\] 1"  
    \]  
}

In diesem Beispiel würde ein Klick auf **Option 2** bei einem *gespielten Sim* ihm einfach 10.000 Zufriedenheitspunkte geben. Du kannst hier jeden beliebigen EA-Cheat oder MakeGod-Befehl eintragen. Das gibt dir die absolute Freiheit, dein eigenes Ingame-Cheat-Menü zusammenzubauen\!

### **So baust du eigene Sets (wichtige Parameter)**

Die Datei enthält ein eingebautes Lexikon (\_help\_set\_parameter). Hier ist kurz erklärt, wie die wichtigsten Parameter funktionieren:

* **Fähigkeiten (Skills):** max\_player\_skills und max\_npc\_skills steuern, ob Skills überhaupt maximiert werden. Mit allowed\_skills begrenzt du das auf bestimmte Skill-Namen. Mit allow\_all\_skills: true werden wirklich alle verfügbaren Skills maximiert.  
* **Traits & Abneigungen:** traits\_all und exclude\_all steuern globale Trait-Filter. Der mächtige Schalter "remove\_all\_dislikes": true entfernt vollautomatisch alle \[DISLIKE\] Merkmale (Abneigungen gegen Farben, Musik, Hobbys), sodass dein Sim niemals mehr grundlos schlechte Laune bekommt.  
* **Magie & Okkult-Vorteile:** Du kannst Perks (Ruhm & Okkult-Fähigkeiten) über perks\_all / perks\_occult gezielt freischalten.  
* **Beziehungen im Haushalt:** harmony\_friendship, harmony\_romance und target\_relationship\_status setzen Freundschaft, Romantik und Beziehungsstatus für Haushaltsmitglieder. Über remove\_negative\_relations, remove\_negative\_relations\_household und remove\_negative\_relations\_scope lassen sich außerdem Feindschaften, Groll und Angst-Bits gezielt im gesamten weltweiten Beziehungsnetz entfernen.

### **Okkulte Sims (Vampire, Werwölfe, Magier)**

MakeGod behandelt okkulte Sims völlig automatisch korrekt\! In der Konfiguration (unter "motives\_to\_fill") weiß das Spiel genau, dass ein Vampir keine "Blase" hat, die eingefroren werden muss, sondern "Durst" und "Vampir-Energie".

## **📖 Vollständige Konfigurations-Referenz**

Alle verfügbaren Parameter auf einen Blick. Die \_help\_set\_parameter-Sektion in der make\_god\_config.json enthält dieselben Beschreibungen direkt im Mod-Ordner.

### **Globale Einstellungen**

| Schlüssel | Typ | Standard | Bedeutung |
| :---- | :---- | :---- | :---- |
| language | String | "de" | Sprache der eingebauten Hilfetexte ("de" oder "en"). |
| debug\_level | String | "normal" | "none" \= Aus, "normal" \= Nur Text-Log, "all" \= Text-Log \+ Vorher/Nachher-Dump als Datei. |
| debug\_alarm\_delay | Zahl | 5.0 | Wartezeit (in Sekunden, wird in Sim-Minuten umgerechnet) vor dem Auslesen des Nachher-Dumps. |
| log\_mode | String | "overwrite" | "overwrite" \= Log-Datei bei jedem Start neu erstellen; "append" \= Einträge anhängen. |
| include\_roommates\_in\_all | Boolean | true | Bei rmg.all oder dem "Household"-Button werden offizielle Mitbewohner mit einbezogen. |
| include\_keyholders\_in\_all | Boolean | true | Bei rmg.all werden auch Freunde mit einem Haustürschlüssel berücksichtigt. |
| dump\_blacklist\_keywords | Liste | *(technische Strings)* | Teilstrings, die beim Sim-Dump aus der Statistik-Ausgabe herausgefiltert werden, z. B. "\_high", "caspartid". |
| buffs\_exclude\_from\_clear | Liste | *(System-Buffs)* | Negative Buffs (Flüche/Krankheiten), die von der automatischen Löschung ausgenommen werden. |
| manual\_add\_settings \-\> friendship | Zahl | 100 | Freundschaftswert, der bei rmg.add zugewiesen wird (-999 ignoriert). |
| manual\_add\_settings \-\> romance | Zahl | \-999 | Romantikwert, der bei rmg.add zugewiesen wird (-999 ignoriert). |
| manual\_add\_settings \-\> spawn\_sim | Boolean | false | true \= Bei rmg.add wird der Sim physisch zu deinem aktiven Sim teleportiert. Löst das MCCC-Flags Problem\! |

### **Skills & Karriere**

| Schlüssel | Typ | Bedeutung |
| :---- | :---- | :---- |
| allow\_all\_skills | Boolean | true \= Alle sicher erkannten Skills maximieren; überschreibt die Filterung durch allowed\_skills. |
| max\_player\_skills | Boolean | Skills für Sims im gespielten Haushalt maximieren. |
| max\_npc\_skills | Boolean | Skills für NPCs und Townies maximieren. |
| allowed\_skills | Liste | Namens-Fragmente erlaubter Skills (z. B. \["fitness", "logic"\]). Leer \= fallback\_skills greift. |
| master\_player\_careers | Boolean | Alle aktiven Karrieren promoten, Schule pushen und den aktuellen Bestrebungs-Meilenstein abschließen (gespielte Sims). |
| master\_npc\_careers | Boolean | Wie oben, aber für NPCs. |

Die Config enthält zusätzlich den Abschnitt "fallback\_skills", der pro Altersgruppe (adult, child, toddler, infant) festlegt, welche Skills maximiert werden, wenn allowed\_skills leer ist. Für Kinder und Kleinkinder greift immer eine altersgerechte Gruppe – unabhängig vom gewählten Set.

### **Luck, Belohnungen & Geld**

| Schlüssel | Typ | Bedeutung |
| :---- | :---- | :---- |
| luck → value | Zahl | Glückswert: \-100 (Pech) bis 100 (Glück); 0 \= nicht verändern. |
| satisfaction\_points | Zahl | Zufriedenheitspunkte hinzufügen. 0 \= kein Eingriff. |
| add\_funds | Zahl | Simoleons dem Haushalt hinzufügen. Pro Haushalt nur einmal pro Run ausgeführt. 0 \= kein Eingriff. |
| max\_funds | Zahl | Obergrenze des Haushaltsvermögens nach dem Hinzufügen. |

### **Bedürfnisse & Motive**

| Schlüssel | Typ | Bedeutung |
| :---- | :---- | :---- |
| fill\_motives\_mode | String | "all" \= EA-Cheat für alle Motive; "config" \= nur die in motives\_to\_fill genannten; "none" \= kein Eingriff. |
| freeze\_motives | Boolean | Setzt den Verfalls-Modifier der in motives\_to\_fill genannten Commodities auf 0\. Der Sim verliert diese Bedürfnisse dann nicht mehr automatisch. |
| motives\_to\_fill | Objekt | Schlüssel: Okkult-Typ ("human", "vampire", "spellcaster", "werewolf", "mermaid"). Wert: Liste exakter Commodity-Namen, z. B. "motive\_hunger" oder "commodity\_motive\_vampire\_thirst". |

### **Traits & Perks**

| Schlüssel | Typ | Bedeutung |
| :---- | :---- | :---- |
| remove\_all\_dislikes | Boolean | true \= Alle \[DISLIKE\]-Merkmale (Farb-/Musik-Abneigungen) werden automatisch erkannt und entfernt. |
| exclude\_all | Liste | Traits immer entfernen – gilt für alle Sims dieses Sets. |
| exclude\_sex\_male | Liste | Traits nur bei männlichen Sims entfernen. |
| exclude\_sex\_female | Liste | Traits nur bei weiblichen Sims entfernen. |
| traits\_all | Liste | Traits immer hinzufügen – gilt für alle Sims dieses Sets. |
| traits\_sex\_male | Liste | Traits nur bei männlichen Sims hinzufügen. |
| traits\_sex\_female | Liste | Traits nur bei weiblichen Sims hinzufügen. |
| traits\_occult | Objekt | Okkult-Typ → Trait-Liste. Nur der Typ des aktuellen Sims wird berücksichtigt. |
| perks\_all | Liste | Okkult-/Ruhm-Perks für alle Sims freischalten (über den internen Bucks-Tracker). |
| perks\_occult | Objekt | Perks nach Okkult-Typ ("vampire", "spellcaster", "werewolf"). |

### **Beziehungen bereinigen & setzen**

| Schlüssel | Typ | Bedeutung |
| :---- | :---- | :---- |
| harmony\_friendship | Zahl | Freundschaftswert für alle Haushaltsmitglieder setzen. \-999 \= nicht anfassen. |
| harmony\_romance | Zahl | Romantikwert setzen (nur für Sims ab Teen-Alter). \-999 \= nicht anfassen. |
| target\_relationship\_status | String | Beziehungsstatus erzwingen. Erlaubt: "friend", "best\_friend", "woohoo\_partner", "significant\_other", "engaged", "married". |
| relationship\_system | Objekt | Definiert globale Regeln (z. B. allow\_downgrade, allow\_incest, allow\_teen\_adult\_romance) sowie die exakten EA-Bits und Konflikt-Entfernungen pro Beziehungsstatus. |
| remove\_negative\_relations | Boolean | true \= Scannt alle weltweiten Beziehungen. Sims, die ein Bit aus remove\_negative\_relations\_scope tragen, werden von **allen** negativen Bits befreit. |
| remove\_negative\_relations\_household | Boolean | true \= Haushaltsmitglieder werden **immer** bereinigt – unabhängig vom Scope. |
| remove\_negative\_relations\_scope | Liste | Bit-Namens-Fragmente (z. B. "friend", "romantic", "married"), die einem weltweiten Sim Kandidaten-Status verleihen. Als negativ gelten Bits wie enemy, grudge, divorced, breakup, hostile, fear. |
| harmony\_extended\_network | Objekt | Eine erweiterte Matrix, um alters- und geschlechtsabhängig Beziehungen zu Freunden/Familie weltweit aufzubauen. (enabled: true/false, scopes: \[...\]) |

**Beispiel:** "remove\_negative\_relations": true mit "remove\_negative\_relations\_scope": \["friend", "romantic", "married"\]  
→ Alle Freunde, Partner und Haushaltsmitglieder werden von Groll, Feindschaft und Angst befreit. Unbekannte Townies ohne Beziehung bleiben unberührt.

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

### **3\. Dump eines bestimmten Sims per ID**

Mit dem Befehl rmg.dump id \<SimID\> (z. B. rmg.dump id 12345678\) kannst du gezielt einen einzelnen Sim exportieren – auch wenn er nicht in deinem aktiven Haushalt ist. Die SimID findest du entweder im Sim-Abschnitt eines vorherigen Dumps (Feld **ID**) oder über rmg.name "Vorname" in der Konsole (gibt bei mehreren Treffern alle IDs aus).

## **❓ Häufige Fragen (FAQ)**

**Das "Make God" Menü taucht im Spiel nicht auf\!**

* Vergewissere dich, dass du beide Dateien (.ts4script und .package) in deinem Mods-Ordner hast.  
* Prüfe, ob du "Script-Mods" in den Spieloptionen aktiviert hast.  
* Versteckt sich die Option vielleicht unter "Aktionen" \-\> "Mehr Auswahl..."?  
* Falls das Menü durch andere Mods blockiert wird, funktionieren die Text-Befehle wie rmg.active über die Konsole in der Regel weiterhin.

**Mein Batch-Skript / rmg.name setzt keine Flags bei Townies (z.B. MCCC/WickedWhims)\!**

* Drittanbieter-Mods registrieren Trait-Änderungen oft nur, wenn der Sim als "Instanced" (physisch auf dem Grundstück geladen) markiert ist. Befindet sich der Townie "schlafend" in seinem Haus, speichert EA zwar das Trait, aber Mods wie MCCC blockieren das Update in ihrer Datenbank.  
* **Die Lösung:** Aktiviere "spawn\_sim": true in deiner make\_god\_config.json unter "manual\_add\_settings". Rufst du den NPC in deinem Batch nun zuerst über rmg.add auf, teleportiert das Skript ihn sofort physisch zu deinem Sim. Anschließend funktioniert die Zuweisung über rmg.name fehlerfrei\!

**Wie vergebe ich Schlüssel automatisch im Batch?**

* Schlüssel sind in der Sims-Engine zickig. Am stabilsten funktioniert es, wenn du den Trait trait\_HasKey direkt in die traits\_all- oder traits\_sex\_female-Liste deines Wunsch-Sets (z. B. Set 3\) einträgst.  
* Wenn du dann in deinem Skript rmg.add id \[sim\_id\] (Teleport) gefolgt von rmg.id \[sim\_id\] 3 ausführst (z. B. via rmg.bat setup\_npc name "Yuki Behr"), bekommt sie den Schlüssel zuverlässig.

**Der Button "Haushalt" fehlt bei einigen Sims\!**

* Das ist pure Absicht als Schutzmaßnahme. Der Haushalt-Button wird bei NPCs (Townies, Briefträger etc.) absichtlich versteckt, damit du nicht versehentlich Familien, die du nicht spielst, in Götter verwandelst.

**Mein Kleinkind hat nicht die Fähigkeit "Fitness" bekommen\!**

* Auch das ist Absicht\! Die Mod schützt Kinder und Kleinkinder davor, unpassende Erwachsenen-Skills zu erhalten. Die Mod maximiert stattdessen automatisch ihre altersgerechten Fähigkeiten (wie Motorik oder das Töpfchengehen).

**Ich habe die make\_god\_config.json zerschossen und das Spiel lädt sie nicht mehr\!**

* Keine Panik\! Lösche die .json Datei einfach aus deinem Mods-Ordner. Wenn du das Spiel das nächste Mal startest, generiert die Mod automatisch eine frische Standard-Datei.

**Wo finde ich Logs oder Debug-Infos?**

* Die Mod schreibt in make\_god\_debug.txt im Mods-Ordner.  
* Mit debug\_level: "normal" oder "all" in der Config und dem Konsolen-Zusatz debug bzw. debug\_all bekommst du deutlich mehr Details.

**Ich bin unsicher beim Bearbeiten der Config. Was ist der sichere Weg?**

* Vor dem Bearbeiten kurz eine Kopie der Datei machen (z.B. make\_god\_config\_backup.json).  
* Danach nur kleine Änderungen machen und testen.  
* Wenn etwas kaputt ist: make\_god\_config.json löschen, Spiel neu starten, neue Standard-Datei erzeugen lassen.

**Perks oder Zauber werden nicht freigeschaltet, obwohl die Namen korrekt wirken\!**

* Die Namen müssen exakt mit dem internen \_\_name\_\_-Attribut der Engine übereinstimmen – nicht mit dem Anzeigenamen im Spiel.  
* Nutze rmg.dump reference, um die korrekten Namen direkt aus dem laufenden Spiel zu exportieren.  
* Okkult-Perks (Vampire, Magier, Werwölfe) können nur freigeschaltet werden, wenn der Sim den entsprechenden Okkult-Typ bereits hat.  
* **Wichtig für gespielte Sims:** Das Spiel initialisiert den internen Perk-Tracker oft erst, wenn das entsprechende Menü angesehen wird. Öffne das Vorteil-/Perk-Fenster deines Sims (z. B. Vampirkräfte oder Magier-Vorteile) mindestens einmal manuell im Spiel, bevor du MakeGod ausführst, damit das Skript die Perks erfolgreich eintragen kann.

**rmg.name findet den Sim nicht\!**

* Gib den Vor- oder Nachnamen exakt ein (Groß-/Kleinschreibung wird ignoriert).  
* Bei mehreren Treffern gibt die Mod alle Kandidaten mit ID in der Konsole aus – verwende dann rmg.id \<SimID\>.  
* Sims, die nicht im Spielspeicher geladen sind (z. B. Townies aus weit entfernten Welten), werden möglicherweise nicht gefunden.

**Ich habe rmg.add benutzt, aber die Beziehungswerte stimmen nicht / ändern sich nicht\!**

* *Wichtig:* Sims, die aktuell nicht aktiv im Level geladen sind ("Hidden"), können einige Beziehungs-Updates teilweise ignorieren oder das Update schlägt stumm fehl. Nutze auch hier "spawn\_sim": true in der Config, um den Sim für das Update zuverlässig zu dir zu rufen.

**Beziehungen oder Geld werden nach einem Spielupdate zurückgesetzt\!**

* Das ist kein Mod-Bug – EAs "Relationship Culling" löscht ältere Freundschaften bei bestimmten Ereignissen automatisch.  
* Abhilfe: MC Command Center (MCCC) installieren und die No-Cull-Flags aktivieren. Diese Flags lassen sich auch direkt über MakeGod verteilen, z. B. Deaderpool\_MCCC\_Trait\_FlagNoRelCull in traits\_all.

**Karrieren werden nicht gepusht\!**

* Karrieren können nur befördert werden, wenn der Sim bereits in einer Karriere ist. MakeGod weist keine neue Karriere zu – nur vorhandene werden gepusht.  
* Schule (gradeschool / highschool) wird für Kinder und Teens automatisch erkannt und braucht nicht konfiguriert zu werden.

## **⚠️ Wichtige Hinweise zur Performance (Freezes & Lags)**

Wenn du das Kommando rmg.all oder Beziehungs-Updates bei Sims mit sehr vielen Bekanntschaften ausführst, arbeitet das Skript im Hintergrund hochkomplexe Matrizen ab. Es scannt das gesamte erweiterte soziale Netzwerk deines Sims, bereinigt versteckte negative Tracker, ignoriert Kompatibilitäts-Konflikte und passt Freundschafts- sowie Romantikwerte nach Alter und Geschlecht an.  
**Keine Panik, das Spiel stürzt nicht ab\!**  
Da die Engine diese Berechnungen auf dem sogenannten "Main-Thread" durchführt, verarbeitet MakeGod bei größeren Gruppen (wie rmg.all) immer nur 2 Sims gleichzeitig und macht dazwischen kurze Pausen. Das Spiel läuft währenddessen weiter, es kann jedoch zu kurzen Mikrorucklern kommen, bis die Warteschlange komplett abgearbeitet ist.  
**Tipp:** Wenn du aufwendige Beziehungs-Funktionen wie harmony\_extended\_network per enabled: false deaktivierst oder einzelne Freundschafts-/Romantikwerte gezielt auf \-999 setzt, läuft das Skript deutlich schneller durch.  
**Hinweis zur Nutzung des 'debug\_all' Befehls:**  
Wenn Sie den Befehl mit dem Parameter debug\_all (z. B. rmg.all debug\_all) ausführen, sammelt die Mod massiv "Vorher-Nachher"-Speicherabzüge (Dumps) aller betroffenen Sims im Arbeitsspeicher und wartet 15 Sim-Minuten, bis die Engine alle Änderungen verarbeitet hat. Anschließend werden diese in eine gesonderte Run-Textdatei exportiert. Nutzen Sie diesen Befehl nur, wenn das Spiel auf einer schnellen SSD installiert ist, da es sonst zu starken Verzögerungen beim Speichern der Log-Dateien kommen kann.  
*Viel Spaß beim Erschaffen deiner perfekten Sims-Welt\!*