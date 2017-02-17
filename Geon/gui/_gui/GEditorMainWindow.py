from PyQt4.Qt import QMainWindow, Qt

from GDialColorSelection import GDialColorSelection
from GDialConnectDatabase import GDialConnectDatabase
from GDialImportDatabaseData import GDialImportDatabaseData
from GDialImportRasterFileData import GDialImportRasterFileData
from GDialImportVectorFileData import GDialImportVectorFileData
from GDocker import GDocker
from GEditorCentralTabW import GEditorCentralTabW
from GEditorLayerListW import GEditorLayerListW
from GEditorMenuBar import GEditorMenuBar
from GEditorStatusBar import GEditorStatusBar
from Geon.utils import GPrint


# FIXME Fix the import trouble (ex  : try to import Geon.app from here...)
class GEditorMainWindow(QMainWindow):
    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.setWindowTitle("GEditor")
        self.showMaximized()

        self._app = None

        self._tabW = GEditorCentralTabW(self)
        self.setCentralWidget(self._tabW)
        self.setStatusBar(GEditorStatusBar(self))
        self.setMenuBar(GEditorMenuBar(self))

        self._controller = controller
        self._controller.setMapCanvas(self._tabW.layerTab().mapCanvas())

        # Add a docker for layers management
        layerDock = GDocker(self)
        layerDock.setWindowTitle(self.tr("Layers"))

        self._layerList = GEditorLayerListW(layerDock, self._controller.layerSet())
        layerDock.setWidget(self._layerList)
        self.addDockWidget(Qt.LeftDockWidgetArea, layerDock)

        self.show()

    def controller(self):
        return self._controller

    def dialConnectDatabase(self):
        GDialConnectDatabase(self)

    def dialImportDatabaseData(self):
        if self._controller.databaseConnected():
            GDialImportDatabaseData(self)
        else:
            GPrint("Could not load tables : not connected to a database", "!!")

    # noinspection PyUnresolvedReferences
    def dialImportVectorFileData(self):
        dial = GDialImportVectorFileData(self)
        dial.fileSelected.connect(self._controller.createVectorLayerFromFile)
        dial.fileSelected.connect(self.refreshLayerList)
        dial.show()

    def dialImportRasterFileData(self):
        dial = GDialImportRasterFileData(self)
        dial.fileSelected.connect(self._controller.createRasterLayerFromFile)
        dial.fileSelected.connect(self.refreshLayerList)
        dial.show()

    def dialSelectLayerColor(self):
        if self._controller.layerSet():
            dial = GDialColorSelection(self)
            dial.currentColorChanged.connect(self._controller.showNewCurrentLayerColor)
            dial.colorSelected.connect(self._controller.setCurrentLayerColor)
            dial.destroyed.connect(self._controller.resetCurrentLayerColor)
            dial.rejected.connect(self._controller.resetCurrentLayerColor)
            dial.show()
        else:
            GPrint("Impossible to set color : no layer loaded", "!!")

    def switchToApp(self):
        # TODO Add functionality to switch to app
        pass

    def refreshLayerList(self):
        self._layerList.refreshList(self._controller.layerSet())

    def viewLayer(self, layerName):
        layer = self._controller.getLayer(layerName)
        if layer:
            self._tabW.layerTab().viewLayer(layer)
            self._controller.setCurrentLayer(layer)
