import os
from posixpath import basename
import sys
from tkinter import filedialog
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar, QStackedWidget, QStatusBar, QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize
from ui.episode_editor import EpisodeEditWidget
from ui.main_menu import MainMenuWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EAY Generator")
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.main_menu = MainMenuWidget(self)
        self.episode_editor = EpisodeEditWidget(self)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.episode_editor)
        

        
         # Submenus
        self.setMenuBar(None)
        
    def switch_to_editor(self, episode_name=None, prompts=[]):
        # button_new = QAction(QIcon("assets/plus.png"), self.tr("Create New Episode"), self)
        # button_new.setStatusTip(self.tr("Start a new episode"))
        # button_new.triggered.connect(lambda: self.switch_to_editor())
        # button_save = QAction(QIcon("assets/disk.png"), self.tr("Save Current Episode"), self)
        # button_save.setStatusTip(self.tr("Save the current episode"))
        # button_save.triggered.connect(lambda: self.save_episode(episode_input.text(), self.prompts))
        button_mainmenu = QAction(QIcon("assets/arrow-circle-225.png"), self.tr("Return to Main Menu"), self)
        button_mainmenu.setStatusTip(self.tr("Return to the main menu"))
        button_mainmenu.triggered.connect(lambda: self.switch_to_menu())
        editor_menubar = QMenuBar()
        file_menu = editor_menubar.addMenu(self.tr("&File"))
            # file_menu.addAction(button_new)
            # file_menu.addAction(button_save)
        file_menu.addAction(button_mainmenu)
        help_menu = editor_menubar.addMenu(self.tr("&Help"))
        help_menu.addAction(QAction(QIcon("assets/question-frame.png"), self.tr("About"), self))
        self.setMenuBar(editor_menubar)
        if episode_name:
            self.episode_editor.load_episode(episode_name, prompts)
            self.setWindowTitle("EAY Generator - Episode: " + episode_name)
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_menu(self):
        self.setMenuBar(None)
        self.setWindowTitle("EAY Generator")
        self.main_menu.update_folder_display()
        self.stacked_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Add application icon
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(current_dir, ".."))
    icon_path = os.path.join(root_dir, "assets", "icon.ico")
    if os.path.exists(icon_path):
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)
    else:
        print(f"Warning: Icon asset not found at {icon_path}")

    window.show()
    sys.exit(app.exec())