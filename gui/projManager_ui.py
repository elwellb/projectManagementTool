# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'projManager.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1021, 1000)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(1000, 1000))
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 1002, 1062))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 1, 5, 1, 1)

        self.assetCreate = QPushButton(self.verticalLayoutWidget)
        self.assetCreate.setObjectName(u"assetCreate")
        self.assetCreate.setEnabled(False)

        self.gridLayout.addWidget(self.assetCreate, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.projectCreate = QPushButton(self.verticalLayoutWidget)
        self.projectCreate.setObjectName(u"projectCreate")

        self.gridLayout.addWidget(self.projectCreate, 1, 2, 1, 1)

        self.projectCombo = QComboBox(self.verticalLayoutWidget)
        self.projectCombo.setObjectName(u"projectCombo")

        self.gridLayout.addWidget(self.projectCombo, 1, 1, 1, 1)

        self.openAssetButton = QPushButton(self.verticalLayoutWidget)
        self.openAssetButton.setObjectName(u"openAssetButton")
        self.openAssetButton.setEnabled(False)

        self.gridLayout.addWidget(self.openAssetButton, 1, 6, 1, 1)

        self.renameProj = QPushButton(self.verticalLayoutWidget)
        self.renameProj.setObjectName(u"renameProj")
        self.renameProj.setEnabled(False)

        self.gridLayout.addWidget(self.renameProj, 1, 3, 1, 1)

        self.deleteProj = QPushButton(self.verticalLayoutWidget)
        self.deleteProj.setObjectName(u"deleteProj")
        self.deleteProj.setEnabled(False)

        self.gridLayout.addWidget(self.deleteProj, 1, 4, 1, 1)

        self.renameAsset = QPushButton(self.verticalLayoutWidget)
        self.renameAsset.setObjectName(u"renameAsset")
        self.renameAsset.setEnabled(False)

        self.gridLayout.addWidget(self.renameAsset, 2, 6, 1, 1)

        self.deleteAsset = QPushButton(self.verticalLayoutWidget)
        self.deleteAsset.setObjectName(u"deleteAsset")
        self.deleteAsset.setEnabled(False)

        self.gridLayout.addWidget(self.deleteAsset, 3, 6, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.assetTable = QTableWidget(self.verticalLayoutWidget)
        self.assetTable.setObjectName(u"assetTable")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.assetTable.sizePolicy().hasHeightForWidth())
        self.assetTable.setSizePolicy(sizePolicy1)
        self.assetTable.setAlternatingRowColors(True)
        self.assetTable.setColumnCount(0)

        self.verticalLayout.addWidget(self.assetTable)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Project:", None))
        self.assetCreate.setText(QCoreApplication.translate("Form", u"+ New Asset", None))
        self.projectCreate.setText(QCoreApplication.translate("Form", u"+ New Project", None))
        self.openAssetButton.setText(QCoreApplication.translate("Form", u"Open Asset", None))
        self.renameProj.setText(QCoreApplication.translate("Form", u"Rename Project", None))
        self.deleteProj.setText(QCoreApplication.translate("Form", u"Delete Project", None))
        self.renameAsset.setText(QCoreApplication.translate("Form", u"Rename Asset", None))
        self.deleteAsset.setText(QCoreApplication.translate("Form", u"Delete Asset", None))
    # retranslateUi

