import os
from core.fileManager import choose_audio_file, save_temp_audio
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
            self.parent_window.edit_prompt_in_index(self.potential_audio_removal)
            
    def select_audio_while_safekeeping_saved_prompt(self):
        source_file_path = choose_audio_file(self)
        if not source_file_path:
            return
        previous_audio_path = self.current_audio_path
        
        self.current_audio_path = save_temp_audio(source_file_path)
        # Save previous audio as potential deletion.
        if previous_audio_path and os.path.exists(previous_audio_path):
            self.potential_audio_removal.append(previous_audio_path)
        self.audio_label.setText(self.tr("Audio loaded: ") + os.path.basename(source_file_path))
    
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.potential_audio_removal = []
        self.setWindowTitle(self.tr("Prompt Editor"))
        self.add_prompt_button.setText(self.tr("Update Prompt"))
        self.add_prompt_button.clicked.disconnect()
        self.add_prompt_button.clicked.connect(lambda: self.update_prompt_if_valid())