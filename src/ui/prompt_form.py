import os
import shutil
import uuid
from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QLabel, QLineEdit, QListWidget, QPushButton,  QVBoxLayout, QWidget, QFileDialog
from core.models import Prompt
from core.fileManager import choose_audio_file, save_temp_audio

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
        audio_value = self.current_audio_path if self.current_audio_path is not None else "(No audio)"
        # Get the values from the input fields
        return Prompt(
            self.personal_prompt_input.text(),
            self.screen_prompt_input.text(),
            audio_value,
            self.get_suggestions(),
            self.x_checkbox.isChecked(),
            self.us_checkbox.isChecked()
        )

    def select_audio(self):
        source_file_path = choose_audio_file(self)
        if not source_file_path:
            return
        previous_audio_path = self.current_audio_path
        self.current_audio_path = save_temp_audio(source_file_path)
        # Delete previous audio, if any
        if previous_audio_path is not None and os.path.exists(previous_audio_path):
            os.remove(previous_audio_path)
        self.audio_label.setText(self.tr("Audio loaded: ") + os.path.basename(source_file_path))
    
    def add_suggestion_to_list(self):
        self.suggestions_list.addItem(self.suggestions_input.text())
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
        self.audio_label.setText("(No audio)")
        self.suggestions_list.clear()
        self.us_checkbox.setChecked(False)
        self.x_checkbox.setChecked(False)
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        layout = QVBoxLayout()
        
        # Personal Prompt
        self.personal_prompt_label = QLabel(self.tr("Personal Prompt"))
        self.personal_prompt_label.setToolTip(self.tr("(Required Field)\nThis is the question that will be asked to the player in question on their device at the start."))
        self.personal_prompt_input = QLineEdit()
        self.personal_prompt_input.setPlaceholderText(self.tr("e.g. What is your favorite color?"))
        
        # Screen Prompt
        self.screen_prompt_label = QLabel(self.tr("Screen Prompt"))
        self.screen_prompt_label.setToolTip(self.tr("(Required Field)\nThis is the question that will be shown to other players when coming up with lies, and will also be shown on screen alongside everyone's answers."))
        self.screen_prompt_input = QLineEdit()
        self.screen_prompt_input.setPlaceholderText(self.tr("e.g. <PLAYER>'s favorite color is <BLANK>."))
        self.add_player_button = QPushButton(self.tr("Insert Player Name into the Prompt"))
        self.add_player_button.setToolTip(self.tr("Inserts the <PLAYER> placeholder into the prompt, which will be replaced with the player's name when the prompt is displayed."))
        self.add_player_button.clicked.connect(lambda: self.screen_prompt_input.insert("<PLAYER>"))
        self.add_blank_button = QPushButton(self.tr("Insert Blank into the Prompt"))
        self.add_blank_button.setToolTip(self.tr("Inserts the <BLANK> placeholder into the prompt, which will be replaced with a blank when the prompt is displayed."))
        self.add_blank_button.clicked.connect(lambda: self.screen_prompt_input.insert("<BLANK>"))
        
        # Audio
        self.audio_label = QLabel("(No audio)")
        self.current_audio_path = None
        self.add_audio_button = QPushButton(self.tr("Set audio for current prompt (.ogg only)"))
        self.add_audio_button.clicked.connect(lambda: self.select_audio())
        self.remove_audio_button = QPushButton(self.tr("Remove audio for current prompt"))
        
        # Suggestions
        self.suggestions_label = QLabel(self.tr("Suggestions"))
        self.suggestions_label.setToolTip(self.tr("Dummy answers, used for Audience Lies in both games, as well as Jackbox Lies and Lie For Me button on Fibbage 4 only.")) # Unknown if required or not so far, nor how many are needed if so (8-10?).
        self.suggestions_input = QLineEdit()
        self.suggestions_input.setPlaceholderText(self.tr("e.g. chocolate"))
        self.suggestions_input.returnPressed.connect(lambda: self.add_suggestion_to_list())
        self.remove_suggestion_button = QPushButton(self.tr("Remove Suggestion"))
        self.remove_suggestion_button.setEnabled(False)
        self.remove_suggestion_button.clicked.connect(lambda: [self.suggestions_list.takeItem(self.suggestions_list.currentRow()), self.remove_suggestion_button.setEnabled(self.suggestions_list.count() != 0)])
        self.suggestions_list = QListWidget()
        self.suggestions_list.currentItemChanged.connect(lambda: self.remove_suggestion_button.setEnabled(True))
        # Checkboxes
        self.us_checkbox = QCheckBox(self.tr("Mark as U.S.-Centric Prompt"))
        self.us_checkbox.setToolTip(self.tr("Check this box if the prompt is specific to U.S. culture, and should be removed when playing using the U.S. filter in compatible games."))
        self.x_checkbox = QCheckBox(self.tr("Mark as Not Family-Friendly Prompt"))
        self.x_checkbox.setToolTip(self.tr("Check this box if the prompt is not family-friendly, and should be removed when playing using the Family-Friendly Filter in compatible games."))
        # Add Prompt Button
        self.add_prompt_button = QPushButton(self.tr("Add Prompt"))
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