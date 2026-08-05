from tkinter import filedialog, messagebox

from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QPushButton, QVBoxLayout, QWidget

from core.fileManager import generateFibbage3Files, generateFibbage4Files, list_episode_folders, read_episode_prompts, registerPack
from core.models import LANGUAGE_NAMES, VALID_LANGUAGES

class BuildMenuWidget(QWidget):
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("EAY Generator - Build Episode")
        layout = QVBoxLayout()
        link_game_button = QPushButton(self.tr("Link Game Pack"))
        link_game_button.clicked.connect(lambda: self.link_game_pack(self.language))
        layout.addWidget(link_game_button)
        choose_modding_game_label = QLabel(self.tr("Choose game to set prompts on:"))
        layout.addWidget(choose_modding_game_label)
        self.choose_modding_game_combobox = QComboBox()
        self.choose_modding_game_combobox.addItem("Fibbage 3")
        for lang in VALID_LANGUAGES:
            text = f"Fibbage 4 - {LANGUAGE_NAMES[VALID_LANGUAGES.index(lang)]}"
            self.choose_modding_game_combobox.addItem(text, lang)
        layout.addWidget(self.choose_modding_game_combobox)
        
        # Checkboxes for episode
        base_prompt_checkbox = QCheckBox(self.tr("Base Prompts"))
        layout.addWidget(base_prompt_checkbox)
        episode_checkboxes = [ ]
        for episode in list_episode_folders():
            checkbox = QCheckBox(f"{episode}")
            layout.addWidget(checkbox)
            episode_checkboxes.append(checkbox)

        # Apply episode button
        generate_files_button = QPushButton(self.tr("Generate Files On Build Folder"))
        generate_files_button.clicked.connect(lambda: self.apply_episode(base_prompt_checkbox.isChecked(), [checkbox for checkbox in episode_checkboxes if checkbox.isChecked()]))
        layout.addWidget(generate_files_button)

        self.setLayout(layout)
        
    def link_game_pack(self):
        pack_path = filedialog.askdirectory(title=self.tr("Select the game pack directory"))
        if pack_path:
            pack_number = registerPack(pack_path)
            if pack_number:
                messagebox.showinfo("Success", f"Game Pack {pack_number} linked successfully.")
            else:
                messagebox.showerror("Error", "Invalid game pack directory selected.")

    def apply_episode(self, include_base_prompts, selected_episodes):
        if not selected_episodes:
            messagebox.showwarning("Warning", "No episodes selected!")
            return
        result_prompts = []
        for episode in selected_episodes:
            result_prompts.extend(read_episode_prompts(episode.text()))
        print(f"Applying episodes: {', '.join([checkbox.text() for checkbox in selected_episodes if checkbox.isChecked()])}")
        # Generate the necessary files for the selected game.
        build_type = self.choose_modding_game_combobox.currentText()
        if build_type == "Fibbage 3":
            generateFibbage3Files(result_prompts, include_base_prompts)
        elif build_type.startswith("Fibbage 4"):
            lang = self.choose_modding_game_combobox.currentData()
            generateFibbage4Files(result_prompts, include_base_prompts, lang)