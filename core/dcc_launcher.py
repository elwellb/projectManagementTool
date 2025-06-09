import subprocess

def open_in_maya(file_path):
    """
    Opens the specified file in Autodesk Maya.
    """
    try:
        subprocess.Popen(file_path, shell=True)
    except:
        raise FileNotFoundError("Maya executable not found. Please ensure Maya is installed and configured correctly.")

def open_in_photoshop(file_path):
    """
    Opens the specified file in Adobe Photoshop.
    """
    try:
        subprocess.Popen(file_path, shell=True)
    except:
        raise FileNotFoundError("Photoshop executable not found. Please ensure Photoshop is installed and configured correctly.")

def open_in_txt_editor(file_path):
    """
    Opens the specified file in a text editor.
    """
    try:
        subprocess.Popen(file_path, shell=True)
    except:
        raise FileNotFoundError("Text editor executable not found. Please ensure a text editor is installed and configured correctly.")
