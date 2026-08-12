import os
from pathlib import Path
from core.fileManager import choose_audio_file, exists_audio, get_unique_filename, remove_audio, save_temp_audio
from core.models import EAYPrompt
from ui.constants import NO_AUDIO, PROMPT_EDITOR, UPDATE_AUDIOFILE, UPDATE_PROMPT
from ui.prompt_form import CustomDialog, PromptFormWidget

class PromptFormWidget_ForEditor(PromptFormWidget):
    def get_current_prompt(self):
        if self.current_audio_path is not None:
            # If updated audio replaces original audio
            if self.original_audio_path is not None:
                audio_value = os.path.basename(self.original_audio_path)
            # implement a new name for the update file in the moment.
            else:
                audio_value = self.new_name
        else:
            audio_value = None
        return EAYPrompt(
            self.personal_prompt_input.text(),
            self.screen_prompt_input.text(),
            audio_value,
            self.get_suggestions(),
            self.x_checkbox.isChecked(),
            self.us_checkbox.isChecked()
        )
    
    def set_fields(self, prompt):
        """Initialize fields and attributes with the data from the given prompt."""
        self.personal_prompt_input.setText(prompt.personal_question)
        self.screen_prompt_input.setText(prompt.screen_question)
        self.audio_label.setText(prompt.audio if prompt.hasAudio else self.tr(NO_AUDIO))
        self.current_audio_path = prompt.audio if prompt.hasAudio else None
        self.original_audio_path = self.current_audio_path
        self.suggestions_list.clear()
        for suggestion in prompt.suggestions:
            self.suggestions_list.addItem(suggestion)
        self.us_checkbox.setChecked(prompt.us)
        self.x_checkbox.setChecked(prompt.x)
        
    def update_audio_if_needed(self):
        """Manipulates audio files according to flags raised within the editor."""
        # Remove original audio if the remove flag is set and exists.
        if self.remove_flag and self.original_audio_path is not None:
            remove_audio(self.original_audio_path)
        if self.replace_flag:
            # Replace the original audio with the update if it exists.
            if self.original_audio_path is not None and exists_audio(self.original_audio_path):
                remove_audio(self.original_audio_path)
            self.original_audio_path = save_temp_audio("update.ogg", self.new_name)
        # Remove any update audio file that may have been left.
        remove_audio("update.ogg")
        
    def update_prompt_if_valid(self):
            if self.replace_flag and self.original_audio_path is None:
                self.new_name = get_unique_filename()
            else:
                self.new_name = self.original_audio_path
            # Get current prompt data from the form
            prompt = self.get_current_prompt()
            
            # Present dialog if not valid
            if not prompt.is_valid_prompt():
                dlg = CustomDialog()
                dlg.exec()
                return
            self.update_audio_if_needed()
            self.parent_window.edit_prompt_in_index()
            remove_audio("update.ogg")
    
    def select_updated_audio(self):
            """Savekeeps selected audio with an specific name, to replace if update is confirmed."""
            source_file_path = choose_audio_file(self)
            print("Selected audio file: " + str(source_file_path))
            if not source_file_path:
                return
            self.replace_flag = True
            self.current_audio_path = save_temp_audio(source_file_path, UPDATE_AUDIOFILE)
            self.audio_label.setText(self.tr("Audio loaded: ") + os.path.basename(source_file_path))
    
    def set_up_audio_removal(self):
        """Prepares temp environment to remove audio if an update is confirmed"""
        # Set remove flag as true and replace as false.
        if self.current_audio_path is not None and exists_audio(self.current_audio_path):
            self.remove_flag = True
            self.replace_flag = False
            self.current_audio_path = None
        # Remove any update file that may have been originally selected, but not confirmed
        if Path(UPDATE_AUDIOFILE).is_file():
            remove_audio(UPDATE_AUDIOFILE)
        self.audio_label.setText(self.tr(NO_AUDIO))
    
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.remove_flag = False
        self.replace_flag = False
        self.remove_audio_button.clicked.disconnect()
        self.remove_audio_button.clicked.connect(lambda: self.set_up_audio_removal())
        self.setWindowTitle(self.tr(PROMPT_EDITOR))
        self.add_audio_button.clicked.disconnect()
        self.add_audio_button.clicked.connect(lambda: self.select_updated_audio())
        self.add_prompt_button.setText(self.tr(UPDATE_PROMPT))
        self.add_prompt_button.clicked.disconnect()
        self.add_prompt_button.clicked.connect(lambda: self.update_prompt_if_valid())