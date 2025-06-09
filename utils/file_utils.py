import os
import json
import tempfile
import re

# Path to the main data file for storing project information
DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "project_data.json")
# Root directory for temporary project files
ROOT_DIR = os.path.join(tempfile.gettempdir(), "ProjectManager")
# Regex pattern for validating names (alphanumeric, underscores, hyphens)
VALID_NAME_REGEX = re.compile(r"^[\w\-]+$")

def ensure_dir(path):
    """Ensure that a directory exists, creating it if necessary."""
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def load_data():
    """Load project data from the JSON file if it exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
        # Fallback in case file doesn't exist (shouldn't reach here)
        return {"branches": {}}
    
def save_data(data):
    """Save the provided data dictionary to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def is_valid_name(name):
    """Check if a name matches the allowed pattern."""
    return bool(VALID_NAME_REGEX.fullmatch(name))