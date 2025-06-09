from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from utils.file_utils import ROOT_DIR
import os

class CreateAssetDialog(QDialog):
    def __init__(self, parent=None, projectName=None):
        super(CreateAssetDialog, self).__init__(parent)
        uiFilePath = os.path.join(os.path.dirname(__file__), "newAssetDialog.ui")
        uic.loadUi(uiFilePath, self)
        self.projectName = projectName
        self.fillAssetTypeCombo()
        self.bindAssetChoices()

    def bindAssetChoices(self):
        self.assetTypeCombo.currentIndexChanged.connect(self.updateAssetSubtypeOptions)
        self.charButton.toggled.connect(self.on_characters_selected)
        self.propButton.toggled.connect(self.on_props_selected)

    def get_asset_name(self):
        assetName = self.assetName.text()
        return assetName.strip() if assetName else None
    
    def get_asset_type(self):
        assetType = self.assetTypeCombo.currentText()

        if self.charButton.isChecked():
            subtype = "Characters"
        elif self.propButton.isChecked():
            subtype = "Props"
        elif self.enviroButton.isChecked():
            subtype = "Environments"
        else:
            subtype = ""
        #print(f"{assetType}/{subtype}")


        return f"{assetType}/{subtype}" if assetType else None
    
    def on_characters_selected(self, checked):
        if checked and self.assetTypeCombo.currentText() == "Rigs" or checked and self.assetTypeCombo.currentText() == "Animations":
            self.populateReferenceCombo("Characters")
        else:
            self.referenceCombo.clear()

    def on_props_selected(self, checked):
        if checked and self.assetTypeCombo.currentText() == "Rigs" or checked and self.assetTypeCombo.currentText() == "Animations":
            self.populateReferenceCombo("Props")
        else:
            self.referenceCombo.clear()

    def fillAssetTypeCombo(self):
        assetTypes = ["Models", "Textures", "Rigs", "Animations", "VFX"]
        self.assetTypeCombo.addItems(assetTypes)
        self.assetTypeCombo.setCurrentIndex(0)
        self.charButton.setChecked(True)  # Default to Characters for Models and Textures

    def updateAssetSubtypeOptions(self):

        assetType = self.assetTypeCombo.currentText()
        if assetType == "Models" or assetType == "Textures":
            self.charButton.setEnabled(True)
            self.propButton.setEnabled(True)
            self.enviroButton.setEnabled(True)
            self.referenceCombo.setEnabled(False)
        elif assetType == "Rigs" or assetType == "Animations":
            self.charButton.setEnabled(True)
            self.propButton.setEnabled(True)
            self.enviroButton.setEnabled(False)
            if self.enviroButton.isChecked():
                self.charButton.setChecked(True)  # Default to Characters if Environment is selected
            self.referenceCombo.setEnabled(True)
        else:
            self.charButton.setEnabled(False)
            self.propButton.setEnabled(False)
            self.enviroButton.setEnabled(False)
            self.charButton.setChecked(False)
            self.propButton.setChecked(False)
            self.enviroButton.setChecked(False)
            self.referenceCombo.setEnabled(False)
            
    def populateReferenceCombo(self, subtype):
        self.referenceCombo.clear()

        if not self.projectName or not subtype:
            return

        if self.assetTypeCombo.currentText() =="Rigs":
            ref_dir = os.path.join(
            ROOT_DIR, "Projects", self.projectName, "ArtDepot", "Models", subtype
            )
            
        elif self.assetTypeCombo.currentText() == "Animations":
            ref_dir = os.path.join(
            ROOT_DIR, "Projects", self.projectName, "ArtDepot", "Rigs", subtype
            )

        else:
            ref_dir = None

        if not os.path.exists(ref_dir):
            return

        for name in os.listdir(ref_dir):
            if name.lower() in {"tools", "config"}:
                continue
            asset_path = os.path.join(ref_dir, name)
            if os.path.isdir(asset_path):
                self.referenceCombo.addItem(name)

    def get_reference_target(self):
        return self.referenceCombo.currentText().strip()