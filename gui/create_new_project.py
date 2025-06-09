from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import os

class CreateProjectDialog(QDialog):
    def __init__(self, parent=None):
        super(CreateProjectDialog, self).__init__(parent)
        uiFilePath = os.path.join(os.path.dirname(__file__), "newProjDialog.ui")
        uic.loadUi(uiFilePath, self)

    def get_project_name(self):

        projName = self.projectName.text()
        return projName.strip() if projName else None