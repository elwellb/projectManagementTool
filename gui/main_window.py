import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QFile, Qt

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.Window)
        self.initUI()

    def initUI(self):
        uiFilePath = os.path.join(os.path.dirname(__file__), "projManager.ui")
        uiFile = QFile(uiFilePath)

        if not uiFile.exists():
            raise FileNotFoundError(f"UI File not found: {uiFilePath}")

        if not uiFile.open(QFile.ReadOnly):
            raise IOError(f"Unable to open UI file: {uiFilePath}")
        
        try:
            uic.loadUi(uiFile, self)
        finally:
            uiFile.close()