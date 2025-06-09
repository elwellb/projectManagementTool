import os
import json
import tempfile
import re

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),"data", "project_data.json")
ROOT_DIR = os.path.join(tempfile.gettempdir(), "ProjectManager")

def ensure_dir(path):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
        return {"branches": {}}
    
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def sanitize_name(name):
    """Sanitize a project or asset name by removing invalid characters."""
    return re.sub(r"[\\/:*?\"<>|]", "_", name.strip())