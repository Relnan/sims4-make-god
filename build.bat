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
set MOD_DEST=%UserProfile%\Documents\Electronic Arts\The Sims 4\Mods\Meine eigenen
set ISLC_EXE=%UserProfile%\Documents\ISLC v1.0.3.7\Intelligent standby list cleaner ISLC.exe
:: ==========================================

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

:: [5] Altes Deployment bereinigen
echo [+] Bereinige alte Dateien im Mod-Ordner...
if not exist "%MOD_DEST%" mkdir "%MOD_DEST%"
del /Q "%MOD_DEST%\make_god.ts4script" 2>nul
del /Q "%MOD_DEST%\make_god_debug.txt" 2>nul
del /Q "%MOD_DEST%\rmg_dump_*.txt" 2>nul

:: [6] Deployment
echo [+] Kopiere Mod nach: %MOD_DEST%
copy /Y "make_god.ts4script" "%MOD_DEST%\make_god.ts4script" >nul

if exist "make_god_config.json" copy /Y "make_god_config.json" "%MOD_DEST%\" >nul
if exist "locales\" xcopy /E /I /Y "locales" "%MOD_DEST%\locales\" >nul
if exist "Relnan_MakeGod_UI.package" copy /Y "Relnan_MakeGod_UI.package" "%MOD_DEST%\Relnan_MakeGod_UI.package" >nul

:: [7] Aufräumen im Arbeitsverzeichnis
if exist "*.pyc" del "*.pyc"

echo [+] Build abgeschlossen.
echo.
echo weiter mit Tastendruck... (Sims 4 wird gleich gestartet)
pause

:: --- PERFORMANCE OPTIMIERUNG & SPIELSTART ---

if "%USE_ISLC%"=="1" (
    tasklist /FI "IMAGENAME eq Intelligent*" 2>NUL | find /I "list cleaner" >NUL
    if %errorlevel% neq 0 (
        if exist "%ISLC_EXE%" (
            echo [+] Starte ISLC...
            start "" "%ISLC_EXE%" -minimized -polling 1000 -listsize 1024 -freememory 32768
        )
    )
)

echo [+] Starte Sims 4 via Steam...
start steam://rungameid/1222670

timeout /t 3
exit