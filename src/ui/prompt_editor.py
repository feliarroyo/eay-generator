from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui.prompt_form_editor import PromptFormWidget_ForEditor

class PromptEditor(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        layout = QVBoxLayout()
        self.form = PromptFormWidget_ForEditor(self)
        layout.addWidget(self.form)
        self.setLayout(layout)
        
    def set_fields(self, prompt, id):
        self.currentPromptId = id
        self.form.set_fields(prompt)
        
    def edit_prompt_in_index(self, potential_audio_removal):
        self.parent_window.edit_prompt_in_index(self.currentPromptId, self.form.get_current_prompt(), potential_audio_removal)
        self.close()