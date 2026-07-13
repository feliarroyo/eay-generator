from PySide6.QtWidgets import QVBoxLayout, QWidget

from ui.prompt_form_editor import PromptFormWidget_ForEditor

class PromptEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.form = PromptFormWidget_ForEditor(self)
        layout.addWidget(self.form)
        self.setLayout(layout)
        
    def set_fields(self, prompt, id):
        self.currentPromptId = id
        self.form.set_fields(prompt)
        
    def update_prompt(self, prompt):
        # Update the prompt with the values from the form
        prompt.personal_question = self.form.personal_prompt_input.text()
        prompt.screen_question = self.form.screen_prompt_input.text()
        prompt.audio = self.form.audio_label.text()
        prompt.suggestions = [self.form.suggestions_list.item(i).text() for i in range(self.form.suggestions_list.count())]
        prompt.us = self.form.us_checkbox.isChecked()
        prompt.x = self.form.x_checkbox.isChecked()