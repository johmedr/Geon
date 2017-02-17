from PyQt4.Qt import QDialog, QFormLayout, QCheckBox, QLineEdit, QLabel, QPushButton, SIGNAL


# FIXME Clean this, using QDialog default signals instead of new buttons (accept())
class GDialImportDatabaseData(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)

        self.setWindowTitle("Import data from database")
        layout = QFormLayout(self)

        layout.addRow(QLabel("Database : " + self.parent().controller().databaseName()))
        layout.addRow(QLabel("Tables : "))
        self._tables = self.parent().controller().databaseTables()
        self._tablesItem = []
        for t in self._tables:
            cb = QCheckBox(t)
            self._tablesItem.append(cb)
            layout.addRow(cb)

        self._subset = QLineEdit(self)
        layout.addRow("Subset : ", self._subset)

        # TODO add More option (geom column, ...)
        validateButton = QPushButton("Ok", self)
        self.connect(validateButton, SIGNAL("clicked()"), self.validate)
        layout.addRow(validateButton)
        self.setLayout(layout)
        self.show()

    def validate(self):
        for i in range(0, len(self._tablesItem)):
            if self._tablesItem[i].isChecked():
                self.parent().controller().createLayerFromTable(self._tables[i], self._subset.text())
        self.parent().refreshLayerList()
        self.close()
