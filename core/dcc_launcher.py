import subprocess
import os
import sys

def open_in_maya(file_path):

    #maya_exe = find_maya_path()
    try:
        subprocess.Popen(file_path, shell=True)
    except:
        raise FileNotFoundError("Maya executable not found. Please ensure Maya is installed and configured correctly.")
    

def open_in_photoshop(file_path):
    try:
        subprocess.Popen(file_path, shell=True)
    except:
        raise FileNotFoundError(f"Photoshop executable not found. Please ensure Photoshop is installed and configured correctly.")
    
def open_in_txt_editor(file_path):
    try:
        subprocess.Popen(file_path, shell=True)
    except:
        raise FileNotFoundError(f"Text editor executable not found. Please ensure a text editor is installed and configured correctly.")