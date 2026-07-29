import os
from core.fileManager import create_base_folder, create_episode_folder, list_episode_folders, read_episode_prompts
from PySide6.QtWidgets import QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget
from ui.build_menu import BuildMenuWidget
create_base_folder()  # Ensure the base folder exists

class MainMenuWidget(QWidget):
    def __init__(self, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window
        self.parent_window.setWindowTitle("EAY Generator")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        episode_label = QLabel(self.tr("Episode Name"))
        episode_input = QLineEdit()
        episode_input.setPlaceholderText(self.tr("e.g. Inside Jokes"))
        episode_input.textChanged.connect(lambda name: new_episode_button.setEnabled(self.validate_episode_name(name)))
        new_episode_button = QPushButton(self.tr("Create New Episode"))
        new_episode_button.clicked.connect(lambda: self.create_episode(episode_input.text()))
        new_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(episode_label)
        layout.addWidget(episode_input)
        layout.addWidget(new_episode_button)

        self.edit_episode_button = QPushButton(self.tr("Edit Selected Episode"))
        self.edit_episode_button.clicked.connect(lambda: self.load_episode(self.folder_display.currentItem().text()))
        
        layout.addWidget(self.edit_episode_button)
        self.delete_episode_button = QPushButton(self.tr("Delete Selected Episode"))
        self.delete_episode_button.clicked.connect(lambda: self.delete_episode(self.folder_display.currentItem().text()))
        self.delete_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(self.delete_episode_button)
        self.folder_display = QListWidget()
        self.update_folder_display()
        self.folder_display.currentItemChanged.connect(self.update_buttons)
        layout.addWidget(self.folder_display)
        self.language = "en"
        open_folder_button = QPushButton(self.tr("Open Episode Folder"))
        open_folder_button.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), "episodes")))
        layout.addWidget(open_folder_button)
        apply_episodes_button = QPushButton(self.tr("Apply Custom Episodes"))
        layout.addWidget(apply_episodes_button)
        apply_episodes_button.clicked.connect(lambda: self.open_build_menu())
        self.setLayout(layout)

    def validate_episode_name(self, name):
        # For now, it only checks that it isn't empty or whitespace. When episode select is implemented, it must check that the name isn't already in use, and also typical file name restrictions
        return len(name.strip()) > 0 

    def create_episode(self, episode_name):
        # Create episode folder.
        create_episode_folder(episode_name)
        self.parent_window.switch_to_editor(episode_name)        

    def load_episode(self, episode_name):
        self.parent_window.switch_to_editor(episode_name, read_episode_prompts(episode_name))
        
    def delete_episode(self, episode_name):
        episode_path = os.path.join(os.getcwd(), "episodes", episode_name)
        if os.path.exists(episode_path):
            import shutil
            shutil.rmtree(episode_path)
            print(f"Episode folder '{episode_name}' deleted.")
            self.update_folder_display()
        else:
            print(f"Episode folder '{episode_name}' does not exist.")
    
    def update_folder_display(self):
        self.folder_display.clear()
        self.folder_display.addItems(list_episode_folders())
    
    def update_buttons(self, current):
        value = current is not None        
        self.delete_episode_button.setEnabled(value)
        self.edit_episode_button.setEnabled(value)
        
    def open_build_menu(self):
            self.build_menu = BuildMenuWidget(self.parent_window)
            self.build_menu.show()
            self.setEnabled(False)
            self.build_menu.closeEvent = lambda event: self.setEnabled(True)
