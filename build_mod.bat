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

:: [2] Python Kompilierung
"%PYTHON_EXE%" -m py_compile make_god.py
if errorlevel 1 (
    echo.
    echo !!! FEHLER IM CODE GEFUNDEN !!!
    pause & exit /b
)

:: [3] .pyc Datei vorbereiten
if exist "__pycache__" (
    for /r "__pycache__" %%f in (*.pyc) do copy /Y "%%f" "make_god.pyc" >nul
    rmdir /S /Q "__pycache__"
)

:: [4] .ts4script Archiv erstellen
echo [+] Packe Archiv...
if exist "make_god.ts4script" del "make_god.ts4script"
"%SEVEN_ZIP%" a -tzip "make_god.ts4script" "make_god.pyc" >nul

:: [5] Deployment
echo [+] Kopiere Mod nach: %MOD_DEST%
if not exist "%MOD_DEST%" mkdir "%MOD_DEST%"
copy /Y "make_god.ts4script" "%MOD_DEST%\make_god.ts4script" >nul

if exist "*.json" copy /Y "*.json" "%MOD_DEST%\" >nul
if exist "locales\" xcopy /E /I /Y "locales" "%MOD_DEST%\locales\" >nul

:: [6] Aufräumen
if exist "make_god.pyc" del "make_god.pyc"

echo [+] Build abgeschlossen.
echo.

:: --- PERFORMANCE OPTIMIERUNG & SPIELSTART ---

if "%USE_ISLC%"=="1" (
    tasklist /FI "IMAGENAME eq Intelligent*" 2>NUL | find /I "list cleaner" >NUL
    if %errorlevel% neq 0 (
        if exist "%ISLC_EXE%" (
            echo [+] Starte ISLC...
            :: Hier werden die Anführungszeichen nur für den Start-Befehl gesetzt
            start "" "%ISLC_EXE%" -minimized -polling 1000 -listsize 1024 -freememory 32768
        )
    )
)

echo [+] Starte Sims 4 via Steam...
start steam://rungameid/1222670

timeout /t 3
exit