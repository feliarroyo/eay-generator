from PySide6.QtWidgets import QCheckBox, QComboBox, QFileDialog, QLabel, QListWidget, QMessageBox, QPushButton, QVBoxLayout, QWidget

from core.fileManager import generateFibbage3Files, generateFibbage4Files, get_linked_game_pack_path, list_episode_folders, registerPack
from core.models import LANGUAGE_NAMES, VALID_LANGUAGES
from ui.constants import APP_TITLE_BUILD, CHOOSE_GAME, ERROR, FIBBAGE_3, FIBBAGE_4, GENERATE_AND_INSTALL, GENERATE_AND_INSTALL_TIP, GENERATE_ON_BUILD, GENERATE_ON_BUILD_TIP, INCLUDE_BASE_PROMPTS, INVALID_GAMEPACK_MESSAGE, LINK_GAME_DESCRIPTION, NO_EPISODE_MESSAGE, NO_PACK_MESSAGE, REVERT_CHANGES, REVERT_CHANGES_TIP, SELECT_EPISODES, SELECT_GAMEPACK, SELECT_PACK, SUCCESS, WARNING

class BuildMenuWidget(QWidget):
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle(self.tr(APP_TITLE_BUILD))
        layout = QVBoxLayout()
        link_game_label = QLabel(self.tr(LINK_GAME_DESCRIPTION))
        layout.addWidget(link_game_label)
        link_game_button = QPushButton(self.tr(SELECT_PACK))
        link_game_button.clicked.connect(lambda: self.link_game_pack())
        layout.addWidget(link_game_button)
        choose_modding_game_label = QLabel(self.tr(CHOOSE_GAME))
        layout.addWidget(choose_modding_game_label)
        self.choose_modding_game_combobox = QComboBox()
        self.choose_modding_game_combobox.addItem(FIBBAGE_3)
        for lang in VALID_LANGUAGES:
            text = f"Fibbage 4 - {LANGUAGE_NAMES[VALID_LANGUAGES.index(lang)]}"
            self.choose_modding_game_combobox.addItem(text, lang)
        layout.addWidget(self.choose_modding_game_combobox)
        
        # Checkboxes for episode
        base_prompt_checkbox = QCheckBox(self.tr(INCLUDE_BASE_PROMPTS))
        layout.addWidget(base_prompt_checkbox)
        episode_label = QLabel(self.tr(SELECT_EPISODES))
        layout.addWidget(episode_label)
        episode_checkboxes = [ ]
        episode_display = QListWidget()
        episode_display.setFixedHeight(100)
        episode_display.setSelectionMode(QListWidget.MultiSelection)
        for episode in list_episode_folders():
            episode_display.addItem(episode)
            episode_checkboxes.append(episode)

        # Apply episode button
        generate_build_button = QPushButton(self.tr(GENERATE_ON_BUILD))
        generate_build_button.setEnabled(False)
        generate_build_button.setToolTip(self.tr(GENERATE_ON_BUILD_TIP))
        generate_build_button.clicked.connect(lambda: self.build_episode(base_prompt_checkbox.isChecked(), episode_display.selectedItems()))
        generate_and_install_button = QPushButton(self.tr(GENERATE_AND_INSTALL))
        generate_and_install_button.setEnabled(False)
        generate_and_install_button.setToolTip(self.tr(GENERATE_AND_INSTALL_TIP))
        generate_and_install_button.clicked.connect(lambda: self.build_and_apply_episode(base_prompt_checkbox.isChecked(), episode_display.selectedItems()))
        episode_display.itemSelectionChanged.connect(lambda: generate_build_button.setEnabled(len(episode_display.selectedItems()) > 0))
        episode_display.itemSelectionChanged.connect(lambda: generate_and_install_button.setEnabled(len(episode_display.selectedItems()) > 0)) # TO-DO: Also has to check if game pack was linked
        
        layout.addWidget(episode_display)
        layout.addWidget(generate_build_button)
        layout.addWidget(generate_and_install_button)
        revert_changes_button = QPushButton(self.tr(REVERT_CHANGES))
        revert_changes_button.setToolTip(self.tr(REVERT_CHANGES_TIP))
        revert_changes_button.clicked.connect()
        layout.addWidget(revert_changes_button)

        self.setLayout(layout)
        
    def link_game_pack(self):
        """Save the relevant game pack path in a text file for future use."""
        pack_path = QFileDialog.getExistingDirectory(self, self.tr(SELECT_GAMEPACK))
        if pack_path:
            pack_number = registerPack(pack_path)
            if pack_number:
                QMessageBox.information(self, SUCCESS, f"Game Pack {pack_number} linked successfully.")
            else:
                QMessageBox.critical(self, ERROR, INVALID_GAMEPACK_MESSAGE)
    
    def build_and_apply_episode(self, include_base_prompts, selected_episodes):
        if not selected_episodes:
            QMessageBox.warning(self, self.tr(WARNING), self.tr(NO_EPISODE_MESSAGE))
            return
        build_type = self.choose_modding_game_combobox.currentText()
        if build_type == FIBBAGE_3:
            pack_number = 4
        elif build_type.startswith(FIBBAGE_4):
            pack_number = 9
        game_path = get_linked_game_pack_path(pack_number)
        if game_path is not None:
            self.build_episode(include_base_prompts, selected_episodes, game_path)
        else:
            QMessageBox.critical(self, self.tr(ERROR), self.tr(NO_PACK_MESSAGE))
    
    def build_episode(self, include_base_prompts, selected_episodes, build_path=None):
        if not selected_episodes:
            QMessageBox.warning(self, self.tr(WARNING), self.tr(NO_EPISODE_MESSAGE))
            return
        # Generate the necessary files for the selected game.
        build_type = self.choose_modding_game_combobox.currentText()
        if build_type == FIBBAGE_3:
            success = generateFibbage3Files(selected_episodes, include_base_prompts) if build_path is None else generateFibbage3Files(selected_episodes, include_base_prompts, build_path)
        elif build_type.startswith(FIBBAGE_4):
            lang = self.choose_modding_game_combobox.currentData()
            success = generateFibbage4Files(selected_episodes, include_base_prompts, lang) if build_path is None else generateFibbage4Files(selected_episodes, include_base_prompts, lang, build_path)
            
        if success:
            QMessageBox.information(self, SUCCESS, f"Files generated successfully for {build_type}.")
        else:
            QMessageBox.critical(self, ERROR, f"Build failed for {build_type}.")