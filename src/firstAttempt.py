import tkinter as tk
from tkinter import Menu, Toplevel, ttk
from tkinter import messagebox
import json
from tkinter import filedialog

def load_data():
    path = "data/eayEpisode.json"  # Path to the JSON file
    with open(path, "r") as f:
        data = json.load(f)
        print(data)
    # Load data from a JSON file or database
    list_values = list([
        ("Personal Question", "Screen Question", "Suggestions", "Suggestive?", "U.S.-centric?")
    ])  # Example data
    print(list_values)
    for col_name in list_values[0]:
        table_view.heading(col_name, text=col_name)

    for value_tuple in data["prompts"]:
        table_view.insert('', tk.END, values=[value_tuple['personal'], value_tuple['screen'], value_tuple['suggestions'], value_tuple['x'], value_tuple['us']])

def add_prompt():
    """Adds the prompt to the episode."""
    task = personalquestion_entry.get()  # Get task from the entry field
    if task:
        tasks.append(task)  # Add task to the list
        
        table_view.insert('', tk.END, values=[personalquestion_entry.get(), screenquestion_entry.get(), suggestions_entry.get(), x_variable.get(), us_variable.get()])  # Display task in the treeview
        personalquestion_entry.delete(0, tk.END)  # Clear input field
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")  # Show warning if input is empty
def new_episode():
    """Creates a new file."""
    # Implement the logic for creating a new file
    pass
def open_file():
    pass
def close_file():
    pass
def remove_prompt():
    """Removes selected task from the list."""
    try:
        selected_prompt = table_view.focus()
        print(table_view.item(selected_prompt)['values'])
        # selected_task_index = task_listbox.curselection()[0]  # Get index of selected task
        # task_listbox.delete(selected_task_index)  # Remove task from listbox
        # del tasks[selected_task_index]  # Remove task from the list
        pass
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")  # Show warning if no task is selected
def save_episode():
    remove_prompt()
    return

# Create the main application window
root = tk.Tk()
root.title("EAY Generator")  # Set window title
# root.geometry("300x400")  # Set window size
root.option_add('*tearOff', False)
root.tk.call('tk', 'windowingsystem')

frame = tk.Frame(root)
frame.pack()

# Toolbar
menubar = Menu(root)
menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='Options')
root['menu'] = menubar
menu_file.add_command(label='Create New Episode', command=new_episode)
menu_file.add_command(label='Return to Episode List', command=open_file)
menu_file.add_command(label='Quit', command=close_file)


input_frame = tk.Frame(frame)
input_frame.grid(column=0, row=0, padx=5, pady=5)

# Personal question entry field
personalquestion_frame = tk.LabelFrame(input_frame, text="Personal Question")
personalquestion_frame.grid(column=0, row=0)
personalquestion_entry = tk.Entry(personalquestion_frame, width=30)
personalquestion_entry.insert(0, "Example: What is your favorite color?")
personalquestion_entry.bind("<FocusIn>", lambda e: personalquestion_entry.delete(0, 'end'))
personalquestion_entry.grid(column=0, row=0, padx=5, pady=5)

# Screen question entry field
screenquestion_frame = tk.LabelFrame(input_frame, text="Screen Question" )
screenquestion_frame.grid(column=0, row=1)
screenquestion_entry = tk.Entry(screenquestion_frame, width=30)  # Input field for entering names
screenquestion_entry.insert(0, "Example: <PLAYER>'s favorite color is <BLANK>.")
screenquestion_entry.bind("<FocusIn>", lambda e: screenquestion_entry.delete(0, 'end'))
screenquestion_entry.grid(column=0, row=0, padx=5, pady=5)

# Screen question entry field
suggestions_frame = tk.LabelFrame(input_frame, text="Suggestions")
suggestions_frame.grid(column=0, row=2)
suggestions_entry = tk.Entry(suggestions_frame, width=30)
suggestions_entry.insert(0, "Example:chocolate|bread|banana")
suggestions_entry.bind("<FocusIn>", lambda e: suggestions_entry.delete(0, 'end'))
suggestions_entry.grid(column=0, row=0, padx=5, pady=5)

# Additional settings frame
additionalSettings_frame = tk.LabelFrame(input_frame, text="Additional Settings")
additionalSettings_frame.grid(column=0, row=3)

# Suggestive content
x_variable = tk.BooleanVar()
x_checkbutton = tk.Checkbutton(additionalSettings_frame, text="Mark prompt as suggestive", variable=x_variable)
x_checkbutton.grid(column=0, row=0, padx=5, pady=5)

# US content checkboxes
us_variable = tk.BooleanVar()
us_checkbutton = tk.Checkbutton(additionalSettings_frame, text="Mark prompt as U.S. content", variable=us_variable)
us_checkbutton.grid(column=0, row=1, padx=5, pady=5)

# Button frame
button_frame = tk.Frame(input_frame)
button_frame.grid(column=0, row=4, padx=5, pady=5)
audio_button = tk.Button(button_frame, text="Add Audio", command=lambda: filedialog.askopenfilename(filetypes=[("Audio Files", "*.ogg")]))
audio_button.grid(column=0, row=0, padx=5, pady=5)  # Display the button
add_button = tk.Button(button_frame, text="Add Prompt", command=add_prompt)  # Button to add prompts
add_button.grid(column=1, row=0, padx=5, pady=5)  # Display the button

# Separator
separator = ttk.Separator(input_frame, orient="horizontal")
separator.grid(column=0, row=5, padx=(20, 10), pady=10, sticky="ew")

# Episode name entry field
episode_frame = tk.LabelFrame(input_frame, text="Episode Name")
episode_frame.grid(column=0, row=6)
episode_entry = tk.Entry(episode_frame, width=30)
episode_entry.insert(0, "Example: Friend Group Inside Jokes")
episode_entry.bind("<FocusIn>", lambda e: episode_entry.delete(0, 'end'))
episode_entry.grid(column=0, row=0, padx=5, pady=5)

save_button = tk.Button(input_frame, text="Save Episode", command=save_episode)  # Button to save episode
save_button.grid(column=0, row=7, padx=5, pady=5)  # Display the button

# TreeView frame
table_frame = ttk.Frame(frame)
table_frame.grid(column=1, row=0, padx=5, pady=5)
table_scrollbar = ttk.Scrollbar(table_frame)
table_scrollbar.pack(side="right", fill="y")
cols = ("Personal Question", "Screen Question", "Suggestions", "Suggestive?", "U.S.-centric?")
table_view = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
table_view.column("Personal Question", width=150)
table_view.column("Screen Question", width=150)
table_view.column("Suggestions", width=150)
table_view.column("Suggestive?", width=75)
table_view.column("U.S.-centric?", width=75)
table_view.pack()
table_scrollbar.config(command=table_view.yview)


# List to store tasks
tasks = []  
load_data()

# Run the application
root.mainloop()