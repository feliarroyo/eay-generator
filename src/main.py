import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QSettings
from PySide6.QtGui import QCloseEvent, QIcon
from core.fileManager import delete_temp_folder
from core.assetsManager import change_app_language, get_internal_assets_path, get_system_default_language
from ui.build_menu import BuildMenuWidget
from ui.episode_editor import EpisodeEditWidget
from ui.main_menu import MainMenuWidget

class EditorWindow(QMainWindow):
    def __init__(self, main_menu_window):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.episode_editor = EpisodeEditWidget(self)
        self.setCentralWidget(self.episode_editor)

    def load_episode_data(self, episode_name, prompts=[]):
        print(f"Loading episode data for '{episode_name}' with {len(prompts)} prompts.")
        self.episode_editor.load_episode(episode_name, prompts)
        self.setWindowTitle(self.tr("EAY Generator - Episode: ") + episode_name)

    def switch_to_menu(self):
        print("Switching back to main menu and cleaning up temporary files.")
        self.episode_editor.clear_editor()
        self.main_menu_window.main_menu.update_folder_display()
        self.main_menu_window.show()
        self.close()
        
    def closeEvent(self, event: QCloseEvent):
        """Intercepts window close requests and returns to the main menu."""
        self.episode_editor.return_to_menu()
        event.ignore()

class BuildMenuWindow(QMainWindow):
    def __init__(self, main_menu_window):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.build_menu = BuildMenuWidget(self)
        self.setCentralWidget(self.build_menu)
        self.setWindowTitle(self.tr("EAY Generator - Build Episode"))

    def switch_to_menu(self):
        self.main_menu_window.show()
        self.close()
    
    def closeEvent(self, event: QCloseEvent):
        """Intercepts window close requests and returns to the main menu."""
        if self.build_menu.revert_menu:
            self.build_menu.revert_menu.close()
        self.switch_to_menu()
        event.ignore()

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        delete_temp_folder()
        self.setWindowTitle(self.tr("EAY Generator"))
        self.main_menu = MainMenuWidget(self)
        self.setCentralWidget(self.main_menu)
    
    def switch_to_editor(self, episode_name=None, prompts=[]):
        self.editor_window = EditorWindow(self)
        self.editor_window.load_episode_data(episode_name, prompts)
        self.editor_window.show()
        self.hide()
        
    def switch_to_build_menu(self):
        self.build_menu_window = BuildMenuWindow(self)
        self.build_menu_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Language settings
    settings = QSettings("EAYModding", "EAYGenerator")
    saved_lang = settings.value("language", get_system_default_language())
    change_app_language(app, saved_lang)
    # Add application icon
    icon_path = get_internal_assets_path() / "assets" / "icon.ico"
    if os.path.exists(icon_path):
        app_icon = QIcon(str(icon_path))
        app.setWindowIcon(app_icon)
    else:
        print(f"Warning: Icon asset not found at {icon_path}")

    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())