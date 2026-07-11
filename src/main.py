from posixpath import basename
import sys
from tkinter import filedialog
from PySide6.QtWidgets import QApplication, QCheckBox, QLabel, QLineEdit, QListWidget, QMainWindow, QPushButton, QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QSize

class Prompt:
    def __init__(self, personal_question, screen_question, audio,suggestions, x, us):
        self.personal_question = personal_question
        self.screen_question = screen_question
        self.hasAudio = audio is not "(No audio)"
        self.audio = audio
        self.suggestions = suggestions
        self.x = x
        self.us = us
    def get_prompt_data(self):
        return {
            "personalQuestion": self.personal_question,
            "screenQuestion": self.screen_question,
            "hasAudio": self.hasAudio,
            "audio": self.audio,
            "suggestions": self.suggestions,
            "x": self.x,
            "us": self.us
        }
    def has_audio(self):
        return self.hasAudio

class MainWindow(QMainWindow):
    def add_suggestion(self, suggestions_list, suggestion_input):
        suggestions_list.addItem(suggestion_input.text())
        suggestion_input.clear()
    def save_episode(self, episodeName, prompts):
        print("Length: " + str(len(prompts)))
        episode_file = {
            "episodeName": episodeName,
            "audioCount": 0, # add logic later
            "prompts": []
        }
        for prompt in prompts:
            prompt_data = prompt.get_prompt_data()
            episode_file["audioCount"] += 1 if prompt.has_audio() else 0
            episode_file["prompts"].append(prompt_data)
        print(episode_file)

    def __init__(self):
        super().__init__()
        prompts = []
        self.setWindowTitle("My App")
        layout = QVBoxLayout()
        
        # Toolbar
        # toolbar = QToolBar()
        # self.addToolBar(toolbar)
        button_new = QAction(QIcon("assets/plus.png"), "Create New Episode", self)
        button_new.setStatusTip("Start a new episode")
        # button_action.triggered.connect(...) The current episode will be lost. Are you sure?
        # toolbar.addAction(button_new)
        button_save = QAction(QIcon("assets/disk.png"), "Save Current Episode", self)
        button_save.setStatusTip("Save the current episode")
        button_save.triggered.connect(lambda: self.save_episode(episode_input.text(), prompts))
        # toolbar.addAction(button_save)
        button_mainmenu = QAction(QIcon("assets/arrow-circle-225.png"), "Return to Main Menu", self)
        button_mainmenu.setStatusTip("Return to the main menu")
        # button_action.triggered.connect(...) The current episode will be lost. Are you sure?
        # toolbar.addAction(button_mainmenu)
        # toolbar.setIconSize(QSize(16, 16))
        self.setStatusBar(QStatusBar(self))
        # Submenus
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_new)
        file_menu.addAction(button_save)
        file_menu.addAction(button_mainmenu)
        help_menu = menu.addMenu("&Help")
        help_menu.addAction(QAction(QIcon("assets/question-frame.png"), "About", self))
        
        # Personal Prompt
        personal_prompt_label = QLabel("Personal Prompt")
        personal_prompt_input = QLineEdit()
        personal_prompt_input.setPlaceholderText("e.g. What is your favorite color?")
        
        # Screen Prompt
        screen_prompt_label = QLabel("Screen Prompt")
        screen_prompt_input = QLineEdit()
        screen_prompt_input.setPlaceholderText("e.g. <PLAYER>'s favorite color is <BLANK>.")
        add_player_button = QPushButton("Insert Player Name into the Prompt")
        add_player_button.clicked.connect(lambda: screen_prompt_input.insert("<PLAYER>"))
        add_blank_button = QPushButton("Insert Blank into the Prompt")
        add_blank_button.clicked.connect(lambda: screen_prompt_input.insert("<BLANK>"))
        
        # Audio
        audio_label = QLabel("(No audio)")
        add_audio_button = QPushButton("Add audio to current prompt (.ogg only)")
        add_audio_button.clicked.connect(lambda: self.select_audio(audio_label))
        add_audio_button.setCheckable(True) # This should have the select_audio value
        
        
        # Suggestions
        suggestions_label = QLabel("Suggestions")
        suggestions_input = QLineEdit()
        suggestions_input.setPlaceholderText("e.g. chocolate")
        suggestions_input.returnPressed.connect(lambda: self.add_suggestion(suggestions_list, suggestions_input))
        remove_suggestion_button = QPushButton("Remove Suggestion")
        remove_suggestion_button.setEnabled(False)
        remove_suggestion_button.clicked.connect(lambda: [suggestions_list.takeItem(suggestions_list.currentRow()), remove_suggestion_button.setEnabled(False)])
        suggestions_list = QListWidget()
        suggestions_list.currentItemChanged.connect(lambda: remove_suggestion_button.setEnabled(True))
        # Checkboxes
        us_checkbox = QCheckBox("Mark as U.S.-Centric Prompt")
        x_checkbox = QCheckBox("Mark as Not Family-Friendly Prompt")
        
        # Table widget
        prompt_table = QTableWidget()
        prompt_table.setRowCount(0)
        prompt_table.setColumnCount(8)
        prompt_table.setHorizontalHeaderLabels(["Personal Prompt", "Screen Prompt", "Audio", "Suggestions", "Family-Friendly?", "U.S.-Centric?", "Edit", "Remove"])

        # Episode Name
        episode_label = QLabel("Episode Name")
        episode_input = QLineEdit()
        episode_input.setPlaceholderText("Example: Inside Jokes")
        
        add_prompt_button = QPushButton("Add Prompt")
        add_prompt_button.clicked.connect(lambda: prompts.append(self.add_prompt(prompt_table, personal_prompt_input, screen_prompt_input, audio_label, suggestions_list, us_checkbox, x_checkbox, prompts)))
        
        save_episode_button = QPushButton("Save Episode and Return to Main Menu")
        save_episode_button.setCheckable(True)
        save_episode_button.clicked.connect(lambda: self.save_episode(episode_input.text(), prompts))


        
        layout.addWidget(episode_label)
        layout.addWidget(episode_input)
        layout.addWidget(personal_prompt_label)
        layout.addWidget(personal_prompt_input)
        layout.addWidget(screen_prompt_label)
        layout.addWidget(screen_prompt_input)
        layout.addWidget(add_player_button)
        layout.addWidget(add_blank_button)
        layout.addWidget(audio_label)
        layout.addWidget(add_audio_button)
        layout.addWidget(suggestions_label)
        layout.addWidget(suggestions_input)
        layout.addWidget(remove_suggestion_button)
        layout.addWidget(suggestions_list)
        layout.addWidget(us_checkbox)
        layout.addWidget(x_checkbox)
        layout.addWidget(add_prompt_button)
        layout.addWidget(prompt_table) 
        layout.addWidget(save_episode_button) 
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def select_audio(self, audio_label):
        filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.ogg")])
        if filename:
            audio_label.setText(basename(filename))

    def edit_row(self, prompt_table, row):
        pass

    def add_prompt(self, prompt_table, personal_prompt_input, screen_prompt_input, audio_label, suggestions_list, us_checkbox, x_checkbox, prompts):
        # Get the values from the input fields
        personal_prompt = personal_prompt_input.text()
        screen_prompt = screen_prompt_input.text()
        audio = audio_label.text()
        suggestions = [suggestions_list.item(i).text() for i in range(suggestions_list.count())]
        family_friendly = us_checkbox.isChecked()
        us_centric = x_checkbox.isChecked()
        

        # Define buttons
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(lambda: self.edit_row(prompt_table, prompt_table.currentRow()))
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_prompt(prompt_table, prompts))

        # Add the prompt to the table
        row_position = prompt_table.rowCount()
        prompt_table.insertRow(row_position)
        prompt_table.setItem(row_position, 0, QTableWidgetItem(personal_prompt))
        prompt_table.setItem(row_position, 1, QTableWidgetItem(screen_prompt))
        prompt_table.setItem(row_position, 2, QTableWidgetItem(audio))
        prompt_table.setItem(row_position, 3, QTableWidgetItem(", ".join(suggestions_list.item(i).text() for i in range(suggestions_list.count()))))
        prompt_table.setItem(row_position, 4, QTableWidgetItem("Yes" if family_friendly else "No"))
        prompt_table.setItem(row_position, 5, QTableWidgetItem("Yes" if us_centric else "No"))
        prompt_table.setCellWidget(row_position, 6, edit_button)
        prompt_table.setCellWidget(row_position, 7, remove_button)
        # print(personal_prompt, screen_prompt, audio, [suggestions_list.item(i).text() for i in range(suggestions_list.count())], x_checkbox.isChecked(), us_checkbox.isChecked())
        
        personal_prompt_input.clear()
        screen_prompt_input.clear()
        suggestions_list.clear()
        audio_label.setText("(No audio)")
        
        return Prompt(
            personal_prompt,
            screen_prompt,
            audio,
            suggestions,
            x_checkbox.isChecked(),
            us_checkbox.isChecked()
        )
    
    def remove_prompt(self, prompt_table, prompts):
        currentRow = prompt_table.currentRow()
        prompts.pop(currentRow)
        prompt_table.removeRow(currentRow)
        
    
    
    def generate_episode(self, episode_name, prompts):
        pass

app = QApplication(sys.argv)

window = MainWindow()

window.show()

app.exec()