import os
from PySide6.QtCore import QSettings, QTranslator

def change_app_language(app, lang_code):
    """Loads a new .qm file and installs it globally."""
    if not hasattr(app, 'active_translator'):
        app.active_translator = QTranslator()
    else:
        app.removeTranslator(app.active_translator)

    if lang_code == "en":
        return

    qm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "translations", f"{lang_code}.qm")
    
    if app.active_translator.load(qm_path):
        app.installTranslator(app.active_translator)
        settings = QSettings("EAYModding", "EAYGenerator")
        settings.setValue("language", lang_code)
    else:
        print(f"Warning: Could not load translation file: {qm_path}")