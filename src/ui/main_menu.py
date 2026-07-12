from core.folderManagement import create_base_folder, create_episode_folder
from ui.episode_editor import EpisodeEditWidget
from PySide6.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget

create_base_folder()  # Ensure the base folder exists

class MainMenuWidget(QWidget):
    def __init__(self, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window
        self.setWindowTitle("Main Menu")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        episode_name_edit = QLineEdit()
        episode_name_edit.setPlaceholderText("Enter episode name")
        episode_name_edit.textChanged.connect(lambda name: new_episode_button.setEnabled(self.validate_episode_name(name)))
        new_episode_button = QPushButton("New Episode")
        new_episode_button.clicked.connect(lambda: self.create_episode(episode_name_edit.text()))
        new_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(episode_name_edit)
        layout.addWidget(new_episode_button)

        load_episode_button = QPushButton("Load Episode")
        load_episode_button.clicked.connect(self.load_episode)
        layout.addWidget(load_episode_button)

        self.setLayout(layout)

    def validate_episode_name(self, name):
        # For now, it only checks that it isn't empty or whitespace. When episode select is implemented, it must check that the name isn't already in use, and also typical file name restrictions
        return len(name.strip()) > 0 

    def create_episode(self, episode_name):
        # Create episode folder.
        create_episode_folder(episode_name)
        self.parent_window.switch_to_editor()
        

    def load_episode(self):
        self.parent_window.switch_to_editor()
        # Implement loading episode
        pass