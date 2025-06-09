import os, json
import shutil
from utils.file_utils import ensure_dir, ROOT_DIR

def create_project_structure(project="NewProject"):
    """
    Create the directory structure for a new project under a branch.

    This sets up global Tools and Config folders, then creates a set of
    predefined subfolders under the specified project directory inside the Projects folder.
    """
    # Create global Tools and Config directories
    ensure_dir(os.path.join(ROOT_DIR, "Tools"))
    ensure_dir(os.path.join(ROOT_DIR, "Config"))

    base = os.path.join(ROOT_DIR, "Projects", project)
    # List of subfolders to create within the project
    subfolders = [
        "Tools",
        "Config",
        "ArtDepot/Models/Characters/Tools",
        "ArtDepot/Models/Characters/Config",
        "ArtDepot/Models/Props/Tools",
        "ArtDepot/Models/Props/Config",
        "ArtDepot/Models/Environments/Tools",
        "ArtDepot/Models/Environments/Config",
        "ArtDepot/Rigs/Characters/Tools",
        "ArtDepot/Rigs/Characters/Config",
        "ArtDepot/Rigs/Props/Tools",
        "ArtDepot/Rigs/Props/Config",
        "ArtDepot/Animations/Characters/Tools",
        "ArtDepot/Animations/Characters/Config",
        "ArtDepot/Animations/Props/Tools",
        "ArtDepot/Animations/Props/Config",
        "ArtDepot/Textures/Characters/Tools",
        "ArtDepot/Textures/Characters/Config",
        "ArtDepot/Textures/Environments/Tools",
        "ArtDepot/Textures/Environments/Config",
        "ArtDepot/Textures/Props/Tools",
        "ArtDepot/Textures/Props/Config",
        "ArtDepot/VFX/Tools",
        "ArtDepot/VFX/Config",
        "IntermediateDepot/Characters",
        "IntermediateDepot/Props",
        "IntermediateDepot/Environments",
        "IntermediateDepot/Animations",
        "IntermediateDepot/VFX",
        "IntermediateDepot/Rigs",
    ]
    # Create each subfolder
    for folder in subfolders:
        ensure_dir(os.path.join(base, folder))
    inject_config_stub(base)
    return base

def create_asset_structure(project, asset_type, asset_name, reference=None):
    """
    Create the directory structure for a new asset under a level in GameDepot.
    Also creates a subfolder for the Maya source file in ArtDepot.
    """
    asset_parts = asset_type.split('/')
    # asset_parts should be [category, subtype]
    category, subtype = asset_parts
    asset_root = os.path.join(ROOT_DIR, "Projects", project, "ArtDepot", category, subtype, asset_name)
    inject_config_stub(asset_root)
    ensure_dir(asset_root)

    # Prefix mapping for asset file names
    prefix_map = {
        "models": "SM",
        "rigs": "RIG",
        "animations": "A",
        "textures": "T",
        "vfx": "VFX"
    }
    prefix = prefix_map.get(category.lower(), category.upper())
    asset_name = f"{prefix}_{asset_name}"

    # Create the appropriate stub file based on asset category
    if category == "Models":
        create_model_stub(asset_root, asset_name)
    elif category == "Rigs":
        create_rig_stub(asset_root, asset_name, subtype, reference)
    elif category == "Animations":
        create_animation_stub(asset_root, asset_name, subtype, reference)
    elif category == "Textures":
        create_texture_stub(asset_root, asset_name)
    elif category == "VFX":
        create_vfx_stub(asset_root, asset_name)

    return asset_root

def create_model_stub(art_depot_path, asset_name):
    """
    Create a Maya ASCII model file from a template in the specified directory.
    """
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "model_template.ma")
    to_path = os.path.join(art_depot_path, f"{asset_name}.ma")
    shutil.copyfile(from_path, to_path)

def create_rig_stub(art_depot_path, asset_name, subtype, reference):
    """
    Create a Maya ASCII rig file from a template and optionally reference a model.
    """
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "rig_template.ma")
    from_path = os.path.abspath(from_path)
    to_path = os.path.join(art_depot_path, f"{asset_name}.ma")
    shutil.copyfile(from_path, to_path)

    # If a reference is provided, append a Maya file reference command
    if reference:
        relative_ref_path = f"../../../Models/{subtype}/{reference}/SM_{reference}.ma"
        with open(to_path, 'a') as f:
            f.write(f'\nfile -r -type "mayaAscii" -namespace "{reference}" "{relative_ref_path}";\n')

def create_animation_stub(art_depot_path, asset_name, subtype, reference):
    """
    Create a Maya ASCII animation file from a template and optionally reference a rig.
    """
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "anim_template.ma")
    from_path = os.path.abspath(from_path)
    to_path = os.path.join(art_depot_path, f"{asset_name}.ma")
    shutil.copyfile(from_path, to_path)

    # If a reference is provided, append a Maya file reference command
    if reference:
        relative_ref_path = f"../../../Rigs/{subtype}/{reference}/RIG_{reference}.ma"
        with open(to_path, 'a') as f:
            f.write(f'\nfile -r -type "mayaAscii" -namespace "{reference}" "{relative_ref_path}";\n')

def create_texture_stub(art_depot_path, asset_name):
    """
    Create a Photoshop texture file from a template in the specified directory.
    """
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "tex_template.psd")
    to_path = os.path.join(art_depot_path, f"{asset_name}.psd")
    shutil.copyfile(from_path, to_path)

def create_vfx_stub(art_depot_path, asset_name):
    """
    Create a VFX stub file in the specified directory.
    """
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "vfx_template.txt")
    to_path = os.path.join(art_depot_path, f"{asset_name}.txt")
    shutil.copyfile(from_path, to_path)

DEFAULT_CONFIG = {
    "dccs": {
        "Maya": {
            "version": "2024",
            "path": "C:/Program Files/Autodesk/Maya2024/bin/maya.exe"
        },
        "Photoshop": {
            "version": "2023",
            "path": "C:/Program Files/Adobe/Adobe Photoshop 2023/Photoshop.exe"
        }
    },
    "engines": {
        "UnrealEngine": {
            "version": "5.3",
            "path": "C:/Program Files/Epic Games/UE_5.3/Engine/Binaries/Win64/UE5Editor.exe"
        }
    },
    "tools": {
        "CustomExporter": {
            "version": "1.2.0"
        },
        "Validator": {
            "version": "2.0.1"
        }
    }
}

def inject_config_stub(base_path):
    config_path = os.path.join(base_path, "Config")
    os.makedirs(config_path, exist_ok=True)

    config_file = os.path.join(config_path, "config.json")
    if not os.path.exists(config_file):
        with open(config_file, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        #print(f"Default config written to {config_file}")
    else:
        #print(f"Config already exists at {config_file}")
        return
