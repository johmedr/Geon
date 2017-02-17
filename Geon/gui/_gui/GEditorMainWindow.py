from PyQt4.Qt import QMainWindow, Qt

from GDialConnectDatabase import GDialConnectDatabase
from GDocker import GDocker
from GEditorCentralTabW import GEditorCentralTabW
from GEditorLayerListW import GEditorLayerListW
from GEditorMenuBar import GEditorMenuBar
from GEditorStatusBar import GEditorStatusBar


class GEditorMainWindow(QMainWindow):
    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.setWindowTitle("GEditor")

        self._controller = controller

        self.showMaximized()
        self.setMenuBar(GEditorMenuBar(self))

        self.setCentralWidget(GEditorCentralTabW(self))
        self.setStatusBar(GEditorStatusBar(self))

        # Add a docker for layers management
        layerDock = GDocker(self)
        layerDock.setWindowTitle(self.tr("Layers"))
        self._layerList = GEditorLayerListW(layerDock)
        layerDock.setWidget(self._layerList)
        self.addDockWidget(Qt.LeftDockWidgetArea, layerDock)

        self.show()

    def controller(self):
        return self._controller

    def dialConnectDatabase(self):
        dial = GDialConnectDatabase(self)
