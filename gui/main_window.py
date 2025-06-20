import os, re, datetime, shutil
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHeaderView, QInputDialog
from PyQt5.QtCore import QFile, Qt, QTimer

from core.project_generation import create_project_structure, create_asset_structure
from core.dcc_launcher import open_in_maya, open_in_photoshop, open_in_txt_editor
from gui.create_new_project import CreateProjectDialog
from gui.create_new_asset import CreateAssetDialog
from data.project_data import ProjectStore
from utils.file_utils import ROOT_DIR, is_valid_name

"""
Main application window for the Project Management Tool.
Handles project and asset management, UI setup, and user interactions.
"""

class MainWindow(QWidget):
    """
    Main window class for the Project Management Tool.
    Manages UI initialization, project and asset creation, and asset launching.
    """
    def __init__(self):
        """
        Initializes the main window, sets up UI, binds buttons, and starts the asset refresh timer.
        """
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.Window)
        self.store = ProjectStore()
        self.initUI()
        self.bindButtons()
        self.populate_project_combo()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.populate_asset_list)
        self.timer.start(5000)  # Refresh asset list every 5 seconds

    def initUI(self):
        """
        Loads the UI from the .ui file and sets the window title.
        """
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

        self.setWindowTitle("Project Management Tool")

    def bindButtons(self):
        """
        Connects UI buttons to their respective handler functions.
        """
        self.projectCreate.clicked.connect(self.create_project)
        self.projectCombo.currentIndexChanged.connect(self.populate_asset_list)
        self.assetCreate.clicked.connect(self.create_asset)
        self.openAssetButton.clicked.connect(self.open_asset)
        self.renameProj.clicked.connect(self.rename_project)
        self.deleteProj.clicked.connect(self.delete_project)
        self.renameAsset.clicked.connect(self.rename_asset)
        self.deleteAsset.clicked.connect(self.delete_asset)

    def create_project(self):
        """
        Handles the creation of a new project via a dialog.
        Validates input and updates the project list.
        """
        dialog = CreateProjectDialog(self)
        if dialog.exec_():
            raw_name = dialog.get_project_name()
            if not raw_name:
                QMessageBox.warning(self, "Invalid Project Name", "Project name cannot be empty.")
                return
            if not is_valid_name(raw_name):
                QMessageBox.warning(self, "Invalid Project Name", "Project names can only contain letters, numbers, underscores, and dashes.")
                return
            project_name = raw_name
            if project_name:
                self.store.add_project(project_name)
                create_project_structure(project_name)
                self.populate_project_combo()

    def populate_project_combo(self):
        """
        Populates the project combo box with available projects and updates asset controls.
        """
        self.projectCombo.clear()
        self.projectCombo.addItems(self.store.get_projects())
        if self.projectCombo.count() > 0:
            self.assetCreate.setEnabled(True)
            self.openAssetButton.setEnabled(True)
            self.renameProj.setEnabled(True)
            self.deleteProj.setEnabled(True)
            self.renameAsset.setEnabled(True)
            self.deleteAsset.setEnabled(True)
        else:
            self.assetCreate.setEnabled(False)
            self.openAssetButton.setEnabled(False)
            self.renameProj.setEnabled(False)
            self.deleteProj.setEnabled(False)
            self.renameAsset.setEnabled(False)
            self.deleteAsset.setEnabled(False)
        self.createTable()

    def create_asset(self):
        """
        Handles the creation of a new asset for the selected project.
        Validates input and updates the asset list.
        """
        project = self.projectCombo.currentText()
        assetDialog = CreateAssetDialog(self, project)
        if assetDialog.exec_():
            raw_name = assetDialog.get_asset_name()
            if not raw_name:
                QMessageBox.warning(self, "Invalid Asset Name", "Asset name cannot be empty.")
                return
            if not is_valid_name(raw_name):
                QMessageBox.warning(self, "Invalid Asset Name", "Asset names can only contain letters, numbers, underscores, and dashes.")
                return
            asset_name = raw_name
            if not asset_name:
                asset_name = None
            asset_type = assetDialog.get_asset_type()
            if not asset_type:
                asset_type = None

            reference = assetDialog.get_reference_target()
            if not reference:
                reference = None

            # Require reference for Rigs and Animations
            if "Rigs" in asset_type or "Animations" in asset_type:
                if not reference:
                    QMessageBox.warning(self, "Reference Required", "Rigs and Animations require a reference object.")
                    return
            if project and asset_name and asset_type:
                create_asset_structure(project, asset_type, asset_name, reference)
                self.store.add_asset(project, asset_name, asset_type)
                self.populate_asset_list()

    def populate_asset_list(self):
        """
        Populates the asset table with assets for the selected project.
        """
        self.assetTable.setRowCount(0)

        project = self.projectCombo.currentText()
        if not project:
            return

        assets = self.store.get_assets(project)

        for asset in assets:
            asset_name = asset.get("name")
            asset_type = asset.get("type", "Unknown")

            # Build asset directory path
            asset_dir = os.path.join(
                ROOT_DIR, "Projects", project, "ArtDepot",
                *asset_type.split("/"),
                asset_name
            )

            if not os.path.exists(asset_dir):
                continue

            # Determine file prefix based on asset type
            prefix = ""
            if "Models" in asset_type:
                prefix = "SM_"
            elif "Rigs" in asset_type:
                prefix = "RIG_"
            elif "Animations" in asset_type:
                prefix = "A_"
            elif "Textures" in asset_type:
                prefix = "T_"
            elif "VFX" in asset_type:
                prefix = "VFX_"

            # Look for asset files with the correct prefix and extension
            for fname in os.listdir(asset_dir):
                if (fname.endswith(".ma") or fname.endswith(".psd") or fname.endswith(".txt")) and fname.startswith(prefix):
                    full_path = os.path.join(asset_dir, fname)
                    self.add_asset_to_table(asset_name, asset_type, full_path)
                    break

    def add_asset_to_table(self, name, type_, path):
        """
        Adds an asset entry to the asset table.
        """
        # Split asset type into category and subtype
        category, subtype = type_.split("/") if "/" in type_ else (type_, "")
        row = self.assetTable.rowCount()
        self.assetTable.insertRow(row)
        self.assetTable.setItem(row, 0, QTableWidgetItem(str(name)))
        self.assetTable.setItem(row, 1, QTableWidgetItem(str(category)))
        self.assetTable.setItem(row, 2, QTableWidgetItem(str(subtype)))

        # Get last modified time or mark as missing
        if os.path.exists(path):
            last_modified = os.path.getmtime(path)
            modified_str = datetime.datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M')
        else:
            modified_str = "File Missing"

        last_item = QTableWidgetItem(modified_str)
        last_item.setData(Qt.UserRole, path)
        self.assetTable.setItem(row, 3, last_item)

    def createTable(self):
        """
        Sets up the asset table columns, headers, and selection behavior.
        """
        self.assetTable.setColumnCount(4)
        self.assetTable.setHorizontalHeaderLabels(["Asset Name", "Asset Category", "Asset Subtype", "Last Modified"])
        self.assetTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.assetTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.assetTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.assetTable.setSortingEnabled(True)

        self.assetTable.resizeColumnsToContents()
        self.assetTable.resizeRowsToContents()

        header = self.assetTable.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.populate_asset_list()

    def open_asset(self):
        """
        Opens the selected asset in the appropriate application based on file type.
        """
        selected_asset = self.assetTable.currentItem()
        if not selected_asset:
            QMessageBox.warning(self, "No Selection", "Please select an asset to open.")
            return

        row = selected_asset.row()
        path_item = self.assetTable.item(row, 3)
        asset_path = path_item.data(Qt.UserRole)

        if not os.path.exists(asset_path):
            QMessageBox.warning(self, "File Not Found", f"The asset file does not exist: {asset_path}")
            return

        # Launch the asset in the correct application
        if asset_path.endswith(".ma"):
            open_in_maya(asset_path)
        elif asset_path.endswith(".psd"):
            open_in_photoshop(asset_path)
        elif asset_path.endswith(".txt"):
            open_in_txt_editor(asset_path)

    def rename_project(self):
        old_name = self.projectCombo.currentText()
        new_name, ok = QInputDialog.getText(self, "Rename Project", "Enter new project name:")
        if ok and is_valid_name(new_name):
            os.rename(os.path.join(ROOT_DIR, "Projects", old_name), 
                      os.path.join(ROOT_DIR, "Projects", new_name))
            self.store.rename_project(old_name, new_name)
            self.populate_project_combo()

    def delete_project(self):
        name = self.projectCombo.currentText()
        confirm = QMessageBox.question(
            self,
            "Delete Project",
            f"Are you sure you want to delete the project '{name}'? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            shutil.rmtree(os.path.join(ROOT_DIR, "Projects", name), ignore_errors=True)
            self.store.delete_project(name)
            self.populate_project_combo()

    def rename_asset(self):
        row = self.assetTable.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an asset to rename.")
            return
        old_name = self.assetTable.item(row, 0).text()
        new_name, ok = QInputDialog.getText(self, "Rename Asset", "Enter new asset name:")
        if ok and is_valid_name(new_name):
            project = self.projectCombo.currentText()
            self.store.rename_asset(project, old_name, new_name)
            asset_type = self.assetTable.item(row, 1).text()
            asset_subtype = self.assetTable.item(row, 2).text()
            asset_path = os.path.join(ROOT_DIR, "Projects", project, "ArtDepot", asset_type, asset_subtype, old_name)
            new_asset_path = os.path.join(ROOT_DIR, "Projects", project, "ArtDepot", asset_type, asset_subtype, new_name)
            os.rename(asset_path, new_asset_path)
            self.populate_asset_list()

    def delete_asset(self):
        row = self.assetTable.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Selection", "Please select an asset to delete.")
            return
        asset_name = self.assetTable.item(row, 0).text()
        project = self.projectCombo.currentText()
        confirm = QMessageBox.question(
            self,
            "Delete Asset",
            f"Are you sure you want to delete the asset '{asset_name}'? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.store.delete_asset(project, asset_name)
            asset_type = self.assetTable.item(row, 1).text()
            asset_subtype = self.assetTable.item(row, 2).text()
            asset_path = os.path.join(ROOT_DIR, "Projects", project, "ArtDepot", asset_type, asset_subtype, asset_name)
            shutil.rmtree(asset_path, ignore_errors=True)
            self.populate_asset_list()