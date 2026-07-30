from tkinter import filedialog

from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget

from core.fileManager import list_episode_folders, registerPack
from core.models import LANGUAGE_NAMES, VALID_LANGUAGES

class BuildMenuWidget(QWidget):
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        layout = QVBoxLayout()
        link_game_button = QPushButton(self.tr("Link Game Pack"))
        link_game_button.clicked.connect(lambda: self.link_game_pack(self.language))
        layout.addWidget(link_game_button)
        choose_modding_game_label = QLabel(self.tr("Choose game to set prompts on:"))
        layout.addWidget(choose_modding_game_label)
        choose_modding_game_combobox = QComboBox()
        choose_modding_game_combobox.addItem("Fibbage 3")
        for lang in VALID_LANGUAGES:
            choose_modding_game_combobox.addItem(f"Fibbage 4 - {LANGUAGE_NAMES[VALID_LANGUAGES.index(lang)]}")
        # choose_modding_game_combobox.currentTextChanged.connect(lambda lang: setattr(self, 'language', lang))
        layout.addWidget(choose_modding_game_combobox)
        
        # Checkboxes for episode
        episode_checkboxes = []
        for episode in list_episode_folders():
            checkbox = QCheckBox(f"{episode}")
            layout.addWidget(checkbox)
            episode_checkboxes.append(checkbox)

        # Apply episode button
        apply_episode_button = QPushButton(self.tr("Apply Episode"))
        apply_episode_button.clicked.connect(lambda: self.apply_episode(episode_checkboxes))
        layout.addWidget(apply_episode_button)

        self.setLayout(layout)
        
    def link_game_pack(self):
        pack_path = filedialog.askdirectory(title=self.tr("Select the game pack directory"))
        if pack_path:
            pack_number = registerPack(pack_path)
            if pack_number:
                print(f"Game Pack {pack_number} linked successfully.")
            else:
                print("Invalid game pack directory selected.")