# 🌟 MakeGod Mod v1.0 – Das ultimative God-Mode Tool für Die Sims 4

**Endlich ist es soweit!** Nach intensiver Entwicklung, System-Optimierungen und unzähligen Testläufen präsentiere ich stolz die **Version 1.0** der MakeGod Mod. 

MakeGod ist keine gewöhnliche Cheat-Sammlung, sondern ein massives, intelligentes Werkzeug, das dir stundenlange Handarbeit und das lästige Eintippen von Einzel-Cheats erspart. Mit wenigen Klicks oder Konsolenbefehlen kannst du das Leben, die Fähigkeiten, die Finanzen und das komplette soziale Netzwerk deiner Sims nach deinen eigenen Regeln formen.

Hier sind die Highlights, die Version 1.0 zu bieten hat:

## ✨ Die wichtigsten Features im Überblick

### 🎯 Intelligente Profil-Sets (God-Mode auf Knopfdruck)
Statt jeden Sim einzeln anzupassen, nutzt MakeGod vorkonfigurierte "Sets" (Profile). Egal ob du deinen eigenen Sim zum unsterblichen **"Ultimate God"** machst (maximale Skills, Millionen Simoleons eingefrorene Bedürfnisse), einen Townie zum perfekten **"Mortal Lover"** formst oder ein **"Blessed Child"** mit maximierten Kleinkind-Fähigkeiten erschaffst – ein Klick oder ein Befehl genügt. 

### 🖱️ Das UI Macro System (Dein eigenes Kuchen-Menü)
Das Shift-Klick Ingame-Menü ist ab sofort **komplett frei programmierbar**! Du bist nicht mehr auf meine Vorgaben beschränkt. In der `make_god_config.json` kannst du die 5 Klick-Optionen für spielbare Sims und NPCs mit deinen eigenen Makros und Cheat-Ketten hinterlegen. Nutze Platzhalter wie `[sim_id]`, um gezielt den angeklickten Sim zu manipulieren.

### 🤖 Das mächtige Batch-Automatisierungssystem (`rmg.bat`)
Für die Power-User: Du kannst in der Config komplette Befehlslisten schreiben und diese im Spiel via `rmg.bat <BatchName> name "Bella Grusel, Yuki Behr"` auf ganze Listen von Sims gleichzeitig abfeuern. Die Mod ersetzt dynamische Kontext-Platzhalter (`[sim_id]`, `[sim_first]`) zur Laufzeit. Perfekt, um bei einem neuen Spielstand mit einem Befehl deine Lieblings-NPCs vorzubereiten!

### 🧛 Voller Okkult- & Alters-Support
Die Mod ist smart genug, um zu wissen, wer vor ihr steht. 
* **Okkulte:** Vampire, Magier und Werwölfe erhalten automatisch ihre spezifischen Perks, Zauber und Traits. Die Mod weiß sogar, dass ein Vampir keine "Blase" hat, sondern "Durst", und friert exakt die richtigen Bedürfnisse ein.
* **Altersgerecht:** Kinder und Kleinkinder werden davor geschützt, Erwachsenen-Skills wie "Mixen" zu erhalten. Sie maximieren stattdessen brav ihre Motorik- und Töpfchen-Fähigkeiten.

### ❤️ Beziehungs-Netzwerke & Harmonie
Nie wieder Stress im Haushalt! Mit einem Klick kannst du Feindschaften, Groll und Ängste im gesamten weltweiten Beziehungsnetzwerk eines Sims löschen. Die Mod kann automatisch Liebes- und Freundschaftswerte basierend auf Geschlecht und Alter anpassen und den Beziehungsstatus (z. B. auf "Ehepartner") zwingen.

### 🛠️ Tiefe Integration mit MCCC & WickedWhims
Nutzt du das *MC Command Center* oder *WickedWhims*? MakeGod klinkt sich nahtlos ein! Vergib vollautomatisch Flags, die das Aussehen und die Muskeln deiner Sims für immer einfrieren, sie vor EAs Lösch-Algorithmus (Culling) schützen, sie immun gegen Krankheiten/Schwitzen machen oder ihnen "Unique Looks" verleihen.

### 🕵️‍♂️ Das Referenz-Dump-System für Modder
Du willst einen bestimmten Trait aus einer anderen Mod in deine Config aufnehmen, kennst aber den internen Code nicht? Der Befehl `rmg.dump reference` durchsucht in Sekundenschnelle die tiefste Engine-Ebene deines laufenden Spiels und exportiert dir eine saubere Textdatei mit ALLEN aktuell geladenen Traits, Zaubern und Perks – inklusive denen deiner installierten Mods!

## ⚙️ Installation & Anforderungen

1. Lade dir die `.zip` oder die Dateien `make_god.ts4script` und `Relnan_MakeGod_UI.package` herunter.
2. Entpacke/Verschiebe sie in deinen Die Sims 4 `Mods`-Ordner.
3. **WICHTIG (Hard Requirement):** Du benötigst zwingend den **XML Injector** von Scumbumbo/Triplis, damit das Ingame-Klick-Menü funktioniert!

## 🚀 So legst du los
Starte das Spiel, öffne die Cheat-Konsole (`Strg+Shift+C`) und tippe **`rmg.active`**, um deinen aktuellen Sim in einen Gott zu verwandeln, oder **`rmg.all`**, um den gesamten Haushalt zu segnen. Alle weiteren Befehle findest du im Spiel, wenn du einfach nur `rmg` in die Konsole tippst!

*Danke an alle, die bei der Entstehung geholfen haben. Viel Spaß beim Erschaffen eurer perfekten Sims-Welten!*