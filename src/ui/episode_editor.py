from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from core.models import EAYCustomEpisode
from core.fileManager import update_temp_episode_file, delete_temp_folder, place_temp_files_on_episode_folder
from ui.prompt_form import PromptFormWidget
from ui.prompt_table import PromptTable


class EpisodeEditWidget(QWidget):

    def save_episode_and_return(self):
        """Generate the episode file, place its contents on the episode folder, and return to the main menu."""
        episode_file = EAYCustomEpisode(self.episode_name, self.prompts)
        update_temp_episode_file(self.episode_name, episode_file)
        place_temp_files_on_episode_folder(self.episode_name)
        self.clear_editor()
        self.parent_window.switch_to_menu()

    def load_episode(self, episode_name, prompts=[]):
        self.episode_name = episode_name
        self.episode_label.setText(self.tr("Episode: ") + episode_name)
        self.prompt_table.set_prompts_on_table(prompts)
        self.prompts = prompts

    def add_prompt_at_the_end(self):
        prompt = self.prompt_form.get_current_prompt()
        self.prompt_table.add_prompt_to_table(prompt)
        self.prompt_form.clear_inputs()  # Clear the input fields after adding the prompt
        self.prompts.append(prompt)
        
    def edit_prompt_in_index(self, index, prompt):
        self.prompts[index] = prompt
        self.prompt_table.update_prompt_in_table(index, prompt)

    def remove_prompt(self):
        currentRow = self.prompt_table.remove_prompt_from_table()
        self.prompts.pop(currentRow)

    def clear_editor(self):
        self.prompt_form.clear_inputs()
        self.prompt_table.clear_table()
        print("Clearing editor and deleting temporary files.")
        delete_temp_folder()
        self.prompts = []

    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.prompts = []
        
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
