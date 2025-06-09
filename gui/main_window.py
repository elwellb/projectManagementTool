import os
import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QHeaderView
from PyQt5.QtCore import QFile, Qt, QTimer


from core.project_generation import create_project_structure, create_asset_structure
from core.dcc_launcher import open_in_maya, open_in_photoshop, open_in_txt_editor
from gui.create_new_project import CreateProjectDialog
from gui.create_new_asset import CreateAssetDialog
from data.project_data import ProjectStore
from utils.file_utils import ROOT_DIR


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowFlags(Qt.Window)
        self.store = ProjectStore()
        self.initUI()
        self.bindButtons()
        self.populate_project_combo()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.populate_asset_list)
        self.timer.start(5000)  # Refresh asset list every second

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

    def bindButtons(self):
        self.projectCreate.clicked.connect(self.create_project)
        self.projectCombo.currentIndexChanged.connect(self.populate_asset_list)
        self.assetCreate.clicked.connect(self.create_asset)
        self.openAssetButton.clicked.connect(self.open_asset)

    def create_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec_():
            project_name = dialog.get_project_name()
            if project_name:
                self.store.add_project(project_name)
                create_project_structure(project_name)
                self.populate_project_combo()

    def populate_project_combo(self):
        self.projectCombo.clear()
        self.projectCombo.addItems(self.store.get_projects())
        self.createTable()

    def create_asset(self):
        project = self.projectCombo.currentText()
        assetDialog = CreateAssetDialog(self, project)
        if assetDialog.exec_():
            asset_name = assetDialog.get_asset_name()
            if not asset_name:
                asset_name = None
            asset_type = assetDialog.get_asset_type()
            if not asset_type:
                asset_type = None

            reference = assetDialog.get_reference_target()
            if not reference:
                reference = None
                
            if "Rigs" in asset_type or "Animations" in asset_type:
                if not reference:
                    QMessageBox.warning(self, "Reference Required", "Rigs and Animations require a reference object.")
                    return
            if project and asset_name and asset_type:
                create_asset_structure(project, asset_type, asset_name, reference)
                self.store.add_asset(project, asset_name, asset_type)
                self.populate_asset_list()

    def populate_asset_list(self):
        self.assetTable.setRowCount(0)

        project = self.projectCombo.currentText()
        if not project:
            return

        assets = self.store.get_assets(project)

        for asset in assets:
            asset_name = asset.get("name")

            asset_type = asset.get("type", "Unknown")

            asset_dir = os.path.join(
                ROOT_DIR, "Projects", project, "ArtDepot",
                *asset_type.split("/"),
                asset_name
            )

            if not os.path.exists(asset_dir):
                continue

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

            for fname in os.listdir(asset_dir):
                if (fname.endswith(".ma") or fname.endswith(".psd") or fname.endswith(".txt")) and fname.startswith(prefix):
                    full_path = os.path.join(asset_dir, fname)
                    self.add_asset_to_table(asset_name, asset_type, full_path)
                    break




    def add_asset_to_table(self, name, type_, path):
        print(f"Adding asset: {name}, Type: {type_}, Path: {path}")
        category, subtype = type_.split("/") if "/" in type_ else (type_, "")
        row = self.assetTable.rowCount()
        self.assetTable.insertRow(row)
        self.assetTable.setItem(row, 0, QTableWidgetItem(str(name)))
        self.assetTable.setItem(row, 1, QTableWidgetItem(str(category)))
        self.assetTable.setItem(row, 2, QTableWidgetItem(str(subtype)))

        if os.path.exists(path):
            last_modified = os.path.getmtime(path)
            modified_str = datetime.datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M')
        else:
            modified_str = "File Missing"

        last_item = QTableWidgetItem(modified_str)
        last_item.setData(Qt.UserRole, path)
        self.assetTable.setItem(row, 3, last_item)

    def createTable(self):
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
        
        if asset_path.endswith(".ma"):
            open_in_maya(asset_path)
        elif asset_path.endswith(".psd"):
            open_in_photoshop(asset_path)
        elif asset_path.endswith(".txt"):
            open_in_txt_editor(asset_path)

