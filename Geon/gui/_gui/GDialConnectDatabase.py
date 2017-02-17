from PyQt4.Qt import QDialog, QLineEdit, QFormLayout, QPushButton, SIGNAL, QErrorMessage

from Geon.utils import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_DATABASE, DEFAULT_USER, DEFAULT_PASSWORD


class GDialConnectDatabase(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle(self.tr("Connect"))

        # Create inputs
        self._hostLine = QLineEdit(self)
        self._hostLine.setText(DEFAULT_HOST)
        self._portLine = QLineEdit(self)
        self._portLine.setText(DEFAULT_PORT)
        self._databaseLine = QLineEdit(self)
        self._databaseLine.setText(DEFAULT_DATABASE)
        self._userLine = QLineEdit(self)
        self._userLine.setText(DEFAULT_USER)
        self._passwordLine = QLineEdit(self)
        self._passwordLine.setText(DEFAULT_PASSWORD)
        validateButton = QPushButton(self.tr("Validate"), self)

        self.connect(validateButton, SIGNAL("clicked()"), self.validate)

        # Set a form layout
        layout = QFormLayout(self)
        layout.addRow(self.tr("Host : "), self._hostLine)
        layout.addRow(self.tr("Port : "), self._portLine)
        layout.addRow(self.tr("Database : "), self._databaseLine)
        layout.addRow(self.tr("User : "), self._userLine)
        layout.addRow(self.tr("Password : "), self._passwordLine)
        layout.addWidget(validateButton)
        self.setLayout(layout)
        self.show()

    def validate(self):
        host = self._hostLine.text()
        port = self._portLine.text()
        database = self._databaseLine.text()
        user = self._userLine.text()
        password = self._passwordLine.text()
        e = self.parent().controller().connectDatabase(host, port, database, user, password)
        if not e:
            self.parent().statusBar().showMessage(self.tr("Connected to database <" + database + ">"))
            self.close()
        else:
            err = QErrorMessage(self)
            err.setWindowTitle(self.tr("Unable to connect database"))
            err.showMessage("Connection to database failed \n Error : " + str(e))
            err.show()
