from pathlib import Path
import sys
from PySide6.QtCore import QLocale, QSettings, QTranslator

from core.models import PROGRAM_LANGUAGES

def get_internal_assets_path():
    """For use with assets and translations bundled with the exe."""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent

def get_system_default_language():
    """
    Iterate within the OS UI language priority until finding one of the supported languages. 
    Otherwise, defaults to 'en'.
    """
    # uiLanguages() returns a list of language codes (including locales: e.g. en_US or es-AR)
    for lang in QLocale.system().uiLanguages():
        
        # Normalize and extract base language code
        base_code = lang.replace('-', '_').split('_')[0]
        
        # Use the language if it is one of the supported by the program
        if base_code in PROGRAM_LANGUAGES:
            return base_code
            
    # Fallback to English if no supported language is found
    return "en"

def change_app_language(app, lang_code: str):
    """Loads a new .qm file and installs it globally."""
    if not hasattr(app, "active_translator"):
        app.active_translator = QTranslator()
    else:
        app.removeTranslator(app.active_translator)

    # Save preference regardless of language chosen
    settings = QSettings("EAYModding", "EAYGenerator")
    settings.setValue("language", lang_code)

    # English is the hardcoded fallback UI language
    if lang_code == "en":
        return

    # Locate the .qm file inside the bundled translations folder
    qm_path = get_internal_assets_path() / "translations" / f"{lang_code}.qm"

    # Convert Path object to str for QTranslator.load()
    if app.active_translator.load(str(qm_path)):
        app.installTranslator(app.active_translator)
    else:
        print(f"Warning: Could not load translation file: {qm_path}")