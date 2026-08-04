import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction, QIcon
from ui.episode_editor import EpisodeEditWidget
from ui.main_menu import MainMenuWidget

class EditorWindow(QMainWindow):
    def __init__(self, main_menu_window):
        super().__init__()
        self.main_menu_window = main_menu_window
        self.episode_editor = EpisodeEditWidget(self)
        self.setCentralWidget(self.episode_editor)
        
        # Set Menu Bar
        editor_menubar = self.menuBar()
        
        file_menu = editor_menubar.addMenu(self.tr("&File"))
        button_mainmenu = QAction(QIcon("assets/arrow-circle-225.png"), self.tr("Return to Main Menu"), self)
        button_mainmenu.setStatusTip(self.tr("Return to the main menu"))
        button_mainmenu.triggered.connect(lambda: self.switch_to_menu())
        file_menu.addAction(button_mainmenu)
        # help_menu = editor_menubar.addMenu(self.tr("&Help"))
        # help_menu.addAction(QAction(QIcon("assets/question-frame.png"), self.tr("About"), self))
    
    def load_episode_data(self, episode_name, prompts=[]):
        self.episode_editor.load_episode(episode_name, prompts)
        self.setWindowTitle("EAY Generator - Episode: " + episode_name)

    def switch_to_menu(self):
        self.main_menu_window.main_menu.update_folder_display()
        self.main_menu_window.show()
        self.close()

class MainMenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EAY Generator")
        self.main_menu = MainMenuWidget(self)
        self.setCentralWidget(self.main_menu)
    
    def switch_to_editor(self, episode_name=None, prompts=[]):
        self.editor_window = EditorWindow(self)
        self.editor_window.load_episode_data(episode_name, prompts)
        self.editor_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Add application icon
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    icon_path = os.path.join(root_dir, "assets", "icon.ico")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    else:
        print(f"Warning: Icon asset not found at {icon_path}")

    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec())