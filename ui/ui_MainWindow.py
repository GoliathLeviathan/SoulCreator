# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/ui_MainWindow.ui'
#
# Created: Tue Jan 10 18:28:00 2012
#      by: pyside-uic 0.2.11 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1024, 479)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.horizontalLayout_5 = QtGui.QHBoxLayout(self.centralwidget)
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		self.selectWidget_select = SelectWidget(self.centralwidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.selectWidget_select.sizePolicy().hasHeightForWidth())
		self.selectWidget_select.setSizePolicy(sizePolicy)
		self.selectWidget_select.setObjectName("selectWidget_select")
		self.horizontalLayout_5.addWidget(self.selectWidget_select)
		self.verticalLayout_15 = QtGui.QVBoxLayout()
		self.verticalLayout_15.setObjectName("verticalLayout_15")
		self.widget_traits = BackgroundImageWidget(self.centralwidget)
		self.widget_traits.setObjectName("widget_traits")
		self.verticalLayout = QtGui.QVBoxLayout(self.widget_traits)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")
		self.stackedWidget_traits = QtGui.QStackedWidget(self.widget_traits)
		self.stackedWidget_traits.setFrameShape(QtGui.QFrame.NoFrame)
		self.stackedWidget_traits.setFrameShadow(QtGui.QFrame.Plain)
		self.stackedWidget_traits.setObjectName("stackedWidget_traits")
		self.stackedWidgetPage_info = QtGui.QWidget()
		self.stackedWidgetPage_info.setObjectName("stackedWidgetPage_info")
		self.verticalLayout_3 = QtGui.QVBoxLayout(self.stackedWidgetPage_info)
		self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.frame_info = QtGui.QFrame(self.stackedWidgetPage_info)
		self.frame_info.setObjectName("frame_info")
		self.layout_info = QtGui.QVBoxLayout(self.frame_info)
		self.layout_info.setContentsMargins(0, 0, 0, 0)
		self.layout_info.setObjectName("layout_info")
		self.horizontalLayout_4.addWidget(self.frame_info)
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_4.addItem(spacerItem)
		self.verticalLayout_3.addLayout(self.horizontalLayout_4)
		spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout_3.addItem(spacerItem1)
		self.stackedWidget_traits.addWidget(self.stackedWidgetPage_info)
		self.stackedWidgetPage_attributes = QtGui.QWidget()
		self.stackedWidgetPage_attributes.setObjectName("stackedWidgetPage_attributes")
		self.verticalLayout_6 = QtGui.QVBoxLayout(self.stackedWidgetPage_attributes)
		self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_6.setObjectName("verticalLayout_6")
		self.frame_attributes = QtGui.QFrame(self.stackedWidgetPage_attributes)
		self.frame_attributes.setObjectName("frame_attributes")
		self.layout_attributes = QtGui.QVBoxLayout(self.frame_attributes)
		self.layout_attributes.setContentsMargins(0, 0, 0, 0)
		self.layout_attributes.setObjectName("layout_attributes")
		self.verticalLayout_6.addWidget(self.frame_attributes)
		spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout_6.addItem(spacerItem2)
		self.stackedWidget_traits.addWidget(self.stackedWidgetPage_attributes)
		self.stackedWidgetPage_skills = QtGui.QWidget()
		self.stackedWidgetPage_skills.setObjectName("stackedWidgetPage_skills")
		self.verticalLayout_7 = QtGui.QVBoxLayout(self.stackedWidgetPage_skills)
		self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_7.setObjectName("verticalLayout_7")
		self.horizontalLayout_10 = QtGui.QHBoxLayout()
		self.horizontalLayout_10.setObjectName("horizontalLayout_10")
		self.verticalLayout_4 = QtGui.QVBoxLayout()
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.frame_skills = QtGui.QFrame(self.stackedWidgetPage_skills)
		self.frame_skills.setObjectName("frame_skills")
		self.layout_skills = QtGui.QVBoxLayout(self.frame_skills)
		self.layout_skills.setContentsMargins(0, 0, 0, 0)
		self.layout_skills.setObjectName("layout_skills")
		self.verticalLayout_4.addWidget(self.frame_skills)
		self.horizontalLayout_10.addLayout(self.verticalLayout_4)
		self.frame_skillSpecialties = QtGui.QFrame(self.stackedWidgetPage_skills)
		self.frame_skillSpecialties.setObjectName("frame_skillSpecialties")
		self.layout_specialties = QtGui.QVBoxLayout(self.frame_skillSpecialties)
		self.layout_specialties.setContentsMargins(0, 0, 0, 0)
		self.layout_specialties.setObjectName("layout_specialties")
		self.horizontalLayout_10.addWidget(self.frame_skillSpecialties)
		self.verticalLayout_7.addLayout(self.horizontalLayout_10)
		self.stackedWidget_traits.addWidget(self.stackedWidgetPage_skills)
		self.stackedWidgetPage_merits = QtGui.QWidget()
		self.stackedWidgetPage_merits.setObjectName("stackedWidgetPage_merits")
		self.horizontalLayout_3 = QtGui.QHBoxLayout(self.stackedWidgetPage_merits)
		self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.frame_merits = QtGui.QFrame(self.stackedWidgetPage_merits)
		self.frame_merits.setObjectName("frame_merits")
		self.layout_merits = QtGui.QVBoxLayout(self.frame_merits)
		self.layout_merits.setContentsMargins(0, 0, 0, 0)
		self.layout_merits.setObjectName("layout_merits")
		self.horizontalLayout_3.addWidget(self.frame_merits)
		spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem3)
		self.stackedWidget_traits.addWidget(self.stackedWidgetPage_merits)
		self.stackedWidgetPage_morality = QtGui.QWidget()
		self.stackedWidgetPage_morality.setObjectName("stackedWidgetPage_morality")
		self.verticalLayout_14 = QtGui.QVBoxLayout(self.stackedWidgetPage_morality)
		self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout_14.setObjectName("verticalLayout_14")
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.frame_morality = QtGui.QFrame(self.stackedWidgetPage_morality)
		self.frame_morality.setObjectName("frame_morality")
		self.layout_morality = QtGui.QVBoxLayout(self.frame_morality)
		self.layout_morality.setContentsMargins(0, 0, 0, 0)
		self.layout_morality.setObjectName("layout_morality")
		self.horizontalLayout.addWidget(self.frame_morality)
		spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem4)
		self.verticalLayout_14.addLayout(self.horizontalLayout)
		spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout_14.addItem(spacerItem5)
		self.stackedWidget_traits.addWidget(self.stackedWidgetPage_morality)
		self.stackedWidgetPage_powers = QtGui.QWidget()
		self.stackedWidgetPage_powers.setObjectName("stackedWidgetPage_powers")
		self.horizontalLayout_7 = QtGui.QHBoxLayout(self.stackedWidgetPage_powers)
		self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_7.setObjectName("horizontalLayout_7")
		self.frame_powers = QtGui.QFrame(self.stackedWidgetPage_powers)
		self.frame_powers.setObjectName("frame_powers")
		self.layout_powers = QtGui.QVBoxLayout(self.frame_powers)
		self.layout_powers.setContentsMargins(0, 0, 0, 0)
		self.layout_powers.setObjectName("layout_powers")
		self.horizontalLayout_7.addWidget(self.frame_powers)
		spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_7.addItem(spacerItem6)
		self.stackedWidget_traits.addWidget(self.stackedWidgetPage_powers)
		self.stackedWidgetPage_flaws = QtGui.QWidget()
		self.stackedWidgetPage_flaws.setObjectName("stackedWidgetPage_flaws")
		self.horizontalLayout_6 = QtGui.QHBoxLayout(self.stackedWidgetPage_flaws)
		self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_6.setObjectName("horizontalLayout_6")
		self.frame_flaws = QtGui.QFrame(self.stackedWidgetPage_flaws)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.frame_flaws.sizePolicy().hasHeightForWidth())
		self.frame_flaws.setSizePolicy(sizePolicy)
		self.frame_flaws.setObjectName("frame_flaws")
		self.layout_flaws = QtGui.QVBoxLayout(self.frame_flaws)
		self.layout_flaws.setContentsMargins(0, 0, 0, 0)
		self.layout_flaws.setObjectName("layout_flaws")
		self.horizontalLayout_6.addWidget(self.frame_flaws)
		spacerItem7 = QtGui.QSpacerItem(477, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_6.addItem(spacerItem7)
		self.stackedWidget_traits.addWidget(self.stackedWidgetPage_flaws)
		self.verticalLayout.addWidget(self.stackedWidget_traits)
		self.verticalLayout_15.addWidget(self.widget_traits)
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.label_pointsLeft = QtGui.QLabel(self.centralwidget)
		self.label_pointsLeft.setObjectName("label_pointsLeft")
		self.horizontalLayout_2.addWidget(self.label_pointsLeft)
		spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem8)
		self.pushButton_previous = QtGui.QPushButton(self.centralwidget)
		self.pushButton_previous.setObjectName("pushButton_previous")
		self.horizontalLayout_2.addWidget(self.pushButton_previous)
		self.pushButton_next = QtGui.QPushButton(self.centralwidget)
		self.pushButton_next.setObjectName("pushButton_next")
		self.horizontalLayout_2.addWidget(self.pushButton_next)
		self.verticalLayout_15.addLayout(self.horizontalLayout_2)
		self.horizontalLayout_5.addLayout(self.verticalLayout_15)
		MainWindow.setCentralWidget(self.centralwidget)
		self.mainToolBar = QtGui.QToolBar(MainWindow)
		self.mainToolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
		self.mainToolBar.setObjectName("mainToolBar")
		MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
		self.menubar = QtGui.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
		self.menubar.setObjectName("menubar")
		self.menuFile = QtGui.QMenu(self.menubar)
		self.menuFile.setObjectName("menuFile")
		self.menuAbout = QtGui.QMenu(self.menubar)
		self.menuAbout.setObjectName("menuAbout")
		self.menuConfiguration = QtGui.QMenu(self.menubar)
		self.menuConfiguration.setObjectName("menuConfiguration")
		MainWindow.setMenuBar(self.menubar)
		self.dockWidget_advantages = QtGui.QDockWidget(MainWindow)
		self.dockWidget_advantages.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
		self.dockWidget_advantages.setObjectName("dockWidget_advantages")
		self.dockWidget_advantagesContents = QtGui.QWidget()
		self.dockWidget_advantagesContents.setObjectName("dockWidget_advantagesContents")
		self.layout_advantages = QtGui.QVBoxLayout(self.dockWidget_advantagesContents)
		self.layout_advantages.setObjectName("layout_advantages")
		self.dockWidget_advantages.setWidget(self.dockWidget_advantagesContents)
		MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_advantages)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.actionSave = QtGui.QAction(MainWindow)
		self.actionSave.setObjectName("actionSave")
		self.actionOpen = QtGui.QAction(MainWindow)
		self.actionOpen.setObjectName("actionOpen")
		self.actionAbout = QtGui.QAction(MainWindow)
		self.actionAbout.setObjectName("actionAbout")
		self.actionPrint = QtGui.QAction(MainWindow)
		self.actionPrint.setObjectName("actionPrint")
		self.actionExport = QtGui.QAction(MainWindow)
		self.actionExport.setObjectName("actionExport")
		self.actionNew = QtGui.QAction(MainWindow)
		self.actionNew.setObjectName("actionNew")
		self.actionSettings = QtGui.QAction(MainWindow)
		self.actionSettings.setObjectName("actionSettings")
		self.actionQuit = QtGui.QAction(MainWindow)
		self.actionQuit.setObjectName("actionQuit")
		self.mainToolBar.addAction(self.actionNew)
		self.mainToolBar.addAction(self.actionOpen)
		self.mainToolBar.addAction(self.actionSave)
		self.mainToolBar.addSeparator()
		self.mainToolBar.addAction(self.actionExport)
		self.mainToolBar.addAction(self.actionPrint)
		self.menuFile.addAction(self.actionNew)
		self.menuFile.addAction(self.actionOpen)
		self.menuFile.addAction(self.actionSave)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionExport)
		self.menuFile.addAction(self.actionPrint)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionQuit)
		self.menuAbout.addAction(self.actionAbout)
		self.menuConfiguration.addAction(self.actionSettings)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuConfiguration.menuAction())
		self.menubar.addAction(self.menuAbout.menuAction())

		self.retranslateUi(MainWindow)
		self.stackedWidget_traits.setCurrentIndex(6)
		QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("activated()"), MainWindow.close)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
		self.label_pointsLeft.setText(QtGui.QApplication.translate("MainWindow", "0/0/0", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButton_previous.setText(QtGui.QApplication.translate("MainWindow", "Previous", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButton_next.setText(QtGui.QApplication.translate("MainWindow", "Next", None, QtGui.QApplication.UnicodeUTF8))
		self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
		self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
		self.menuConfiguration.setTitle(QtGui.QApplication.translate("MainWindow", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
		self.dockWidget_advantages.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Advantages", None, QtGui.QApplication.UnicodeUTF8))
		self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
		self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
		self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "&Open", None, QtGui.QApplication.UnicodeUTF8))
		self.actionOpen.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
		self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About...", None, QtGui.QApplication.UnicodeUTF8))
		self.actionPrint.setText(QtGui.QApplication.translate("MainWindow", "&Print", None, QtGui.QApplication.UnicodeUTF8))
		self.actionPrint.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
		self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "Export...", None, QtGui.QApplication.UnicodeUTF8))
		self.actionExport.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
		self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "New", None, QtGui.QApplication.UnicodeUTF8))
		self.actionNew.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
		self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "&Settings...", None, QtGui.QApplication.UnicodeUTF8))
		self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))

from src.Widgets.Components.BackgroundImageWidget import BackgroundImageWidget
from src.Widgets.SelectWidget import SelectWidget
