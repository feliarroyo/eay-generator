import os
from core.fileManager import create_base_folder, get_user_data_path, update_temp_episode_file, list_episode_folders, load_episode_to_temp_folder, read_episode_prompts
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QListWidget, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import QCoreApplication, QEvent, QSettings
from core.assetsManager import change_app_language
from core.models import FIB4_LANGUAGES, PROGRAM_LANGUAGE_NAMES, PROGRAM_LANGUAGES
from ui.build_menu import BuildMenuWidget
create_base_folder()  # Ensure the base folder exists

class MainMenuWidget(QWidget):
    def __init__(self, parent_window, parent=None):
        super().__init__(parent)
        self.parent_window = parent_window
        self.parent_window.setWindowTitle(self.tr("EAY Generator"))

        layout = QVBoxLayout()
        self.language_label = QLabel(self.tr("Select Language"))
        layout.addWidget(self.language_label)
        self.language_combobox = QComboBox()
        for index, lang in enumerate(PROGRAM_LANGUAGES):
            text = PROGRAM_LANGUAGE_NAMES[index]
            self.language_combobox.addItem(text, lang)
        settings = QSettings("EAYModding", "EAYGenerator")
        self.language_combobox.setCurrentIndex(PROGRAM_LANGUAGES.index(settings.value("language", "en")))
        self.language_combobox.currentIndexChanged.connect(lambda index: self.change_language(self.language_combobox.itemData(index)))
        
        layout.addWidget(self.language_combobox)
        # self.toggle_lang_button = QPushButton(self.tr("Cambiar idioma a español"))
        # self.toggle_lang_button.clicked.connect(lambda: self.toggle_language())
        # layout.addWidget(self.toggle_lang_button)
        self.episode_label = QLabel(self.tr("Episode Name"))
        layout.addWidget(self.episode_label)
        self.episode_input = QLineEdit()
        self.episode_input.setPlaceholderText(self.tr("e.g. Inside Jokes"))
        self.episode_input.textChanged.connect(lambda name: self.new_episode_button.setEnabled(self.validate_episode_name(name)))
        layout.addWidget(self.episode_input)
        self.new_episode_button = QPushButton(self.tr("Create New Episode"))
        self.new_episode_button.clicked.connect(lambda: self.create_episode(self.episode_input.text()))
        self.new_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(self.new_episode_button)

        self.edit_episode_button = QPushButton(self.tr("Edit Selected Episode"))
        self.edit_episode_button.clicked.connect(lambda: self.load_episode(self.folder_display.currentItem().text()))
        self.edit_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(self.edit_episode_button)
        self.delete_episode_button = QPushButton(self.tr("Delete Selected Episode"))
        self.delete_episode_button.clicked.connect(lambda: self.delete_episode(self.folder_display.currentItem().text()))
        self.delete_episode_button.setEnabled(False)  # Disable the button by default
        layout.addWidget(self.delete_episode_button)
        self.refresh_folders_button = QPushButton(self.tr("Refresh Episode List"))
        self.refresh_folders_button.clicked.connect(self.update_folder_display)
        layout.addWidget(self.refresh_folders_button)
        self.folder_display = QListWidget()
        self.folder_display.setFixedHeight(100)
        self.update_folder_display()
        self.folder_display.currentItemChanged.connect(self.update_buttons)
        layout.addWidget(self.folder_display)
        self.language = "en"
        self.open_folder_button = QPushButton(self.tr("Open Episode Folder"))
        episode_path = get_user_data_path() / "episodes"
        self.open_folder_button.clicked.connect(lambda: os.startfile(episode_path))
        layout.addWidget(self.open_folder_button)
        self.apply_episodes_button = QPushButton(self.tr("Apply Custom Episodes"))
        layout.addWidget(self.apply_episodes_button)
        self.apply_episodes_button.clicked.connect(lambda: self.open_build_menu())
        self.setLayout(layout)
        parent_window.setFixedSize(layout.sizeHint().width(), layout.sizeHint().height())

    def change_language(self, lang_code):
        app = QCoreApplication.instance()
        change_app_language(app, lang_code)
        self.retranslate_ui()
        
    def validate_episode_name(self, name):
        # For now, it only checks that it isn't empty or whitespace. When episode select is implemented, it must check that the name isn't already in use, and also typical file name restrictions
        episode_name = name.strip()
        return len(episode_name) > 0 and (episode_name not in list_episode_folders())

    def create_episode(self, episode_name):
        update_temp_episode_file(episode_name)
        self.episode_input.clear()
        self.parent_window.switch_to_editor(episode_name, [])

    def load_episode(self, episode_name):
        load_episode_to_temp_folder(episode_name)
        self.parent_window.switch_to_editor(episode_name, read_episode_prompts(episode_name))
        
    def delete_episode(self, episode_name):
        episode_path = get_user_data_path() / "episodes" / episode_name
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

    def retranslate_ui(self):
        """Retranslate UI from main window to impose translation."""
        self.language_label.setText(self.tr("Select Language"))
        self.episode_label.setText(self.tr("Episode Name"))
        self.episode_input.setPlaceholderText(self.tr("e.g. Inside Jokes"))
        self.new_episode_button.setText(self.tr("Create New Episode"))
        self.edit_episode_button.setText(self.tr("Edit Selected Episode"))
        self.delete_episode_button.setText(self.tr("Delete Selected Episode"))
        self.refresh_folders_button.setText(self.tr("Refresh Episode List"))
        self.open_folder_button.setText(self.tr("Open Episode Folder"))
        self.apply_episodes_button.setText(self.tr("Apply Custom Episodes"))
        self.window().setWindowTitle(self.tr("EAY Generator"))

    def changeEvent(self, event):
        """Qt automatically calls this when a global event happens."""
        # Catch the language change broadcast
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()
            
        # Always call the parent class's changeEvent so PySide doesn't break!
        super().changeEvent(event)