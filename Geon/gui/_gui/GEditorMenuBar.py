from PyQt4.Qt import QMenuBar, QMenu, QAction, QKeySequence, SIGNAL, QDialog, QListWidget

from Geon.core import GPostGISDatabase


class GEditorMenuBar(QMenuBar):
    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)

        self._fileM = QMenu(self.tr("File"))
        self._editM = QMenu(self.tr("Edit"))
        self._dataM = QMenu(self.tr("Data"))
        self._layersM = QMenu(self.tr("Layers"))
        self._modelM = QMenu(self.tr("Model"))
        self._optionM = QMenu(self.tr("Options"))

        self.addMenu(self._fileM)
        self.addMenu(self._editM)
        self.addMenu(self._dataM)
        self.addMenu(self._layersM)
        self.addMenu(self._modelM)
        self.addMenu(self._optionM)

        self._connectDatabaseA = QAction(self.tr("Connect a PostGIS database"), self.parent())
        self._connectDatabaseA.setShortcut(QKeySequence("Ctrl+Shift+C"))
        self._dataM.addAction(self._connectDatabaseA)
        self.parent().connect(self._connectDatabaseA, SIGNAL("triggered()"), self.parent().dialConnectDatabase)

        # self._impA = QAction("Add table", self)
        # self._impA.setShortcut(QKeySequence("Ctrl+A"))
        # self._dataM.addAction(self._impA)
        # self.connect(self._impA, SIGNAL("triggered()"), self.dial)

    def dial(self):
        dial = QDialog(self)
        dial.setWindowTitle("Select a layer")
        list = QListWidget(dial)
        db = GPostGISDatabase()
        for t in db.tables():
            list.addItem(t)
        dial.setBaseSize(list.minimumSize())
        dial.show()
