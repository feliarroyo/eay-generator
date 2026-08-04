from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from core.models import EAYCustomEpisode
from core.fileManager import create_episode_folder, delete_unused_audios, remove_temp_session_folder
from ui.prompt_form import PromptFormWidget
from ui.prompt_table import PromptTable


class EpisodeEditWidget(QWidget):

    def save_episode_and_return(self):
        print("Length: " + str(len(self.prompts)))
        episode_file = EAYCustomEpisode(self.episode_name, self.prompts)
        create_episode_folder(self.episode_name, episode_file)
        self.prompt_form.clear_inputs()
        self.clear_prompts()
        delete_unused_audios(self.potential_audio_removal)
        remove_temp_session_folder()
        self.parent_window.switch_to_menu()

    def load_episode(self, episode_name, prompts=[]):
        self.episode_name = episode_name
        self.episode_label.setText(self.tr("Episode: ") + episode_name)
        self.prompt_table.set_prompts_on_table(prompts)
        self.prompts = prompts
        self.potential_audio_removal = []

    def add_prompt_at_the_end(self):
        prompt = self.prompt_form.get_current_prompt()
        self.prompt_table.add_prompt_to_table(prompt)
        self.prompt_form.clear_inputs()  # Clear the input fields after adding the prompt
        self.prompts.append(prompt)
        
    def edit_prompt_in_index(self, index, prompt, potential_audio_removal):
        self.prompts[index] = prompt
        self.prompt_table.update_prompt_in_table(index, prompt)
        self.potential_audio_removal.extend(potential_audio_removal)

    def remove_prompt(self):
        currentRow = self.prompt_table.remove_prompt_from_table()
        self.prompts.pop(currentRow)

    def clear_prompts(self):
        self.prompt_table.clear_table()
        self.prompts = []

    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.prompts = []
        self.potential_audio_removal = []
        
        # Save Button
        self.episode_label = QLabel(self.tr("Episode: (No episode loaded)"))
        self.save_episode_button = QPushButton(
            self.tr("Save Episode and Return to Main Menu")
        )
        self.save_episode_button.setCheckable(True)
        self.save_episode_button.clicked.connect(lambda: self.save_episode_and_return())
        
        # Prompt Form
        self.prompt_form = PromptFormWidget(self)

        # Table widget
        self.prompt_table = PromptTable(self)

        layout = QVBoxLayout()
        mainLayout = QHBoxLayout()
        layout.addWidget(self.episode_label)
        layout.addWidget(self.save_episode_button)
        mainLayout.addWidget(self.prompt_form, 1)
        mainLayout.addWidget(self.prompt_table, 3)
        layout.addLayout(mainLayout)
        self.setLayout(layout)
