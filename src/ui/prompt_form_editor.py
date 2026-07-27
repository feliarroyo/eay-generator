from posixpath import basename
import sys
from tkinter import filedialog
from PySide6.QtWidgets import QCheckBox, QLabel, QLineEdit, QListWidget, QMainWindow, QPushButton,  QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize

from core.models import Prompt
from ui.prompt_form import CustomDialog, PromptFormWidget

class PromptFormWidget_ForEditor(PromptFormWidget):
    def set_fields(self, prompt):
        self.personal_prompt_input.setText(prompt.personal_question)
        self.screen_prompt_input.setText(prompt.screen_question)
        self.audio_label.setText(prompt.audio)
        self.suggestions_list.clear()
        for suggestion in prompt.suggestions:
            self.suggestions_list.addItem(suggestion)
        self.us_checkbox.setChecked(prompt.us)
        self.x_checkbox.setChecked(prompt.x)
        
    def update_prompt_if_valid(self):
            prompt = self.get_current_prompt()
            if not prompt.is_valid_prompt():
                dlg = CustomDialog()
                dlg.exec()
                return
            self.parent_window.edit_prompt_in_index()
    
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.add_prompt_button.setText("Update Prompt")
        self.add_prompt_button.clicked.disconnect()
        self.add_prompt_button.clicked.connect(lambda: self.update_prompt_if_valid())