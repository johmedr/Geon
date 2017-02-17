from PyQt4.Qt import Qt


# Will be useful to store the common properties and functions of layers
class GLayer:
    def __init__(self, baseName="", name=""):
        self._baseName = baseName
        self._name = name

    def name(self):
        return self._baseName

    def __str__(self):
        return self._name

    def _getColor(self):
        return Qt.white

    def _setColor(self, color):
        pass

    color = property(_getColor, _setColor)
