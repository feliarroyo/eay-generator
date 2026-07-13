import os
from core.fileManager import create_base_folder, create_episode_folder, list_episode_folders, read_episode_prompts
from PySide6.QtWidgets import QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget

create_base_folder()  # Ensure the base folder exists

class MainMenuWidget(QWidget):
    def __init__(self, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window
        self.parent_window.setWindowTitle("EAY Generator")
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

        edit_episode_button = QPushButton("Edit Episode")
        edit_episode_button.clicked.connect(lambda: self.load_episode(self.folder_display.currentItem().text()))
        edit_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(edit_episode_button)
        self.folder_display = QListWidget()
        self.update_folder_display()
        self.folder_display.currentItemChanged.connect(lambda: edit_episode_button.setEnabled(True))
        layout.addWidget(self.folder_display)
        
        open_folder_button = QPushButton("Open Episode Folder")
        open_folder_button.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), "episodes")))
        layout.addWidget(open_folder_button)
        self.setLayout(layout)

    def validate_episode_name(self, name):
        # For now, it only checks that it isn't empty or whitespace. When episode select is implemented, it must check that the name isn't already in use, and also typical file name restrictions
        return len(name.strip()) > 0 

    def create_episode(self, episode_name):
        # Create episode folder.
        create_episode_folder(episode_name)
        self.parent_window.switch_to_editor(episode_name)
        

    def load_episode(self, episode_name):
        self.parent_window.switch_to_editor(episode_name, read_episode_prompts(episode_name))
    
    def update_folder_display(self):
        self.folder_display.clear()
        self.folder_display.addItems(list_episode_folders())
