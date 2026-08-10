import os
from pathlib import Path
from core.fileManager import choose_audio_file, save_temp_audio
from ui.prompt_form import CustomDialog, PromptFormWidget

class PromptFormWidget_ForEditor(PromptFormWidget):
    def set_fields(self, prompt):
        """Initialize fields and attributes with the data from the given prompt."""
        self.personal_prompt_input.setText(prompt.personal_question)
        self.screen_prompt_input.setText(prompt.screen_question)
        self.audio_label.setText(prompt.audio)
        self.current_audio_path = prompt.audio if prompt.hasAudio else None
        self.original_audio_path = self.current_audio_path
        self.suggestions_list.clear()
        for suggestion in prompt.suggestions:
            self.suggestions_list.addItem(suggestion)
        self.us_checkbox.setChecked(prompt.us)
        self.x_checkbox.setChecked(prompt.x)
        
    def update_audio_if_needed(self):
        """Manipulates audio files according to flags raised within the editor."""
        print("ORIGINAL AUDIO PATH: " + str(self.original_audio_path))
        if self.remove_flag and self.original_audio_path is not None:
            print("CURRENT AUDIO PATH: " + str(self.current_audio_path))
            os.remove(self.original_audio_path)
            self.current_audio_path = None
        if self.replace_flag:
            save_temp_audio("update.ogg", self.current_audio_path)
            os.remove("update.ogg")
        
    def update_prompt_if_valid(self):
            prompt = self.get_current_prompt()
            
            if not prompt.is_valid_prompt():
                dlg = CustomDialog()
                dlg.exec()
                return
            self.update_audio_if_needed()
            self.parent_window.edit_prompt_in_index()
    
    def select_updated_audio(self):
            """Savekeeps selected audio with an specific name, to replace if update is confirmed."""
            SAVEKEEP_AUDIO_NAME = "update.ogg"
            source_file_path = choose_audio_file(self)
            print("Selected audio file: " + str(source_file_path))
            if not source_file_path:
                return
            self.replace_flag = True
            self.current_audio_path = save_temp_audio(source_file_path, SAVEKEEP_AUDIO_NAME)
            self.audio_label.setText(self.tr("Audio loaded: ") + os.path.basename(source_file_path))
    
    def set_up_audio_removal(self):
        if self.current_audio_path is not None and os.path.exists(self.current_audio_path):
            self.remove_flag = True
            self.replace_flag = False
        if Path("update.ogg").is_file():
            os.remove("update.ogg")
        self.audio_label.setText(self.tr("(No audio)"))
        
    
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.remove_flag = False
        self.replace_flag = False
        self.remove_audio_button.clicked.disconnect()
        self.remove_audio_button.clicked.connect(lambda: self.set_up_audio_removal())
        self.setWindowTitle(self.tr("Prompt Editor"))
        self.add_audio_button.clicked.disconnect()
        self.add_audio_button.clicked.connect(lambda: self.select_updated_audio())
        self.add_prompt_button.setText(self.tr("Update Prompt"))
        self.add_prompt_button.clicked.disconnect()
        self.add_prompt_button.clicked.connect(lambda: self.update_prompt_if_valid())