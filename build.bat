@echo off
setlocal enabledelayedexpansion
title Sims 4 Mod Builder - FAST BUILD

:: ==========================================
:: KONFIGURATION & PARAMETER
:: ==========================================
:: Parameter-Prüfung: Start mit "/islc" aktiviert das Tool
set USE_ISLC=0
if /I "%~1"=="/islc" set USE_ISLC=1

set PY_VER=python37
set PYTHON_EXE=%UserProfile%\scoop\apps\%PY_VER%\current\python.exe
set SEVEN_ZIP=C:\Program Files\7-Zip\7z.exe
set GAME_DEST=%UserProfile%\Documents\Electronic Arts\The Sims 4
set MODS_DIR=%GAME_DEST%\Mods
set MOD_DEST=%MODS_DIR%\MakeGod
set ISLC_EXE=%UserProfile%\Documents\ISLC v1.0.3.7\Intelligent standby list cleaner ISLC.exe
:: ==========================================

echo === MakeGod Build Pipeline ===

:: --- GATE 1: Prozesspruefung ---
echo [+] Pruefe, ob Die Sims 4 laeuft...
tasklist /FI "IMAGENAME eq TS4_x64.exe" 2>NUL | find /I "TS4_x64.exe" >NUL
if not errorlevel 1 goto :GameRunning

:: Fallback fuer Legacy 32-Bit Systeme
tasklist /FI "IMAGENAME eq TS4.exe" 2>NUL | find /I "TS4.exe" >NUL
if not errorlevel 1 goto :GameRunning

:: --- GATE 2: Mod-Umgebung pruefen ---
echo [+] Pruefe Mods-Verzeichnis und Resource.cfg...
if not exist "%MODS_DIR%\Resource.cfg" (
    echo.
    echo [FEHLER] Keine Resource.cfg in "%MODS_DIR%" gefunden!
    echo Entweder ist der Pfad falsch, oder das Spiel wurde nach der Installation noch nie gestartet.
    pause
    exit /b 1
)

:: --- GATE 3: Zielverzeichnis vorbereiten ---
echo [+] Bereite Zielverzeichnis vor...
if not exist "%MOD_DEST%" (
    echo    - Erstelle Verzeichnis: %MOD_DEST%
    mkdir "%MOD_DEST%"
)

:: --- GATE 4: Altes Deployment & Spiel-Caches bereinigen ---
echo [+] Bereinige alte Dateien und Caches...
del /Q "%MOD_DEST%\make_god.ts4script" 2>nul
del /Q "%MOD_DEST%\make_god_debug.txt" 2>nul
del /Q "%MOD_DEST%\rmg_dump_*.txt" 2>nul
del /Q "%GAME_DEST%\localsimtexturecache.package" 2>nul
del /Q "%GAME_DEST%\localthumbcache.package" 2>nul
del /Q "%GAME_DEST%\avatarcache.package" 2>nul

:: --- GATE 5: Config synchronisieren (Smart Copy) ---
echo [+] Synchronisiere make_god_config.json...
if exist "make_god_config.json" (
    xcopy "make_god_config.json" "%MOD_DEST%\" /D /Y >nul
    echo    - Config geprueft / kopiert.
) else (
    echo    - Keine lokale Config im Projektordner gefunden. ^(Uebersprungen^)
)

echo.
echo [+] Starte Kompilierung mit %PY_VER%...

:: [1] Validierung
if not exist "%PYTHON_EXE%" (
    echo.
    echo FEHLER: %PY_VER% nicht gefunden.
    pause & exit /b
)

:: [2] Python Kompilierung (Mit For-Schleife fuer Windows CMD)
echo [+] Kompiliere Microservices...
for %%i in (*.py) do (
    "%PYTHON_EXE%" -m py_compile "%%i"
    if errorlevel 1 (
        echo.
        echo !!! FEHLER IM CODE GEFUNDEN IN: %%i !!!
        pause & exit /b
    )
)

:: [3] .pyc Dateien vorbereiten
if exist "__pycache__" (
    :: Alle kompilierten Dateien ins Hauptverzeichnis holen und umbenennen (Python 37 Formatierung entfernen)
    for /r "__pycache__" %%f in (*.cpython-37.pyc) do (
        set "filename=%%~nf"
        set "clean_name=!filename:.cpython-37=!.pyc"
        copy /Y "%%f" "!clean_name!" >nul
    )
    rmdir /S /Q "__pycache__"
)

:: [4] .ts4script Archiv erstellen
echo [+] Packe Archiv...
if exist "make_god.ts4script" del "make_god.ts4script"
"%SEVEN_ZIP%" a -tzip "make_god.ts4script" "*.pyc" >nul

:: [5] Deployment (Restliche Dateien)
echo [+] Kopiere Mod nach: %MOD_DEST%
copy /Y "make_god.ts4script" "%MOD_DEST%\make_god.ts4script" >nul
if exist "locales\" xcopy /E /I /Y "locales" "%MOD_DEST%\locales\" >nul
if exist "Relnan_MakeGod_UI.package" copy /Y "Relnan_MakeGod_UI.package" "%MOD_DEST%\Relnan_MakeGod_UI.package" >nul

:: [6] Aufräumen im Arbeitsverzeichnis
if exist "*.pyc" del "*.pyc"

echo [+] Build abgeschlossen.
echo.
echo weiter mit Tastendruck... (Sims 4 wird gleich gestartet)
pause >nul

:: --- PERFORMANCE OPTIMIERUNG & SPIELSTART ---

if "%USE_ISLC%"=="1" (
    if exist "%ISLC_EXE%" (
        tasklist /FI "IMAGENAME eq Intelligent*" 2>NUL | find /I "list cleaner" >NUL
        if !errorlevel! neq 0 (
            echo [+] Starte ISLC...
            start "" "%ISLC_EXE%" -minimized -polling 1000 -listsize 1024 -freememory 32768
        )
    ) else (
        echo [-] ISLC.exe nicht gefunden. Tool wird uebersprungen...
    )
)

echo [+] Starte Sims 4 via Steam...
start steam://rungameid/1222670

timeout /t 3
exit /b 0

:: ==========================================
:: FEHLER-ROUTINEN (Hierhin wird gesprungen)
:: ==========================================
:GameRunning
echo.
echo ************************************************************
echo * ACHTUNG: Die Sims 4 laeuft aktuell!                      *
echo * *
echo * Der Build-Prozess wurde abgebrochen, da das Spiel die    *
echo * Mod-Dateien aktuell blockiert (File Lock). Ein           *
echo * Ueberschreiben ist momentan nicht moeglich.              *
echo * *
echo * Bitte schliesse das Spiel und starte die Batch neu.      *
echo ************************************************************
echo.
echo Warte auf Tastendruck zum Beenden...
pause >nul
exit /b 1