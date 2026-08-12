from PySide6.QtWidgets import QCheckBox, QComboBox, QFileDialog, QLabel, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget

from core.fileManager import generateFibbage3Files, generateFibbage4Files, get_linked_game_pack_path, list_episode_folders, registerPack
from core.models import LANGUAGE_NAMES, VALID_LANGUAGES

class BuildMenuWidget(QWidget):
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle(self.tr("EAY Generator - Build Episode"))
        layout = QVBoxLayout()
        link_game_label = QLabel(self.tr("You need to choose a game pack to:\n - Include base prompts\n - Apply episodes directly into the game\n - Revert changes"))
        layout.addWidget(link_game_label)
        link_game_button = QPushButton(self.tr("Select Party Pack Folder"))
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
        generate_build_button.setToolTip(self.tr("Generates the necessary files for the selected game in the build folder. You can then manually copy them to the game pack."))
        generate_build_button.clicked.connect(lambda: self.build_episode(base_prompt_checkbox.isChecked(), episode_display.selectedItems()))
        generate_and_install_button = QPushButton(self.tr("Generate And Install On Game Pack"))
        generate_and_install_button.setEnabled(False)
        generate_and_install_button.setToolTip(self.tr("Generates the necessary files for the selected game and installs them directly into the linked game pack."))
        generate_and_install_button.clicked.connect(lambda: self.build_and_apply_episode(base_prompt_checkbox.isChecked(), episode_display.selectedItems()))
        episode_display.itemSelectionChanged.connect(lambda: generate_build_button.setEnabled(len(episode_display.selectedItems()) > 0))
        episode_display.itemSelectionChanged.connect(lambda: generate_and_install_button.setEnabled(len(episode_display.selectedItems()) > 0)) # TO-DO: Also has to check if game pack was linked
        
        layout.addWidget(episode_display)
        layout.addWidget(generate_build_button)
        layout.addWidget(generate_and_install_button)
        revert_changes_button = QPushButton(self.tr("Revert Changes"))
        revert_changes_button.setToolTip(self.tr("Reverts all changes made to the game pack by restoring the original files obtained from the backup."))
        revert_changes_button.clicked.connect()
        layout.addWidget(revert_changes_button)

        self.setLayout(layout)
        
    def link_game_pack(self):
        """Save the relevant game pack path in a text file for future use."""
        pack_path = QFileDialog.getExistingDirectory(self, self.tr("Select the game pack directory"))
        if pack_path:
            pack_number = registerPack(pack_path)
            if pack_number:
                QMessageBox.information(self, "Success", f"Game Pack {pack_number} linked successfully.")
            else:
                QMessageBox.critical(self, "Error", "Invalid game pack directory selected.")
    
    def build_and_apply_episode(self, include_base_prompts, selected_episodes):
        if not selected_episodes:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("No episodes selected!"))
            return
        build_type = self.choose_modding_game_combobox.currentText()
        if build_type == "Fibbage 3":
            pack_number = 4
        elif build_type.startswith("Fibbage 4"):
            pack_number = 9
        game_path = get_linked_game_pack_path(pack_number)
        if game_path is not None:
            self.build_episode(include_base_prompts, selected_episodes, game_path)
        else:
            QMessageBox.critical(self, self.tr("Error"), self.tr("No game pack linked for the selected game. Please link a game pack first."))
    
    def build_episode(self, include_base_prompts, selected_episodes, build_path=None):
        if not selected_episodes:
            QMessageBox.warning(self, self.tr("Warning"), self.tr("No episodes selected!"))
            return
        # Generate the necessary files for the selected game.
        build_type = self.choose_modding_game_combobox.currentText()
        if build_type == "Fibbage 3":
            success = generateFibbage3Files(selected_episodes, include_base_prompts) if build_path is None else generateFibbage3Files(selected_episodes, include_base_prompts, build_path)
        elif build_type.startswith("Fibbage 4"):
            lang = self.choose_modding_game_combobox.currentData()
            success = generateFibbage4Files(selected_episodes, include_base_prompts, lang) if build_path is None else generateFibbage4Files(selected_episodes, include_base_prompts, lang, build_path)
            
        if success:
            QMessageBox.information(self, "Success", f"Files generated successfully for {build_type}.")
        else:
            QMessageBox.critical(self, "Failed", f"Build failed for {build_type}.")