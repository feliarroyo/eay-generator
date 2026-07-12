import os
from src.core.fileManager import create_base_folder, create_episode_folder, list_episode_folders
from PySide6.QtWidgets import QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget

create_base_folder()  # Ensure the base folder exists

class MainMenuWidget(QWidget):
    def __init__(self, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window
        self.setWindowTitle("Main Menu")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        episode_label = QLabel(self.tr("Episode Name"))
        episode_input = QLineEdit()
        episode_input.setPlaceholderText(self.tr("e.g. Inside Jokes"))
        episode_input.textChanged.connect(lambda name: new_episode_button.setEnabled(self.validate_episode_name(name)))
        new_episode_button = QPushButton("New Episode")
        new_episode_button.clicked.connect(lambda: self.create_episode(episode_input.text()))
        new_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(episode_label)
        layout.addWidget(episode_input)
        layout.addWidget(new_episode_button)

        load_episode_button = QPushButton("Load Episode")
        load_episode_button.clicked.connect(self.load_episode)
        layout.addWidget(load_episode_button)
        folderDisplay = QListWidget()
        folderDisplay.addItems(list_episode_folders())
        layout.addWidget(folderDisplay)
        self.setLayout(layout)

    def validate_episode_name(self, name):
        # For now, it only checks that it isn't empty or whitespace. When episode select is implemented, it must check that the name isn't already in use, and also typical file name restrictions
        return len(name.strip()) > 0 

    def create_episode(self, episode_name):
        # Create episode folder.
        create_episode_folder(episode_name)
        self.parent_window.switch_to_editor(episode_name)
        

    def load_episode(self):
        self.parent_window.switch_to_editor()
        # Implement loading episode
        pass