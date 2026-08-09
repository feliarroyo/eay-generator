import json
import os
from posixpath import basename
import shutil
from PySide6.QtWidgets import QFileDialog, QMessageBox
import uuid

from core.models import VALID_LANGUAGES, EAYCustomEpisode, EAYPrompt, fib3EAYTemplate, fib3EAYTemplate_Data, fib4EAYTemplate, fib4EAYTemplate_Data

current_file_dir = os.path.dirname(os.path.abspath(__file__))
root_project_dir = os.path.abspath(os.path.join(current_file_dir, "..", ".."))
base_path = os.path.join(root_project_dir, "episodes")
backup_path = os.path.join(root_project_dir, "backup")
app_build_path = os.path.join(root_project_dir, "build")
temp_path = os.path.join(root_project_dir, ".temp_session")

def create_base_folder():
    """Creates the base folder for episodes if it doesn't exist."""
    if not os.path.exists(base_path):
        os.makedirs(base_path)

def update_temp_episode_file(episode_name, content=None):
    """Creates a new folder for the episode with the given name and base file."""
    os.makedirs(temp_path, exist_ok=True)
    
    if content is None:
        content = EAYCustomEpisode(episode_name, [])
    # move_audio_to_episode_folder(temp_path, content)
    # content.remove_temp_reference(temp_path)
    # print(content)
    # print(content.to_dict())
    json.dump(content.to_dict(), open(os.path.join(temp_path, "episode.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    
def place_temp_files_on_episode_folder(episode_name):
    """Moves the contents of the temporary session folder to the episode directory."""
    original_path = os.path.join(base_path, episode_name)
    if not os.path.exists(original_path):
        os.makedirs(original_path)
    backup_path = original_path + ".bak"
    
    if os.path.exists(original_path):
        os.rename(original_path, backup_path)
        shutil.move(temp_path, original_path)
        if os.path.exists(backup_path):
            shutil.rmtree(backup_path)            

def list_episode_folders():
    folderList = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    return folderList

def choose_audio_file(self):
    source_file_path = QFileDialog.getOpenFileName(self, self.tr("Select Audio File"), "", self.tr("Audio Files (*.ogg)"))
    return source_file_path[0]

def delete_temp_folder():
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print(f"Temporary folder '{temp_path}' deleted.")

def remove_temp_session_folder():
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print(f"Temporary session folder '{temp_path}' deleted.")

def save_temp_audio(audio_path, previous_audio_name=None):
    os.makedirs(temp_path, exist_ok=True)
    # Generate a unique name for the copy to avoid same-name conflicts
    if previous_audio_name:
        unique_filename = previous_audio_name
    else:
        unique_filename = f"{uuid.uuid4().hex[:8]}.ogg"
    temp_file_path = os.path.join(temp_path, unique_filename)
    # Copy the file into the staging area
    print(f"Copying audio file '{audio_path}' to temporary session folder as '{temp_file_path}'.")
    shutil.copy2(audio_path, temp_file_path)
    return temp_file_path

def load_episode_to_temp_folder(episode_name):
    episode_path = os.path.join(base_path, episode_name)
    # Copy folder to .temp_session
    if not os.path.exists(episode_path):
        print(f"No episode folder found for '{episode_name}'.")
        return
    
    shutil.copytree(episode_path, temp_path, dirs_exist_ok=True)
    

def read_episode_prompts(episode_name):
    """Reads the prompts from the episode.json file in the specified episode folder."""
    episode_path = os.path.join(base_path, episode_name)
    episode_file_path = os.path.join(episode_path, "episode.json")
    
    if not os.path.exists(episode_file_path):
        print(f"No episode file found for '{episode_name}'.")
        return []
    
    with open(episode_file_path, 'r', encoding='utf-8') as f:
        episode_data = json.load(f)
    
    prompts_data = episode_data.get("prompts", [])
    prompts = [EAYPrompt(p["personal_question"], p["screen_question"], p["audio"], p["suggestions"], p["x"], p["us"]) for p in prompts_data]
    return prompts

def checkPackDirectory(path):
    """Checks if the provided path is a valid game pack directory for either Pack 4 or Pack 9."""
    # PACK 4
    jpp4_base = "./games/Fibbage3/content"
    # PACK 9
    jpp9_base = "./games/Fibbage4/content"
    
    if os.path.isdir(os.path.join(path, jpp4_base)):
        return 4
    if os.path.isdir(os.path.join(path, jpp9_base)):
        return 9
    return False

def registerPack(path):
    """Save a backup of the game pack directory."""
    pack_number = checkPackDirectory(path)
    if not pack_number:
        print(f"Invalid game pack directory: {path}")
        return None
    
    # Save the game path on a text file for later use
    with open(os.path.join(root_project_dir, f"game_pack_{pack_number}.txt"), 'w') as f:
        f.write(path)
    
    # Create a backup of the game contents.
    if pack_number == 4:
        backupFibbage3(path)
    if pack_number == 9:
        backupFibbage4(path)
    print(f"Game Pack {pack_number} registered successfully.")
    return pack_number

def get_linked_game_pack_path(pack_number):
        """Return the path of the previously linked game pack."""
        path_file = os.path.join(root_project_dir, f"game_pack_{pack_number}.txt")
        if not os.path.exists(path_file):
            return None

        with open(os.path.join(root_project_dir, f"game_pack_{pack_number}.txt"), 'r') as f:
            return f.read().strip()

def backupFibbage3(path):
    """"Backups the contents of the path passed to the function, which should be the Fibbage 3 game pack directory."""
    jpp4_jet = os.path.join(path, "games/Fibbage3/content/tmishortie.jet")
    print (jpp4_jet)
    jpp4_folder = os.path.join(path, "games/Fibbage3/content/tmishortie")
    print (jpp4_folder)
    print (os.path.join(backup_path, "games/Fibbage3/content/tmishortie.jet"))
    os.makedirs(os.path.dirname(os.path.join(backup_path, "games/Fibbage3/content/tmishortie")), exist_ok=True)
    shutil.copy2(jpp4_jet, os.path.join(backup_path, "games/Fibbage3/content/tmishortie.jet"))
    shutil.copytree(jpp4_folder, os.path.join(backup_path, "games/Fibbage3/content/tmishortie"), dirs_exist_ok=True)
    pass

def backupFibbage4(path):
    """"Backups the contents of the path passed to the function, which should be the Fibbage 4 game pack directory."""
    for lang in VALID_LANGUAGES:
        jpp9_jet = os.path.join(path, f"games/Fibbage4/content/{lang}/eayblankie.jet")
        jpp9_folder = os.path.join(path, f"games/Fibbage4/content/{lang}/eayblankie")
        os.makedirs(os.path.dirname(os.path.join(backup_path, f"./games/Fibbage4/content/{lang}/eayblankie")), exist_ok=True)
        shutil.copy2(jpp9_jet, os.path.join(backup_path, f"./games/Fibbage4/content/{lang}/eayblankie.jet"))
        shutil.copytree(jpp9_folder, os.path.join(backup_path, f"./games/Fibbage4/content/{lang}/eayblankie"), dirs_exist_ok=True)

def generateFibbageFiles(selected_episodes, base_folder_structure, shortieFileType, dataFileType, fileName, build_path=app_build_path, include_base_prompts=False):
    """Generates the proper files for Enough About You games."""
    # Empty build folder if building on app folder
    if os.path.exists(build_path) and build_path == app_build_path:
        shutil.rmtree(build_path)
    # Create root directory for the files
    target_path = os.path.join(build_path, base_folder_structure)
    os.makedirs(target_path, exist_ok=True)
    
    # Read episode prompts from the selected episodes and create a shortie element
    episode_prompts = []
    for episode in selected_episodes:
        episode_prompts.extend(read_episode_prompts(episode.text()))
    tmi_shortie = shortieFileType(episode_prompts).to_dict()
    
    # Include base prompts files and data if requested
    if include_base_prompts:
        # Check backup is valid
        if not backup_path or not os.path.exists(backup_path):
            print("Warning: Base game backup not found!")
            return False
        # Read base game main file from backup
        main_jet_path = os.path.join(backup_path, base_folder_structure, fileName + ".jet")
        with open(main_jet_path, 'r', encoding='utf-8') as f:
            base_data = json.load(f)
        tmi_shortie["content"].extend(base_data["content"])
        
        # Copy base game prompt data folders into the build
        source_dir = os.path.join(backup_path, base_folder_structure, fileName)
        copy_dir = os.path.join(target_path, fileName)
        shutil.copytree(source_dir, copy_dir, dirs_exist_ok=True)
    
    # Create tmi_shortie.jet file in the proper directory
    main_output_path = os.path.join(target_path, fileName + ".jet")
    with open(main_output_path, 'w', encoding='utf-8') as f:
        json.dump(tmi_shortie, f, ensure_ascii=False, indent=4)
    
    # Create folders for each prompt, with their data.jet file and audio file if applicable
    prompt_index = 0
    for episode in selected_episodes:
        for prompt in read_episode_prompts(episode.text()):
            # Create a folder for each prompt
            prompt_data = dataFileType(prompt)
            prompt_path = os.path.join(target_path, fileName, str(prompt_index))
            os.makedirs(prompt_path, exist_ok=True)
            
            # Add audio file if needed
            if prompt.has_audio():
                audio_path = os.path.join(base_path, episode.text(), prompt.audio)
                if os.path.exists(audio_path):
                    shutil.copy2(audio_path, os.path.join(prompt_path, os.path.basename("questionAudio.ogg")))
                else:
                    print(f"Warning: Audio file not found at {audio_path}")
            
            # Create data.jet file
            data_jet_path = os.path.join(prompt_path, "data.jet")
            with open(data_jet_path, 'w', encoding='utf-8') as f:
                json.dump(prompt_data.to_dict(), f, ensure_ascii=False, indent=4)
            prompt_index += 1
    return True

def generateFibbage3Files(selected_episodes, include_base_prompts=False, build_path=app_build_path):
    """Generates the necessary files for Fibbage 3 based on the provided prompts."""
    return generateFibbageFiles(selected_episodes, "games/Fibbage3/content/", fib3EAYTemplate, fib3EAYTemplate_Data, "tmiShortie", build_path, include_base_prompts)

def generateFibbage4Files(selected_episodes, include_base_prompts=False, lang="en", build_path=app_build_path):
    """Generates the necessary files for Fibbage 4 based on the provided prompts."""
    return generateFibbageFiles(selected_episodes, f"games/Fibbage4/content/{lang}/", fib4EAYTemplate, fib4EAYTemplate_Data, "eayblankie", build_path, include_base_prompts)