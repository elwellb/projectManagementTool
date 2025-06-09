from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from utils.file_utils import ROOT_DIR
import os

class CreateAssetDialog(QDialog):
    """
    Dialog for creating a new asset in the project management tool.
    Handles UI setup, asset type/subtype selection, and reference population.
    """
    def __init__(self, parent=None, projectName=None):
        """
        Initialize the dialog, load UI, and set up controls.
        """
        super(CreateAssetDialog, self).__init__(parent)
        uiFilePath = os.path.join(os.path.dirname(__file__), "newAssetDialog.ui")
        uic.loadUi(uiFilePath, self)
        self.projectName = str(projectName)
        self.fillAssetTypeCombo()
        self.bindAssetChoices()

    def bindAssetChoices(self):
        """
        Connect UI signals to their respective slots for asset type/subtype changes.
        """
        self.assetTypeCombo.currentIndexChanged.connect(self.updateAssetSubtypeOptions)
        self.assetTypeCombo.currentIndexChanged.connect(lambda: self.populateReferenceCombo())
        self.charButton.toggled.connect(self.on_characters_selected)
        self.propButton.toggled.connect(self.on_props_selected)

    def get_asset_name(self):
        """
        Retrieve the asset name from the input field, stripping whitespace.
        """
        assetName = self.assetName.text()
        return assetName.strip() if assetName else None
    
    def get_asset_type(self):
        """
        Get the selected asset type and subtype as a formatted string.
        """
        assetType = self.assetTypeCombo.currentText()

        if self.charButton.isChecked():
            subtype = "Characters"
        elif self.propButton.isChecked():
            subtype = "Props"
        elif self.enviroButton.isChecked():
            subtype = "Environments"
        else:
            subtype = ""
        # Combine asset type and subtype for further processing
        return f"{assetType}/{subtype}" if assetType else None
    
    def on_characters_selected(self, checked):
        """
        Handle toggling of the Characters button.
        Populate reference combo if appropriate.
        """
        checked = self.charButton.isChecked()
        if (checked and self.assetTypeCombo.currentText() == "Rigs") or (checked and self.assetTypeCombo.currentText() == "Animations"):
            self.populateReferenceCombo("Characters")
        else:
            self.referenceCombo.clear()

    def on_props_selected(self, checked):
        """
        Handle toggling of the Props button.
        Populate reference combo if appropriate.
        """
        checked = self.propButton.isChecked()
        if (checked and self.assetTypeCombo.currentText() == "Rigs") or (checked and self.assetTypeCombo.currentText() == "Animations"):
            self.populateReferenceCombo("Props")
        else:
            self.referenceCombo.clear()

    def fillAssetTypeCombo(self):
        """
        Populate the asset type combo box with available types.
        Set default selection and subtype.
        """
        assetTypes = ["Models", "Textures", "Rigs", "Animations", "VFX"]
        self.assetTypeCombo.addItems(assetTypes)
        self.assetTypeCombo.setCurrentIndex(0)
        self.charButton.setChecked(True)  # Default to Characters for Models and Textures

    def updateAssetSubtypeOptions(self):
        """
        Enable or disable subtype buttons and reference combo based on asset type.
        """
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
                self.on_characters_selected(True)
            self.referenceCombo.setEnabled(True)
        else:
            self.charButton.setEnabled(False)
            self.propButton.setEnabled(False)
            self.enviroButton.setEnabled(False)
            self.charButton.setChecked(False)
            self.propButton.setChecked(False)
            self.enviroButton.setChecked(False)
            self.referenceCombo.setEnabled(False)
            
    def populateReferenceCombo(self, subtype=None):
        """
        Populate the reference combo box with available assets for the selected type/subtype.
        """
        self.referenceCombo.clear()

        if not self.projectName:
            return
        
        if isinstance(subtype, int):
            subtype = None
        # Determine subtype if not provided
        if subtype is None:
            if self.charButton.isChecked():
                subtype = "Characters"
            elif self.propButton.isChecked():
                subtype = "Props"
            else:
                return
            
        #print(self.projectName)
        #print(subtype)

        # Set reference directory based on asset type and subtype
        if self.assetTypeCombo.currentText() =="Rigs":
            ref_dir = os.path.join(
            ROOT_DIR, "Projects", self.projectName, "ArtDepot", "Models", subtype
            )
            
        elif self.assetTypeCombo.currentText() == "Animations":
            ref_dir = os.path.join(
            ROOT_DIR, "Projects", self.projectName, "ArtDepot", "Rigs", subtype
            )

        else:
            return

        if not os.path.exists(ref_dir):
            return

        # Add directories as reference options, skipping tools/config
        for name in os.listdir(ref_dir):
            if name.lower() in {"tools", "config"}:
                continue
            asset_path = os.path.join(ref_dir, name)
            if os.path.isdir(asset_path):
                self.referenceCombo.addItem(name)

    def get_reference_target(self):
        """
        Get the currently selected reference target from the combo box.
        """
        return self.referenceCombo.currentText().strip()