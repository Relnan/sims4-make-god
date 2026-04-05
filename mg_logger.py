import os
from datetime import datetime
import mg_config

LOG_FILE = os.path.join(mg_config.MOD_FOLDER, 'make_god_debug.txt')
_log_cleared_this_session = False

def init_logger():
    global _log_cleared_this_session
    mode = mg_config.get("log_mode", "overwrite")
    
    if mode == "overwrite" and not _log_cleared_this_session:
        try:
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                f.write(f"--- MakeGod Log Session Start: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} ---\n")
            _log_cleared_this_session = True
        except:
            pass

def log(message, is_debug=False, out=None, force_debug=False):
    init_logger()
    
    # Neues System: Auslesen des debug_level Strings statt des alten Booleans
    current_level = mg_config.get("debug_level", "normal")
    if isinstance(current_level, str):
        current_level = current_level.lower().strip()
        
    debug_enabled = (current_level in ["normal", "all"]) or force_debug
    
    # Wenn es eine reine Debug-Nachricht ist, aber das Level auf "none" steht, abbrechen
    if is_debug and not debug_enabled:
        return

    prefix = "[DEBUG]" if is_debug else "[INFO]"
    timestamp = datetime.now().strftime('%H:%M:%S')
    full_message = f"{prefix} [{timestamp}] {message}"

    # 1. In die Log-Datei schreiben
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(full_message + "\n")
    except:
        pass
        
    # 2. Ausgabe in die Ingame-Konsole (Info/Fehler immer, Debug nur wenn aktiv)
    if out and (debug_enabled or not is_debug):
        try:
            out(message)
        except:
            pass