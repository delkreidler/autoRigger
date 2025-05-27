import os
import sys
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtCore import QFile, QIODevice

from autoRigger import constant
from autoRigger.core.joint import Joint
from autoRigger.core.chain import Chain
from autoRigger.core.fkChain import FKChain

def get_maya_mainwindow():
    """Returns the Maya main window as a QWidget."""
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QWidget)

# Subclass QMainWindow to customize your application's main window
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        self.setup_UI()  
        self.connect_signals()
        self.update_combo_box()
        self.item = Joint()

    def setup_UI(self):
        self.setWindowFlags(Qt.Window)
        uiFile = QFile(os.path.join(constant.UI_FOLDER, constant.UI_FILE))
        if not uiFile.open(QIODevice.ReadOnly):
            print(f"Cannot open {constant.UI_FILE}: {constant.UI_FILE.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        self.ui = loader.load(uiFile, self)
        uiFile.close()
        self.ui.setParent(self)
    
    def update_combo_box(self):
        self.ui.cBox_item.addItem("Joint", Joint())
        self.ui.cBox_item.addItem("Chain", Chain())
        self.ui.cBox_item.addItem("FK Chain", FKChain())

    def connect_signals(self):
        self.ui.Btn_ConstructGuides.clicked.connect(self.btn_construct_guides)
        self.ui.Btn_ConstructRig.clicked.connect(self.btn_construct_rig)

    def btn_construct_guides(self):
        self.item = self.ui.cBox_item.currentData()
        self.item.construct_guides()

    def btn_construct_rig(self):
        self.item.construct_rig()

def open_window():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QApplication.allWindows()):
            if 'myToolWindowName' in win.objectName(): # update this name to match name below
                win.destroy()
  
    mayaMainWindow = get_maya_mainwindow()
    MainWindow.window = MainWindow(parent = mayaMainWindow)
    MainWindow.window.setObjectName('myToolWindowName') # code above uses this to ID any existing windows
    MainWindow.window.setWindowTitle('AutoRigger Tool')
    MainWindow.window.show()
            