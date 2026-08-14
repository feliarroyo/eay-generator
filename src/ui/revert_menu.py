from core.fileManager import get_linked_game_pack_path, restore_fibbage_3, restore_fibbage_4
from core.models import LANGUAGE_NAMES, FIB4_LANGUAGES
from PySide6.QtWidgets import QComboBox, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget
class RevertMenuWidget(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setWindowTitle(self.tr("EAY Generator - Revert Changes"))
        layout = QVBoxLayout()
        revert_label = QLabel(self.tr("Choose the game pack you want to revert to its original state:"))
        layout.addWidget(revert_label)
        self.choose_revert_game_combobox = QComboBox()
        self.choose_revert_game_combobox.addItem("Fibbage 3")
        for lang in FIB4_LANGUAGES:
            text = f"Fibbage 4 - {LANGUAGE_NAMES[FIB4_LANGUAGES.index(lang)]}"
            self.choose_revert_game_combobox.addItem(text, lang)
        layout.addWidget(self.choose_revert_game_combobox)
        revert_changes_button = QPushButton(self.tr("Revert Changes"))
        revert_changes_button.setToolTip(self.tr("Reverts all changes made to the game pack by restoring the original files obtained from the backup."))
        revert_changes_button.clicked.connect(self.revert_changes)
        layout.addWidget(revert_changes_button)

        self.setLayout(layout)
    
    def revert_changes(self):
        build_type = self.choose_revert_game_combobox.currentText()
        if build_type == "Fibbage 3":
            pack_number = 4
        elif build_type.startswith("Fibbage 4"):
            pack_number = 9
        game_path = get_linked_game_pack_path(pack_number)
        if game_path is not None:
            if pack_number == 4:
                success = restore_fibbage_3()
            elif pack_number == 9:
                lang = self.choose_revert_game_combobox.currentData()
                success = restore_fibbage_4(lang)
            else:
                QMessageBox.critical(self, self.tr("Error"), self.tr("Unsupported game pack number."))
                return
            if success:
                QMessageBox.information(self, self.tr("Success"), self.tr("Changes reverted successfully!"))
            else:
                QMessageBox.critical(self, self.tr("Error"), self.tr("The current game (language) has not been linked, so there is no backup to restore changes."))
        else:
            QMessageBox.critical(self, self.tr("Error"), self.tr("The current game (language) has not been linked, so there is no backup to restore changes."))