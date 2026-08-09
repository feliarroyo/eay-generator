from PySide6.QtWidgets import QPushButton, QTableWidget, QTableWidgetItem
from PySide6 import QtCore
from ui.prompt_editor import PromptEditor

class PromptTable(QTableWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.setRowCount(0)
        self.setColumnCount(8)
        self.setHorizontalHeaderLabels([self.tr("Personal Prompt"), self.tr("Screen Prompt"), self.tr("Audio?"), self.tr("Suggestions"), self.tr("Family-Unfriendly?"), self.tr("U.S.-Centric?"), self.tr("Edit"), self.tr("Remove")])
        
        # To size table properly
        self.resizeColumnsToContents()
        total_width = 0
        for col in range(self.columnCount()):
            total_width += self.columnWidth(col)
        scrollbar_buffer = 25
        final_min_width = total_width + scrollbar_buffer
        self.setMinimumWidth(final_min_width)
    
    def open_prompt_editor(self):
        self.prompt_edit_window = PromptEditor(self.parent_window)
        self.prompt_edit_window.set_fields(self.parent_window.prompts[self.currentRow()], self.currentRow())
        self.prompt_edit_window.show()
        self.setEnabled(False)
        self.prompt_edit_window.closeEvent = lambda event: self.setEnabled(True)
    
    def set_prompts_on_table(self, prompts):
        self.clear_table()
        for prompt in prompts:
            self.add_prompt_to_table(prompt)
        
    def add_prompt_to_table(self, prompt, row_position=None):
        # Default value = at the end of the table
        if row_position is None:
            row_position = self.rowCount()
        
        # Define buttons
        edit_button = QPushButton(self.tr("Edit"))
        edit_button.clicked.connect(lambda: self.open_prompt_editor())
        remove_button = QPushButton(self.tr("Remove"))
        remove_button.clicked.connect(lambda: self.parent_window.remove_prompt())
        
        self.insertRow(row_position)
        item = QTableWidgetItem(prompt.personal_question)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 0, item)
        item = QTableWidgetItem(prompt.screen_question)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 1, item)
        item = QTableWidgetItem(self.tr("Yes") if prompt.hasAudio else self.tr("No"))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 2, item)
        item = QTableWidgetItem(", ".join(prompt.suggestions[i] for i in range(len(prompt.suggestions))))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 3, item)
        item = QTableWidgetItem(self.tr("Yes") if prompt.x else self.tr("No"))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 4, item)
        item = QTableWidgetItem(self.tr("Yes") if prompt.us else self.tr("No"))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 5, item)
        self.setCellWidget(row_position, 6, edit_button)
        self.setCellWidget(row_position, 7, remove_button)
    
    def update_prompt_in_table(self, row_position, prompt):
        item = QTableWidgetItem(prompt.personal_question)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 0, item)
        item = QTableWidgetItem(prompt.screen_question)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 1, item)
        item = QTableWidgetItem(self.tr("Yes") if prompt.hasAudio else self.tr("No"))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 2, item)
        item = QTableWidgetItem(", ".join(prompt.suggestions[i] for i in range(len(prompt.suggestions))))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 3, item)
        item = QTableWidgetItem(self.tr("Yes") if prompt.x else self.tr("No"))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 4, item)
        item = QTableWidgetItem(self.tr("Yes") if prompt.us else self.tr("No"))
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        self.setItem(row_position, 5, item)
    
    def remove_prompt_from_table(self):
        currentRow = self.currentRow()
        self.removeRow(currentRow)
        return currentRow

    def clear_table(self):
        self.clearContents()
        self.setRowCount(0)