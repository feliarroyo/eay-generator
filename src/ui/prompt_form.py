from posixpath import basename
import sys
from tkinter import filedialog
from PySide6.QtWidgets import QCheckBox, QDialog, QDialogButtonBox, QLabel, QLineEdit, QListWidget, QMainWindow, QPushButton,  QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize

from core.models import Prompt

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
         # Get the values from the input fields
        return Prompt(
            self.personal_prompt_input.text(),
            self.screen_prompt_input.text(),
            self.audio_label.text(),
            self.get_suggestions(),
            self.x_checkbox.isChecked(),
            self.us_checkbox.isChecked()
        )

    def select_audio(self):
        pass # Will handle audio later
        # filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.ogg")])
        # if filename:
        #     self.audio_label.setText(basename(filename))
    
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
        self.personal_prompt_input = QLineEdit()
        self.personal_prompt_input.setPlaceholderText(self.tr("e.g. What is your favorite color?"))
        
        # Screen Prompt
        self.screen_prompt_label = QLabel(self.tr("Screen Prompt"))
        self.screen_prompt_input = QLineEdit()
        self.screen_prompt_input.setPlaceholderText(self.tr("e.g. <PLAYER>'s favorite color is <BLANK>."))
        self.add_player_button = QPushButton(self.tr("Insert Player Name into the Prompt"))
        self.add_player_button.clicked.connect(lambda: self.screen_prompt_input.insert("<PLAYER>"))
        self.add_blank_button = QPushButton(self.tr("Insert Blank into the Prompt"))
        self.add_blank_button.clicked.connect(lambda: self.screen_prompt_input.insert("<BLANK>"))
        
        # Audio
        self.audio_label = QLabel("(No audio)")
        self.add_audio_button = QPushButton(self.tr("Set audio for current prompt (.ogg only)"))
        self.add_audio_button.clicked.connect(lambda: self.select_audio())
        
        # Suggestions
        self.suggestions_label = QLabel(self.tr("Suggestions"))
        self.suggestions_input = QLineEdit()
        self.suggestions_input.setPlaceholderText(self.tr("e.g. chocolate"))
        self.suggestions_input.returnPressed.connect(lambda: self.add_suggestion_to_list())
        self.remove_suggestion_button = QPushButton(self.tr("Remove Suggestion"))
        self.remove_suggestion_button.setEnabled(False)
        self.remove_suggestion_button.clicked.connect(lambda: [self.suggestions_list.takeItem(self.suggestions_list.currentRow()), self.remove_suggestion_button.setEnabled(False)])
        self.suggestions_list = QListWidget()
        self.suggestions_list.currentItemChanged.connect(lambda: self.remove_suggestion_button.setEnabled(True))
        # Checkboxes
        self.us_checkbox = QCheckBox(self.tr("Mark as U.S.-Centric Prompt"))
        self.x_checkbox = QCheckBox(self.tr("Mark as Not Family-Friendly Prompt"))
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
        layout.addWidget(self.suggestions_label)
        layout.addWidget(self.suggestions_input)
        layout.addWidget(self.remove_suggestion_button)
        layout.addWidget(self.suggestions_list)
        layout.addWidget(self.us_checkbox)
        layout.addWidget(self.x_checkbox)
        layout.addWidget(self.add_prompt_button)
        self.setLayout(layout)