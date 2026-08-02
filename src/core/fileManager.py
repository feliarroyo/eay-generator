import json
import os
import shutil
from tkinter import Pack

from core.models import VALID_LANGUAGES, EAYCustomEpisode, Prompt, fib3Template, fib3Template_Data, fib4Template, fib4Template_Data

current_file_dir = os.path.dirname(os.path.abspath(__file__))
root_project_dir = os.path.abspath(os.path.join(current_file_dir, "..", ".."))
base_path = os.path.join(root_project_dir, "episodes")
backup_path = os.path.join(root_project_dir, "backup")
build_path = os.path.join(root_project_dir, "build")

def create_base_folder():
    """Creates the base folder for episodes if it doesn't exist."""
    if not os.path.exists(base_path):
        os.makedirs(base_path)

def create_episode_folder(episode_name, content=None, audios=None):
    """Creates a new folder for the episode with the given name and base file."""
    episode_path = os.path.join(base_path, episode_name)

    if not os.path.exists(episode_path):
        os.makedirs(episode_path)
        print(f"Episode folder '{episode_name}' created at {episode_path}.")
    else:
        print(f"Episode folder '{episode_name}' already exists.")
    
    if content is None:
        content = EAYCustomEpisode(episode_name, [])
    print(content)
    print(content.to_dict())
    json.dump(content.to_dict(), open(os.path.join(episode_path, "episode.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    
    #if audios is not None:
     #   for audio in audios:
      #      audio_path = os.path.join(episode_path, audio['filename'])
       #     with open(audio_path, 'wb') as f:
        #        f.write(audio['data'])
        
def list_episode_folders():
    folderList = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    print(folderList)
    return folderList

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
    prompts = [Prompt(p["personal_question"], p["screen_question"], p["audio"], p["suggestions"], p["x"], p["us"]) for p in prompts_data]
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

def generateFibbageFiles(prompts, shortieFileType, dataFileType, fileName):
    if not os.path.exists(build_path):
            os.makedirs(build_path)
    tmiShortie = shortieFileType(prompts)
    json.dump(tmiShortie.to_dict(), open(os.path.join(build_path, fileName + ".jet"), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
    for prompt in prompts:
        # Fibbage 3 tmiShortie/<id>/data.jet:
        prompt_data = dataFileType(prompt)
        prompt_path = os.path.join(build_path, fileName, str(prompts.index(prompt)))
        os.makedirs(prompt_path)
        json.dump(prompt_data.to_dict(), open(os.path.join(prompt_path, "data.jet"), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

def generateFibbage3Files(prompts):
    """Generates the necessary files for Fibbage 3 based on the provided prompts."""
    generateFibbageFiles(prompts, fib3Template, fib3Template_Data, "tmiShortie")
    
def generateFibbage4Files(prompts):
    """Generates the necessary files for Fibbage 4 based on the provided prompts."""
    generateFibbageFiles(prompts, fib4Template, fib4Template_Data, "eayblankie")