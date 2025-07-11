from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QResizeEvent

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QToolBar, QTreeView, QVBoxLayout,
    QWidget, QFrame)

# Scalability: https://doc.qt.io/qt-6/scalability.html

class QProportionalResizeLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aspect_ratio = 1.0

    def setAspectRatio(self, w, h):
        if h != 0:
            self._aspect_ratio = w / h
        else:
            self._aspect_ratio = 1.0

    def resizeEvent(self, event: QResizeEvent):
        # Maintain label size proportional to the aspect ratio on resize
        new_width = event.size().width()
        new_height = event.size().height()
        if new_width / self._aspect_ratio <= new_height:
            w = new_width
            h = int(w / self._aspect_ratio)
        else:
            h = new_height
            w = int(h * self._aspect_ratio)
        self.resize(w, h)
        event.accept()
        # super().resizeEvent(event)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 800)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        #MainWindow.setMaximumSize(QSize(1200, 800))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)

        ### Toolbars and Actions ###
        self.actionOpen_Data_File = QAction(MainWindow)
        self.actionOpen_Data_File.setObjectName(u"actionOpen_Data_File")
        self.actionOpen_Data_File.setEnabled(True)
        icon = QIcon(QIcon.fromTheme(u"document-open"))
        self.actionOpen_Data_File.setIcon(icon)
        self.actionOpen_Data_File.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSave_Gradings = QAction(MainWindow)
        self.actionSave_Gradings.setObjectName(u"actionSave_Gradings")
        self.actionSave_Gradings.setEnabled(False)
        icon1 = QIcon(QIcon.fromTheme(u"document-save"))
        self.actionSave_Gradings.setIcon(icon1)
        self.actionSave_Gradings.setMenuRole(QAction.MenuRole.NoRole)

        ### Main Window Layout ###
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        ### Assignment Navigator Layout ###
        self.assignment_nav_layout = QVBoxLayout()
        self.assignment_nav_layout.setSpacing(0)
        self.assignment_nav_layout.setObjectName(u"assignment_nav_layout")
        self.assignment_nav_layout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.assignment_nav_layout.setContentsMargins(0, 0, 0, 0)
        self.assignment_nav_header_label = QLabel(self.centralwidget)
        self.assignment_nav_header_label.setObjectName(u"assignment_nav_header_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.assignment_nav_header_label.sizePolicy().hasHeightForWidth())
        self.assignment_nav_header_label.setSizePolicy(sizePolicy1)
        self.assignment_nav_header_label.setMaximumSize(QSize(16777215, 16777215))

        self.assignment_nav_layout.addWidget(self.assignment_nav_header_label, 0, Qt.AlignmentFlag.AlignLeft)

        ### Assignment Navigator Tree View Layout ###
        self.assignment_nav_tree_view = QTreeView(self.centralwidget)
        self.assignment_nav_tree_view.setObjectName(u"assignment_nav_tree_view")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(4)
        sizePolicy2.setHeightForWidth(self.assignment_nav_tree_view.sizePolicy().hasHeightForWidth())
        self.assignment_nav_tree_view.setSizePolicy(sizePolicy2)
        self.assignment_nav_tree_view.setMinimumSize(QSize(0, 0))
        self.assignment_nav_tree_view.setMaximumSize(QSize(16777215, 300))

        self.assignment_nav_layout.addWidget(self.assignment_nav_tree_view, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        ### Assignment Navigator Assignment Description & Img Layout ###
        self.assignment_nav_desc_layout = QVBoxLayout()
        self.assignment_nav_desc_layout.setObjectName(u"assignment_nav_desc_layout")
        self.assignment_nav_img_label = QLabel(self.centralwidget)
        self.assignment_nav_img_label.setObjectName(u"assignment_nav_img_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(4)
        sizePolicy3.setHeightForWidth(self.assignment_nav_img_label.sizePolicy().hasHeightForWidth())
        self.assignment_nav_img_label.setSizePolicy(sizePolicy3)
        self.assignment_nav_img_label.setMinimumSize(QSize(250, 250))
        self.assignment_nav_img_label.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2.5px;\n"
"border-color: white;")

        self.assignment_nav_desc_layout.addWidget(self.assignment_nav_img_label)

        self.assignment_nav_desc_label = QLabel(self.centralwidget)
        self.assignment_nav_desc_label.setObjectName(u"assignment_nav_desc_label")

        self.assignment_nav_desc_layout.addWidget(self.assignment_nav_desc_label)


        self.assignment_nav_layout.addLayout(self.assignment_nav_desc_layout)

        self.assignment_nav_layout.setStretch(0, 2)
        self.assignment_nav_layout.setStretch(1, 4)
        self.assignment_nav_layout.setStretch(2, 4)

        self.horizontalLayout_2.addLayout(self.assignment_nav_layout)

        ### Submission Navigator Layout ###
        self.submission_nav_layout = QVBoxLayout()
        self.submission_nav_layout.setObjectName(u"submission_nav_layout")
        self.submission_nav_viewer_layout = QHBoxLayout()
        self.submission_nav_viewer_layout.setObjectName(u"submission_nav_viewer_layout")

        ## Submission Navigator Viewer Layout ###
        viewport_viewer_frame = QFrame()
        viewport_viewer_frame.setLineWidth(1)
        viewport_viewer_frame.setFrameShape(QFrame.Shape.NoFrame)
        viewport_viewer_frame.setFrameShadow(QFrame.Shadow.Sunken)
        viewport_viewer_frame.setObjectName(u"viewport_viewer_frame")

        self.submission_nav_viewer_viewport_layout = QVBoxLayout(viewport_viewer_frame)
        self.submission_nav_viewer_viewport_layout.setObjectName(u"submission_nav_viewer_viewport_layout")
        self.submission_nav_viewer_viewport_img_layout = QHBoxLayout()
        self.submission_nav_viewer_viewport_img_layout.setObjectName(u"submission_nav_viewer_viewport_img_layout")

        self.submission_nav_viewport_img_solution_layout = QVBoxLayout()
        self.submission_nav_viewport_img_solution_layout.setObjectName(u"submission_nav_viewport_img_solution_layout")

        self.attempt_header_label = QLabel(self.centralwidget)
        self.attempt_header_label.setObjectName(u"attempt_header_label")

        self.submission_nav_viewport_img_solution_layout.addWidget(self.attempt_header_label)

        self.attempt_img_label = QLabel(self.centralwidget)
        self.attempt_img_label.setObjectName(u"attempt_img_label")



        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.attempt_img_label = QProportionalResizeLabel(self.centralwidget)
        self.attempt_img_label.setObjectName(u"attempt_img_label")
        self.attempt_img_label.setSizePolicy(sizePolicy4)
        self.attempt_img_label.setMinimumSize(QSize(150, 150))
        self.attempt_img_label.setMaximumSize(QSize(300, 300))
        self.attempt_img_label.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                 "border-style: solid;\n"
                 "border-width: 1px;\n"
                 "border-radius: 2.5px;\n"
                 "border-color: white;")
        self.attempt_img_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.submission_nav_viewport_img_solution_layout.addWidget(self.attempt_img_label)
        # self.submission_nav_viewport_img_solution_layout.setStretch(0, 1)
        # self.submission_nav_viewport_img_solution_layout.setStretch(1, 1)
        self.submission_nav_viewport_img_solution_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.submission_nav_viewer_viewport_img_layout.addLayout(self.submission_nav_viewport_img_solution_layout)

        self.submission_nav_viewport_img_attempt_layout = QVBoxLayout()
        self.submission_nav_viewport_img_attempt_layout.setObjectName(u"submission_nav_viewport_img_attempt_layout")
        self.solution_header_label = QLabel(self.centralwidget)
        self.solution_header_label.setObjectName(u"solution_header_label")

        self.submission_nav_viewport_img_attempt_layout.addWidget(self.solution_header_label)
        self.submission_nav_viewport_img_attempt_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)

        self.solution_img_label = QProportionalResizeLabel(self.centralwidget)
        self.solution_img_label.setObjectName(u"solution_img_label")
        # sizePolicy4.setHeightForWidth(self.solution_img_label.sizePolicy().hasHeightForWidth())
        self.solution_img_label.setSizePolicy(sizePolicy4)
        self.solution_img_label.setMinimumSize(QSize(150, 150))
        self.solution_img_label.setMaximumSize(QSize(300, 300))
        self.solution_img_label.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-radius: 2.5px;\n"
