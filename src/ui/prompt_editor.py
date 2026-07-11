from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.prompt_form import PromptFormWidget

class PromptEditor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.form = PromptFormWidget(self)
        layout.addWidget(self.form)
        self.setLayout(layout)