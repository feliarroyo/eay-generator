from ui.episode_editor import EpisodeEditWidget
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget

class MainMenuWidget(QWidget):
    def __init__(self, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window
        self.setWindowTitle("Main Menu")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        new_episode_button = QPushButton("New Episode")
        new_episode_button.clicked.connect(self.open_episode_editor)
        layout.addWidget(new_episode_button)

        load_episode_button = QPushButton("Load Episode")
        load_episode_button.clicked.connect(self.load_episode)
        layout.addWidget(load_episode_button)

        self.setLayout(layout)

    def open_episode_editor(self):
        self.parent_window.switch_to_editor()

    def load_episode(self):
        # Implement loading an episode here
        pass