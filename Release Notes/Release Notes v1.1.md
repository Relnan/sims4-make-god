# **🌟 MakeGod Mod v1.1 – Das Performance & Präzisions-Update**

**Das erste große Update ist da\!** Basierend auf eurem Feedback haben wir die MakeGod Mod unter der Haube komplett umstrukturiert. Version 1.1 bringt nicht nur neue Features, sondern löst auch das größte Problem bei der Verarbeitung großer Haushalte: Lags und Game-Freezes gehören der Vergangenheit an\!  
Zudem ist die Mod nun noch intelligenter im Umgang mit Drittanbieter-Mods (wie WickedWhims) und verhindert, dass eure individuellen Einstellungen bei Updates verloren gehen.  
Hier sind die Highlights, die Version 1.1 zu bieten hat:

## **✨ Die wichtigsten Neuerungen im Überblick**

### **⚡ Asynchrone Engine (Keine Game-Freezes mehr\!)**

Wer bisher rmg.all in einem riesigen Haushalt genutzt hat, kannte das Problem: Das Spiel fror für mehrere Sekunden ein, während die Mod im Hintergrund komplexe Beziehungs-Matrizen berechnet hat.  
**Das ist vorbei\!** Die neue Engine nutzt *Asynchrones Chunking*. Die Mod verarbeitet nun immer nur 2 Sims gleichzeitig, lässt das Spiel danach für einen Sekundenbruchteil weiterlaufen und nimmt sich dann die nächsten vor. Das Spiel bleibt komplett flüssig, während im Hintergrund wahre Wunder gewirkt werden\!

### **🧠 Das neue Relationship Master System**

Beziehungen zu setzen ist jetzt sicherer und logischer als je zuvor:

* **Downgrade-Schutz:** Sims, die bereits "Seelenverwandte" sind, werden nicht mehr versehentlich auf "Freunde" herabgestuft, nur weil es das Set so vorgibt.  
* **Inzest- & Alters-Schutz:** Die Mod prüft nun nativ Verwandtschaftsgrade und verhindert strikt romantische Zuweisungen zwischen Teenagern und Erwachsenen (konfigurierbar\!).  
* **Keine "Silent Fails" mehr:** Konfligierende Beziehungs-Bits (z. B. "Feind", wenn der Sim "Verheiratet" werden soll) werden vor der Neuzuweisung automatisch und sauber gelöscht.

### **🛡️ Unzerstörbare Config-Dateien (Soft-Parsing)**

Hast du beim Bearbeiten der make\_god\_config.json mal ein Komma vergessen und die Mod hat deine ganze Datei auf Standard zurückgesetzt? Das passiert nie wieder\!  
Das neue *Soft-Parsing* erkennt Tippfehler, legt automatisch ein Backup (.corrupted) deiner fehlerhaften Datei an und lädt trotzdem das Spiel. Zudem werden bei Mod-Updates neue Funktionen automatisch in deine Datei injiziert, ohne deine eigenen Makros oder Sets zu überschreiben.

### **🎭 Universelle Erkennung von Abneigungen (Dislikes)**

Der Schalter "remove\_all\_dislikes" ist jetzt eine echte Superwaffe. Die Mod sucht nicht mehr nur nach EA-Namen, sondern scannt die tiefe Spiele-Engine. **Jedes** Merkmal, das vom Spiel (oder von Mods wie WickedWhims\!) intern als "Abneigung / Turn-Off" geflaggt ist, wird gnadenlos gelöscht. Eure Sims werden nie wieder wegen der falschen Haarfarbe ihres Partners schlechte Laune bekommen\!

### **💊 Hybride Buff-Bereinigung (Mood-Scanner)**

Krankheiten und Flüche werden nicht mehr über eine einfache Liste gelöscht. MakeGod scannt nun die tatsächliche *Stimmung* (Mood) eurer Sims\! Jeder Buff, der den Sim wütend, traurig, beschämt, verängstigt oder angespannt macht, wird dynamisch entfernt.  
*(Hinweis: Essenzielle System-Buffs wie Werwolf-Wut oder Vampir-Durst sind durch eine neue Blacklist in der Config davor geschützt, euer Gameplay zu zerstören).*

### **🕵️‍♂️ KI-Ready Debugging (debug\_all)**

Für die absoluten Tech-Nerds und Mod-Bastler: Der neue Konsolen-Befehl rmg.active debug\_all generiert im Hintergrund einen exakten Vorher-Nachher-Vergleich (Dump) eures Sims und speichert diesen 15 Sim-Minuten später als flache Textdatei im Mod-Ordner ab. Perfekt, um zu prüfen, was genau die Mod unter der Haube verändert hat\!

## **⚙️ Wie update ich von v1.0 auf v1.1?**

Das Update ist spielend leicht:

1. Lösche die alte make\_god.ts4script aus deinem Mods-Ordner.  
2. Füge die neue make\_god.ts4script ein.  
3. **Optional, aber empfohlen:** Lösche deine alte make\_god\_config.json, starte das Spiel einmal, lass die neue Config generieren und trage deine Makros/Sets danach dort wieder ein, um die neuen Strukturblöcke (wie relationship\_system und buffs\_exclude\_from\_clear) sauber in deiner Datei zu haben.

*Viel Spaß mit der flüssigsten und präzisesten Version von MakeGod, die es je gab\!*