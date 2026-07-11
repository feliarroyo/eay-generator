from posixpath import basename
import sys
from tkinter import filedialog
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QStatusBar, QToolBar
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
        
        button_new = QAction(QIcon("assets/plus.png"), "Create New Episode", self)
        button_new.setStatusTip("Start a new episode")
        button_new.triggered.connect(lambda: self.switch_to_editor()) # The current episode will be lost. Are you sure?
        button_save = QAction(QIcon("assets/disk.png"), "Save Current Episode", self)
        button_save.setStatusTip("Save the current episode")
        # button_save.triggered.connect(lambda: self.save_episode(episode_input.text(), self.prompts))
        button_mainmenu = QAction(QIcon("assets/arrow-circle-225.png"), "Return to Main Menu", self)
        button_mainmenu.setStatusTip("Return to the main menu")
        button_mainmenu.triggered.connect(lambda: self.switch_to_menu()) # The current episode will be lost. Are you sure?
        
        # Submenus
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_new)
        file_menu.addAction(button_save)
        file_menu.addAction(button_mainmenu)
        help_menu = menu.addMenu("&Help")
        help_menu.addAction(QAction(QIcon("assets/question-frame.png"), "About", self))
        
    def switch_to_editor(self):
        self.stacked_widget.setCurrentIndex(1)

    def switch_to_menu(self):
        self.stacked_widget.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())