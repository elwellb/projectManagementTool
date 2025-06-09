from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import os

class CreateProjectDialog(QDialog):
    """
    Dialog window for creating a new project.
    Loads the UI from a .ui file and provides a method to get the entered project name.
    """
    def __init__(self, parent=None):
        """
        Initialize the dialog and load the UI file.
        """
        super(CreateProjectDialog, self).__init__(parent)
        # Construct the path to the .ui file located in the same directory as this script
        uiFilePath = os.path.join(os.path.dirname(__file__), "newProjDialog.ui")
        # Load the UI layout from the .ui file
        uic.loadUi(uiFilePath, self)

    def get_project_name(self):
        """
        Retrieve and clean the project name entered by the user.
        """
        # Get the text from the project name input field
        projName = self.projectName.text()
        # Return the stripped project name, or None if empty
        return projName.strip() if projName else None