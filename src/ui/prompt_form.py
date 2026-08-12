import os
import shutil
import uuid
from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QLabel, QLineEdit, QListWidget, QPushButton,  QVBoxLayout, QWidget
from PySide6.QtGui import QIcon, Qt
from core.models import EAYPrompt
from core.fileManager import choose_audio_file, save_temp_audio
from ui.constants import ADD_AUDIO, ADD_BLANK, ADD_BLANK_TIP, ADD_PLAYER, ADD_PLAYER_TIP, ADD_PROMPT, ASSET_KEY, AUDIO_LOADED, BLANK_SYMBOL, NO_AUDIO, NOT_FAMILY_PROMPT, NOT_FAMILY_PROMPT_TIP, PERSONAL_PROMPT, PERSONAL_PROMPT_EXAMPLE, PERSONAL_PROMPT_TIP, PLAYER_SYMBOL, REMOVE_AUDIO, REMOVE_SUGGESTION, SCREEN_PROMPT, SCREEN_PROMPT_EXAMPLE, SCREEN_PROMPT_TIP, SUGGESTIONS, SUGGESTIONS_EXAMPLE, SUGGESTIONS_TIP, US_PROMPT, US_PROMPT_TIP

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Error: Invalid Prompt")

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        layout = QVBoxLayout()
        message = QLabel("The prompt is missing required fields or has no suggestions.")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class PromptFormWidget(QWidget):
    def get_current_prompt(self):
        audio_value = os.path.basename(self.current_audio_path) if self.current_audio_path is not None else None
        # Get the values from the input fields
        return EAYPrompt(
            self.personal_prompt_input.text(),
            self.screen_prompt_input.text(),
            audio_value,
            self.get_suggestions(),
            self.x_checkbox.isChecked(),
            self.us_checkbox.isChecked()
        )

    def select_audio(self):
        source_file_path = choose_audio_file(self)
        print("Selected audio file: " + str(source_file_path))
        if not source_file_path:
            return
        previous_audio_path = None
        if self.current_audio_path:
            previous_audio_path = os.path.basename(self.current_audio_path)
        self.current_audio_path = save_temp_audio(source_file_path, previous_audio_path)
        # Delete previous audio, if any
        if previous_audio_path is not None and os.path.exists(previous_audio_path):
            os.remove(previous_audio_path)
        self.audio_label.setText(self.tr(AUDIO_LOADED))
        
    def remove_audio(self):
        if self.current_audio_path is not None and os.path.exists(self.current_audio_path):
            os.remove(self.current_audio_path)
        self.current_audio_path = None
        self.audio_label.setText(self.tr(NO_AUDIO))
    
    def add_suggestion_to_list(self):
        suggestion = self.suggestions_input.text().strip()
        
        if len(suggestion) > 0 and (suggestion not in self.get_suggestions()):
            self.suggestions_list.addItem(suggestion)
        self.suggestions_input.clear()
        
    def get_suggestions(self):
        return [
            self.suggestions_list.item(i).text()
            for i in range(self.suggestions_list.count())
        ]
        
    def add_prompt_if_valid(self):
        prompt = self.get_current_prompt()
        if not prompt.is_valid_prompt():
            dlg = CustomDialog()
            dlg.exec()
            return
        self.parent_window.add_prompt_at_the_end()

    def clear_inputs(self):
        self.personal_prompt_input.clear()
        self.screen_prompt_input.clear()
        self.audio_label.setText(self.tr(NO_AUDIO))
        self.current_audio_path = None
        self.suggestions_list.clear()
        self.us_checkbox.setChecked(False)
        self.x_checkbox.setChecked(False)
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        layout = QVBoxLayout()
        
        # Personal Prompt
        self.personal_prompt_label = QLabel(self.tr(PERSONAL_PROMPT))
        self.personal_prompt_label.setToolTip(self.tr(PERSONAL_PROMPT_TIP))
        self.personal_prompt_input = QLineEdit()
        self.personal_prompt_input.setPlaceholderText(self.tr(PERSONAL_PROMPT_EXAMPLE))
        
        # Screen Prompt
        self.screen_prompt_label = QLabel(self.tr(SCREEN_PROMPT))
        self.screen_prompt_label.setToolTip(self.tr(SCREEN_PROMPT_TIP))
        self.screen_prompt_input = QLineEdit()
        self.screen_prompt_input.setPlaceholderText(self.tr(SCREEN_PROMPT_EXAMPLE))
        self.add_player_button = QPushButton(self.tr(ADD_PLAYER))
        self.add_player_button.setToolTip(self.tr(ADD_PLAYER_TIP))
        self.add_player_button.clicked.connect(lambda: self.screen_prompt_input.insert(PLAYER_SYMBOL))
        self.add_player_button.setFocusPolicy(Qt.NoFocus)
        self.add_blank_button = QPushButton(self.tr(ADD_BLANK))
        self.add_blank_button.setToolTip(self.tr(ADD_BLANK_TIP))
        self.add_blank_button.clicked.connect(lambda: self.screen_prompt_input.insert(BLANK_SYMBOL))
        self.add_blank_button.setFocusPolicy(Qt.NoFocus)
        
        # Audio
        self.audio_label = QLabel(self.tr(NO_AUDIO))
        self.current_audio_path = None
        self.add_audio_button = QPushButton(self.tr(ADD_AUDIO))
        self.add_audio_button.clicked.connect(lambda: self.select_audio())
        self.remove_audio_button = QPushButton(self.tr(REMOVE_AUDIO))
        self.remove_audio_button.clicked.connect(lambda: self.remove_audio())
        
        # Suggestions
        self.suggestions_label = QLabel(self.tr(SUGGESTIONS))
        self.suggestions_label.setToolTip(self.tr(SUGGESTIONS_TIP)) # Unknown if required or not so far, nor how many are needed if so (8-10?).
        self.suggestions_input = QLineEdit()
        self.suggestions_input.setPlaceholderText(self.tr(SUGGESTIONS_EXAMPLE))
        key_icon = QIcon(ASSET_KEY)
        browse_action = self.suggestions_input.addAction(key_icon, QLineEdit.TrailingPosition)
        browse_action.triggered.connect(lambda: self.add_suggestion_to_list())
        self.suggestions_input.returnPressed.connect(lambda: self.add_suggestion_to_list())
        self.remove_suggestion_button = QPushButton(self.tr(REMOVE_SUGGESTION))
        self.remove_suggestion_button.setEnabled(False)
        self.remove_suggestion_button.clicked.connect(lambda: [self.suggestions_list.takeItem(self.suggestions_list.currentRow()), self.remove_suggestion_button.setEnabled(self.suggestions_list.count() != 0)])
        self.suggestions_list = QListWidget()
        self.suggestions_list.currentItemChanged.connect(lambda: self.remove_suggestion_button.setEnabled(True))
        # Checkboxes
        self.us_checkbox = QCheckBox(self.tr(US_PROMPT))
        self.us_checkbox.setToolTip(self.tr(US_PROMPT_TIP))
        self.x_checkbox = QCheckBox(self.tr(NOT_FAMILY_PROMPT))
        self.x_checkbox.setToolTip(self.tr(NOT_FAMILY_PROMPT_TIP))
        # Add Prompt Button
        self.add_prompt_button = QPushButton(self.tr(ADD_PROMPT))
        self.add_prompt_button.clicked.connect(lambda: self.add_prompt_if_valid())
        
        # Add elements to layout
        layout.addWidget(self.personal_prompt_label)
        layout.addWidget(self.personal_prompt_input)
        layout.addWidget(self.screen_prompt_label)
        layout.addWidget(self.screen_prompt_input)
        layout.addWidget(self.add_player_button)
        layout.addWidget(self.add_blank_button)
        layout.addWidget(self.audio_label)
        layout.addWidget(self.add_audio_button)
        layout.addWidget(self.remove_audio_button)
        layout.addWidget(self.suggestions_label)
        layout.addWidget(self.suggestions_input)
        layout.addWidget(self.remove_suggestion_button)
        layout.addWidget(self.suggestions_list)
        layout.addWidget(self.us_checkbox)
        layout.addWidget(self.x_checkbox)
        layout.addWidget(self.add_prompt_button)
        self.setLayout(layout)