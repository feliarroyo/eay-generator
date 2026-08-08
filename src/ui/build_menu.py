from PySide6.QtWidgets import QCheckBox, QComboBox, QFileDialog, QLabel, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget

from core.fileManager import generateFibbage3Files, generateFibbage4Files, list_episode_folders, read_episode_prompts, registerPack
from core.models import LANGUAGE_NAMES, VALID_LANGUAGES

class BuildMenuWidget(QWidget):
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle("EAY Generator - Build Episode")
        layout = QVBoxLayout()
        link_game_button = QPushButton(self.tr("Link Game Pack"))
        link_game_button.clicked.connect(lambda: self.link_game_pack())
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
        base_prompt_checkbox = QCheckBox(self.tr("Include base game prompts"))
        layout.addWidget(base_prompt_checkbox)
        episode_label = QLabel(self.tr("Select episodes to include:"))
        layout.addWidget(episode_label)
        episode_checkboxes = [ ]
        episode_display = QListWidget()
        episode_display.setFixedHeight(100)
        episode_display.setSelectionMode(QListWidget.MultiSelection)
        for episode in list_episode_folders():
            episode_display.addItem(episode)
            episode_checkboxes.append(episode)

        # Apply episode button
        generate_build_button = QPushButton(self.tr("Generate Files On Build Folder"))
        generate_build_button.setEnabled(False)
        generate_build_button.clicked.connect(lambda: self.apply_episode(base_prompt_checkbox.isChecked(), episode_display.selectedItems()))
        generate_and_install_button = QPushButton(self.tr("Generate And Install On Game Pack"))
        generate_and_install_button.setEnabled(False)
        generate_and_install_button.clicked.connect(lambda: self.apply_episode(base_prompt_checkbox.isChecked(), episode_display.selectedItems()))
        episode_display.itemSelectionChanged.connect(lambda: generate_build_button.setEnabled(len(episode_display.selectedItems()) > 0))
        episode_display.itemSelectionChanged.connect(lambda: generate_and_install_button.setEnabled(len(episode_display.selectedItems()) > 0)) # TO-DO: Also has to check if game pack was linked
        restore_gamepack_button = QPushButton(self.tr("Restore Game Pack to Original State"))
        restore_gamepack_button.setEnabled(False)
        restore_gamepack_button.clicked.connect(lambda: self.restore_episode()) # TO-DO: Implement action
        
        layout.addWidget(episode_display)
        layout.addWidget(generate_build_button)
        
        layout.addWidget(generate_and_install_button)
        layout.addWidget(restore_gamepack_button)

        self.setLayout(layout)
        
    def link_game_pack(self):
        pack_path = QFileDialog.getExistingDirectory(self, self.tr("Select the game pack directory"))
        if pack_path:
            pack_number = registerPack(pack_path)
            if pack_number:
                QMessageBox.show(self, "Success", f"Game Pack {pack_number} linked successfully.")
            else:
                QMessageBox.critical(self, "Error", "Invalid game pack directory selected.")

    def restore_episode(self):
        pass
    
    def apply_episode(self, include_base_prompts, selected_episodes):
        if not selected_episodes:
            QMessageBox.warning(self, "Warning", "No episodes selected!")
            return
        result_prompts = []
        for episode in selected_episodes:
            result_prompts.extend(read_episode_prompts(episode.text()))
        print(f"Applying episodes: {', '.join([episode.text() for episode in selected_episodes])}")
        # Generate the necessary files for the selected game.
        build_type = self.choose_modding_game_combobox.currentText()
        if build_type == "Fibbage 3":
            success = generateFibbage3Files(result_prompts, include_base_prompts)
        elif build_type.startswith("Fibbage 4"):
            lang = self.choose_modding_game_combobox.currentData()
            success = generateFibbage4Files(result_prompts, include_base_prompts, lang)
            
        if success:
            QMessageBox.information(self, "Success", f"Files generated successfully for {build_type}.")
        else:
            QMessageBox.critical(self, "Failed", f"Build failed for {build_type}.")