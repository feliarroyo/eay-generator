from posixpath import basename
import sys
from tkinter import filedialog
from PySide6.QtWidgets import QCheckBox, QLabel, QLineEdit, QListWidget, QMainWindow, QPushButton,  QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize

from core.models import Prompt

class PromptFormWidget(QWidget):
    def add_suggestion(self, suggestions_list, suggestion_input):
        suggestions_list.addItem(suggestion_input.text())
        suggestion_input.clear()
    def select_audio(self, audio_label):
        filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.ogg")])
        if filename:
            audio_label.setText(basename(filename))

    def add_prompt(self, prompt_table, personal_prompt_input, screen_prompt_input, audio_label, suggestions_list, us_checkbox, x_checkbox, prompts):
        # Get the values from the input fields
        personal_prompt = personal_prompt_input.text()
        screen_prompt = screen_prompt_input.text()
        audio = audio_label.text()
        suggestions = [suggestions_list.item(i).text() for i in range(suggestions_list.count())]
        family_friendly = us_checkbox.isChecked()
        us_centric = x_checkbox.isChecked()
        
        personal_prompt_input.clear()
        screen_prompt_input.clear()
        suggestions_list.clear()
        audio_label.setText("(No audio)")
        
        return Prompt(
            personal_prompt,
            screen_prompt,
            audio,
            suggestions,
            x_checkbox.isChecked(),
            us_checkbox.isChecked()
        )
    
    def remove_prompt(self, prompt_table, prompts):
        currentRow = prompt_table.currentRow()
        prompts.pop(currentRow)
        prompt_table.removeRow(currentRow)
        
    
    
    def generate_episode(self, episode_name, prompts):
        pass
    
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.prompts = []
        layout = QVBoxLayout()
        
        # Personal Prompt
        personal_prompt_label = QLabel("Personal Prompt")
        personal_prompt_input = QLineEdit()
        personal_prompt_input.setPlaceholderText("e.g. What is your favorite color?")
        
        # Screen Prompt
        screen_prompt_label = QLabel("Screen Prompt")
        screen_prompt_input = QLineEdit()
        screen_prompt_input.setPlaceholderText("e.g. <PLAYER>'s favorite color is <BLANK>.")
        add_player_button = QPushButton("Insert Player Name into the Prompt")
        add_player_button.clicked.connect(lambda: screen_prompt_input.insert("<PLAYER>"))
        add_blank_button = QPushButton("Insert Blank into the Prompt")
        add_blank_button.clicked.connect(lambda: screen_prompt_input.insert("<BLANK>"))
        
        # Audio
        audio_label = QLabel("(No audio)")
        add_audio_button = QPushButton("Add audio to current prompt (.ogg only)")
        add_audio_button.clicked.connect(lambda: self.select_audio(audio_label))
        add_audio_button.setCheckable(True) # This should have the select_audio value
        
        
        # Suggestions
        suggestions_label = QLabel("Suggestions")
        suggestions_input = QLineEdit()
        suggestions_input.setPlaceholderText("e.g. chocolate")
        suggestions_input.returnPressed.connect(lambda: self.add_suggestion(suggestions_list, suggestions_input))
        remove_suggestion_button = QPushButton("Remove Suggestion")
        remove_suggestion_button.setEnabled(False)
        remove_suggestion_button.clicked.connect(lambda: [suggestions_list.takeItem(suggestions_list.currentRow()), remove_suggestion_button.setEnabled(False)])
        suggestions_list = QListWidget()
        suggestions_list.currentItemChanged.connect(lambda: remove_suggestion_button.setEnabled(True))
        # Checkboxes
        us_checkbox = QCheckBox("Mark as U.S.-Centric Prompt")
        x_checkbox = QCheckBox("Mark as Not Family-Friendly Prompt")

        add_prompt_button = QPushButton("Add Prompt")
        # add_prompt_button.clicked.connect(lambda: self.prompts.append(self.add_prompt(prompt_table, personal_prompt_input, screen_prompt_input, audio_label, suggestions_list, us_checkbox, x_checkbox, self.prompts)))

        layout.addWidget(personal_prompt_label)
        layout.addWidget(personal_prompt_input)
        layout.addWidget(screen_prompt_label)
        layout.addWidget(screen_prompt_input)
        layout.addWidget(add_player_button)
        layout.addWidget(add_blank_button)
        layout.addWidget(audio_label)
        layout.addWidget(add_audio_button)
        layout.addWidget(suggestions_label)
        layout.addWidget(suggestions_input)
        layout.addWidget(remove_suggestion_button)
        layout.addWidget(suggestions_list)
        layout.addWidget(us_checkbox)
        layout.addWidget(x_checkbox)
        layout.addWidget(add_prompt_button)
        self.setLayout(layout)