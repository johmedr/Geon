from PyQt4.Qt import QMenuBar, QMenu, QAction, QKeySequence, SIGNAL, QDialog, QListWidget

from Geon.core import GPostGISDatabase


class GEditorMenuBar(QMenuBar):
    def __init__(self, parent):
        QMenuBar.__init__(self, parent)

        # Menu items
        self._fileM = QMenu(self.tr("File"))
        self._editM = QMenu(self.tr("Edit"))
        self._viewM = QMenu(self.tr("View"))
        self._optionM = QMenu(self.tr("Options"))

        self.addMenu(self._fileM)
        self.addMenu(self._editM)
        self.addMenu(self._viewM)
        self.addMenu(self._optionM)

        # Actions
        self._connectDatabaseA = QAction(self.tr("Connect a PostGIS database"), self.parent())
        self._connectDatabaseA.setShortcut(QKeySequence("Ctrl+Shift+C"))
        self.parent().connect(self._connectDatabaseA, SIGNAL("triggered()"), self.parent().dialConnectDatabase)

        self._importDatabaseDataA = QAction(self.tr("Import data from database"), self.parent())
        self._importDatabaseDataA.setShortcut(QKeySequence("Ctrl+Shift+I"))
        self.parent().connect(self._importDatabaseDataA, SIGNAL("triggered()"), self.parent().dialImportDatabaseData)

        self._importVectorFileDataA = QAction(self.tr("Import vector from file"), self.parent())
        self._importVectorFileDataA.setShortcut(QKeySequence("Ctrl+Shift+V"))
        self.parent().connect(self._importVectorFileDataA, SIGNAL("triggered()"),
                              self.parent().dialImportVectorFileData)

        self._importRasterFileDataA = QAction(self.tr("Import raster data from file"), self.parent())
        self._importRasterFileDataA.setShortcut(QKeySequence("Ctrl+Shift+R"))
        self.parent().connect(self._importRasterFileDataA, SIGNAL("triggered()"),
                              self.parent().dialImportRasterFileData)

        self._colorLayerA = QAction(self.tr("Select layer color"), self.parent())
        self.parent().connect(self._colorLayerA, SIGNAL("triggered()"), self.parent().dialSelectLayerColor)

        # Add actions to menu
        self._fileM.addAction(self._importVectorFileDataA)
        self._fileM.addAction(self._importRasterFileDataA)
        self._fileM.addSeparator()
        self._fileM.addAction(self._connectDatabaseA)
        self._fileM.addAction(self._importDatabaseDataA)

        self._viewM.addAction(self._colorLayerA)

    def dial(self):
        dial = QDialog(self)
        dial.setWindowTitle("Select a layer")
        layerList = QListWidget(dial)
        db = GPostGISDatabase()
        for t in db.tables():
            layerList.addItem(t)
        dial.setBaseSize(layerList.minimumSize())
        dial.show()
