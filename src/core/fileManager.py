import os

current_file_dir = os.path.dirname(os.path.abspath(__file__))
root_project_dir = os.path.abspath(os.path.join(current_file_dir, "..", ".."))
base_path = os.path.join(root_project_dir, "episodes")

def create_base_folder():
    """
    Creates the base folder for episodes if it doesn't exist.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)

def create_episode_folder(episode_name):
    """
    Creates a new folder for the episode with the given name.
    """
    episode_path = os.path.join(base_path, episode_name)

    if not os.path.exists(episode_path):
        os.makedirs(episode_path)
        print(f"Episode folder '{episode_name}' created at {episode_path}.")
    else:
        print(f"Episode folder '{episode_name}' already exists.")
        
def list_episode_folders():
    folderList = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
    print(folderList)
    return folderList