"border-color: white;")

        self.submission_nav_viewport_img_attempt_layout.addWidget(self.solution_img_label)


        self.submission_nav_viewer_viewport_img_layout.addLayout(self.submission_nav_viewport_img_attempt_layout)


        self.submission_nav_viewer_viewport_layout.addLayout(self.submission_nav_viewer_viewport_img_layout)

        self.viewport_button_frame = QFrame()
        self.viewport_button_frame.setLineWidth(1)
        self.viewport_button_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.viewport_button_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.viewport_button_frame.setObjectName(u"viewport_button_frame")

        self.submission_nav_viewer_viewport_buttons_layout = QHBoxLayout(self.viewport_button_frame)
        self.submission_nav_viewer_viewport_buttons_layout.setObjectName(u"submission_nav_viewer_viewport_buttons_layout")
        self.submission_nav_button_previous = QPushButton(self.centralwidget)
        self.submission_nav_button_previous.setObjectName(u"submission_nav_button_previous")
        self.submission_nav_button_previous.setMaximumSize(QSize(50, 16777215))
        icon2 = QIcon(QIcon.fromTheme(u"go-previous"))
        self.submission_nav_button_previous.setIcon(icon2)

        self.submission_nav_viewer_viewport_buttons_layout.addWidget(self.submission_nav_button_previous)

        self.submission_nav_button_next = QPushButton(self.centralwidget)
        self.submission_nav_button_next.setObjectName(u"submission_nav_button_next")
        self.submission_nav_button_next.setMaximumSize(QSize(50, 16777215))
        icon3 = QIcon(QIcon.fromTheme(u"go-next"))
        self.submission_nav_button_next.setIcon(icon3)

        self.submission_nav_viewer_viewport_buttons_layout.addWidget(self.submission_nav_button_next)


        #self.submission_nav_viewer_viewport_layout.addLayout(self.submission_nav_viewer_viewport_buttons_layout)
        self.submission_nav_viewer_viewport_layout.addWidget(self.viewport_button_frame)

        # self.submission_nav_viewer_viewport_layout.setStretch(1, 1)

        # self.submission_nav_viewer_layout.addLayout(self.submission_nav_viewer_viewport_layout)
        self.submission_nav_viewer_layout.addWidget(viewport_viewer_frame)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy5)
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.tabWidget.addTab(self.tab_6, "")

        self.submission_nav_viewer_layout.addWidget(self.tabWidget)

        self.submission_nav_viewer_layout.setStretch(0, 2)
        self.submission_nav_viewer_layout.setStretch(1, 1)

        self.submission_nav_layout.addLayout(self.submission_nav_viewer_layout)

        self.submission_nav_grading_layout = QHBoxLayout()
        self.submission_nav_grading_layout.setObjectName(u"submission_nav_grading_layout")
        self.submission_nav_grading_layout_col1 = QVBoxLayout()
        self.submission_nav_grading_layout_col1.setObjectName(u"submission_nav_grading_layout_col1")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.submission_nav_grading_layout_col1.addWidget(self.label_3)

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.submission_nav_grading_layout_col1.addWidget(self.comboBox)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox_3)

        self.checkBox_5 = QCheckBox(self.centralwidget)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox_5)

        self.checkBox_4 = QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox_4)

        self.checkBox_6 = QCheckBox(self.centralwidget)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox_6)

        self.checkBox_7 = QCheckBox(self.centralwidget)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox_7)

        self.checkBox_8 = QCheckBox(self.centralwidget)
        self.checkBox_8.setObjectName(u"checkBox_8")

        self.submission_nav_grading_layout_col1.addWidget(self.checkBox_8)


        self.submission_nav_grading_layout.addLayout(self.submission_nav_grading_layout_col1)

        self.submission_nav_grading_layout_col2 = QVBoxLayout()
        self.submission_nav_grading_layout_col2.setObjectName(u"submission_nav_grading_layout_col2")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.submission_nav_grading_layout_col2.addWidget(self.label_4)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.submission_nav_grading_layout_col2.addWidget(self.comboBox_2)

        self.submission_nav_grading_layout_col2.setStretch(0, 1)
        self.submission_nav_grading_layout_col2.setStretch(1, 1)

        self.submission_nav_grading_layout.addLayout(self.submission_nav_grading_layout_col2)

        self.submission_nav_grading_layout_col3 = QVBoxLayout()
        self.submission_nav_grading_layout_col3.setObjectName(u"submission_nav_grading_layout_col3")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.submission_nav_grading_layout_col3.addWidget(self.label_5)

        self.comboBox_3 = QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.submission_nav_grading_layout_col3.addWidget(self.comboBox_3)

        self.submission_nav_grading_layout_col3.setStretch(0, 1)
        self.submission_nav_grading_layout_col3.setStretch(1, 1)

        self.submission_nav_grading_layout.addLayout(self.submission_nav_grading_layout_col3)

        self.submission_nav_grading_layout.setStretch(0, 1)
        self.submission_nav_grading_layout.setStretch(1, 1)
        self.submission_nav_grading_layout.setStretch(2, 1)

        self.submission_nav_layout.addLayout(self.submission_nav_grading_layout)

        self.submission_nav_layout.setStretch(0, 1)
        self.submission_nav_layout.setStretch(1, 1)

        self.horizontalLayout_2.addLayout(self.submission_nav_layout)

        self.horizontalLayout_2.setStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionOpen_Data_File)
        self.toolBar.addAction(self.actionSave_Gradings)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_Data_File.setText(QCoreApplication.translate("MainWindow", u"Open Data File", None))
        self.actionSave_Gradings.setText(QCoreApplication.translate("MainWindow", u"Save Gradings", None))
        self.assignment_nav_header_label.setText(QCoreApplication.translate("MainWindow", u"Assignment Navigator", None))
        self.assignment_nav_img_label.setText(QCoreApplication.translate("MainWindow", u" Assignment Image", None))
        self.assignment_nav_desc_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.attempt_header_label.setText(QCoreApplication.translate("MainWindow", u"Solution", None))
        self.attempt_img_label.setText(QCoreApplication.translate("MainWindow", u" Assignment Image", None))
        self.solution_header_label.setText(QCoreApplication.translate("MainWindow", u"Attempt", None))
        self.solution_img_label.setText(QCoreApplication.translate("MainWindow", u" Assignment Image", None))
        self.submission_nav_button_previous.setText("")
        self.submission_nav_button_next.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox_5.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox_4.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox_6.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox_7.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.checkBox_8.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

