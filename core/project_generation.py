import os
import shutil
from utils.file_utils import ensure_dir, ROOT_DIR, sanitize_name

def create_project_structure(project="NewProject"):
    """ Create the directory structure for a new project under a branch. """
    # Global tools and config
    ensure_dir(os.path.join(ROOT_DIR, "Tools"))
    ensure_dir(os.path.join(ROOT_DIR, "Config"))

    project = sanitize_name(project)
    base = os.path.join(ROOT_DIR, "Projects", project)
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
    for folder in subfolders:
        ensure_dir(os.path.join(base, folder))
    return base


def create_asset_structure(project, asset_type, asset_name, reference=None):
    """ 
    Create the directory structure for a new asset under a level in GameDepot.
    Also creates subfolder for maya source file in ArtDepot.
    """
    project = sanitize_name(project)
    asset_name = sanitize_name(asset_name)
    asset_parts = asset_type.split('/')
    #print(asset_parts)

    category, subtype = asset_parts
    asset_root = os.path.join(ROOT_DIR, "Projects", project, "ArtDepot", category, subtype, asset_name)
    ensure_dir(asset_root)
    prefix_map = {
        "models": "SM",
        "rigs": "RIG",
        "animations": "A",
        "textures": "T",
        "vfx": "VFX"
    }
    prefix = prefix_map.get(category.lower(), category.upper())
    asset_name = f"{prefix}_{asset_name}"
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

    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "model_template.ma")
    to_path = os.path.join(art_depot_path, f"{asset_name}.ma")
    shutil.copyfile(from_path, to_path)

def create_rig_stub(art_depot_path, asset_name, subtype, reference):

    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "rig_template.ma")
    from_path = os.path.abspath(from_path)
    to_path = os.path.join(art_depot_path, f"{asset_name}.ma")
    shutil.copyfile(from_path, to_path)

    if reference:
        relative_ref_path = f"../../../Models/{subtype}/{reference}/SM_{reference}.ma"
        with open(to_path, 'a') as f:
            f.write(f'\nfile -r -type "mayaAscii" -namespace "{reference}" "{relative_ref_path}";\n')

def create_animation_stub(art_depot_path, asset_name, subtype, reference):
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "anim_template.ma")
    from_path = os.path.abspath(from_path)
    to_path = os.path.join(art_depot_path, f"{asset_name}.ma")
    shutil.copyfile(from_path, to_path)

    if reference:
        relative_ref_path = f"../../../Rigs/{subtype}/{reference}/RIG_{reference}.ma"
        with open(to_path, 'a') as f:
            f.write(f'\nfile -r -type "mayaAscii" -namespace "{reference}" "{relative_ref_path}";\n')

def create_texture_stub(art_depot_path, asset_name):
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "tex_template.psd")
    from_path = os.path.abspath(from_path)
    to_path = os.path.join(art_depot_path, f"{asset_name}.psd")
    shutil.copyfile(from_path, to_path)

def create_vfx_stub(art_depot_path, asset_name):
    from_path = os.path.join(os.path.dirname(__file__), "..", "file_templates", "vfx_template.txt")
    from_path = os.path.abspath(from_path)
    to_path = os.path.join(art_depot_path, f"{asset_name}.txt")
    shutil.copyfile(from_path, to_path)