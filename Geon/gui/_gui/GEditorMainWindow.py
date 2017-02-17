from PyQt4.Qt import QMainWindow, Qt

from GDialConnectDatabase import GDialConnectDatabase
from GDialImportDatabaseData import GDialImportDatabaseData
from GDocker import GDocker
from GEditorCentralTabW import GEditorCentralTabW
from GEditorLayerListW import GEditorLayerListW
from GEditorMenuBar import GEditorMenuBar
from GEditorStatusBar import GEditorStatusBar


# FIXME Fix the import trouble (ex  : try to import Geon.app from here...)

class GEditorMainWindow(QMainWindow):
    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.setWindowTitle("GEditor")

        self._controller = controller

        self._app = None

        self.showMaximized()
        self.setMenuBar(GEditorMenuBar(self))

        self.setCentralWidget(GEditorCentralTabW(self))
        self.setStatusBar(GEditorStatusBar(self))

        # Add a docker for layers management
        layerDock = GDocker(self)
        layerDock.setWindowTitle(self.tr("Layers"))
        self._layerList = GEditorLayerListW(layerDock, self._controller.layerSet())
        layerDock.setWidget(self._layerList)
        self.addDockWidget(Qt.LeftDockWidgetArea, layerDock)

        self.show()
        self.switchToApp()

    def controller(self):
        return self._controller

    def dialConnectDatabase(self):
        GDialConnectDatabase(self)

    def dialImportDatabaseData(self):
        GDialImportDatabaseData(self)

    def dialImportFileData(self):
        # TODO Add "Import from file" functionality
        pass

    def dialSelectLayerColor(self):
        # TODO Add "Select layer color" functionality
        pass

    def switchToApp(self):
        # TODO Add functionality to switch to app
        pass

    def refreshLayerList(self):
        self._layerList.refresh(self._controller.layerSet())
