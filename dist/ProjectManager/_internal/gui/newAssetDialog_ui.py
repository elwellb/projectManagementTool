# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newAssetDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QButtonGroup, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QLabel,
    QLayout, QLineEdit, QRadioButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(750, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(750, 250))
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(160, 160, 231, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 377, 147))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.assetTypeCombo = QComboBox(self.gridLayoutWidget)
        self.assetTypeCombo.setObjectName(u"assetTypeCombo")

        self.gridLayout.addWidget(self.assetTypeCombo, 1, 1, 1, 1)

        self.propButton = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup = QButtonGroup(Dialog)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.propButton)
        self.propButton.setObjectName(u"propButton")

        self.gridLayout.addWidget(self.propButton, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.enviroButton = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.enviroButton)
        self.enviroButton.setObjectName(u"enviroButton")

        self.gridLayout.addWidget(self.enviroButton, 2, 1, 1, 1)

        self.charButton = QRadioButton(self.gridLayoutWidget)
        self.buttonGroup.addButton(self.charButton)
        self.charButton.setObjectName(u"charButton")

        self.gridLayout.addWidget(self.charButton, 2, 0, 1, 1)

        self.assetName = QLineEdit(self.gridLayoutWidget)
        self.assetName.setObjectName(u"assetName")

        self.gridLayout.addWidget(self.assetName, 0, 1, 1, 1)

        self.referenceCombo = QComboBox(self.gridLayoutWidget)
        self.referenceCombo.setObjectName(u"referenceCombo")

        self.gridLayout.addWidget(self.referenceCombo, 2, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(138, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 3, 1, 1)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Asset Type:", None))
        self.label_3.setText("")
        self.propButton.setText(QCoreApplication.translate("Dialog", u"Prop", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Asset Name:", None))
        self.enviroButton.setText(QCoreApplication.translate("Dialog", u"Environment", None))
        self.charButton.setText(QCoreApplication.translate("Dialog", u"Character", None))
    # retranslateUi

