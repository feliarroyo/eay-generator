import json
import os

from core.models import EAYCustomEpisode, Prompt

current_file_dir = os.path.dirname(os.path.abspath(__file__))
root_project_dir = os.path.abspath(os.path.join(current_file_dir, "..", ".."))
base_path = os.path.join(root_project_dir, "episodes")

def create_base_folder():
    """
    Creates the base folder for episodes if it doesn't exist.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)

def create_episode_folder(episode_name, content=None, audios=None):
    """
    Creates a new folder for the episode with the given name and base file.
    """
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