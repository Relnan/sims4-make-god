@echo off
setlocal enabledelayedexpansion
title Sims 4 Mod Builder - FAST BUILD

:: ==========================================
:: KONFIGURATION (FEST HINTERLEGT)
:: ==========================================
:: Wir nutzen die Version 3.7 von Scoop
set "PY_VER=python310"
set "PYTHON_EXE=%UserProfile%\scoop\apps\%PY_VER%\current\python.exe"

:: 7-Zip Pfad (Standardinstallation)
set "SEVEN_ZIP=C:\Program Files\7-Zip\7z.exe"

:: Zielordner (Nutzt Variable für deinen Dienst-PC Usernamen)
set "MOD_DEST=%UserProfile%\Documents\Electronic Arts\The Sims 4\Mods\Meine eigenen"
:: ==========================================

echo [+] Starte Kompilierung mit %PY_VER%...

:: [1] Validierung: Existiert Python in Scoop?
if not exist "%PYTHON_EXE%" (
    echo.
    echo FEHLER: %PY_VER% nicht unter %PYTHON_EXE% gefunden.
    echo Bitte 'scoop install %PY_VER%' ausfuehren.
    pause & exit /b
)

:: [2] Python Kompilierung
"%PYTHON_EXE%" -m py_compile make_god.py
if errorlevel 1 (
    echo.
    echo !!! FEHLER IM CODE GEFUNDEN !!!
    pause & exit /b
)

:: [3] .pyc Datei vorbereiten
:: Wir holen die .pyc aus dem Cache und benennen sie für Sims 4 um
if exist "__pycache__" (
    for /r "__pycache__" %%f in (*.pyc) do copy /Y "%%f" "make_god.pyc" >nul
    rmdir /S /Q "__pycache__"
)

:: [4] .ts4script Archiv erstellen
echo [+] Packe Archiv...
if exist "make_god.ts4script" del "make_god.ts4script"
"%SEVEN_ZIP%" a -tzip "make_god.ts4script" "make_god.pyc" >nul

:: [5] Deployment in den Mods-Ordner
echo [+] Kopiere Mod nach: %MOD_DEST%
if not exist "%MOD_DEST%" mkdir "%MOD_DEST%"
copy /Y "make_god.ts4script" "%MOD_DEST%\make_god.ts4script" >nul

:: Optionale Dateien (JSON/Locales) falls vorhanden
if exist "*.json" copy /Y "*.json" "%MOD_DEST%\" >nul
if exist "locales\" xcopy /E /I /Y "locales" "%MOD_DEST%\locales\" >nul

:: [6] Aufräumen
del "make_god.pyc"

echo [+] Build abgeschlossen.
echo.

:: --- PERFORMANCE OPTIMIERUNG & SPIELSTART ---

:: ISLC Start (falls nicht aktiv)
tasklist /FI "IMAGENAME eq Intelligent*" 2>NUL | find /I "list cleaner" >NUL
if %errorlevel% neq 0 (
    set "ISLC_EXE=%UserProfile%\Documents\ISLC v1.0.3.7\Intelligent standby list cleaner ISLC.exe"
    if exist "!ISLC_EXE!" (
        echo [+] Starte ISLC...
        start "" "!ISLC_EXE!" -minimized -polling 1000 -listsize 1024 -freememory 32768
    )
)

echo [+] Starte Sims 4 via Steam...
start steam://rungameid/1222670

:: Kurze Bestätigung vor dem Schließen des Fensters
timeout /t 3
exit