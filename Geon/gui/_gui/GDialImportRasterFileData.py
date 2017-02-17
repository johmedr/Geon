from PyQt4.Qt import QFileDialog


class GDialImportRasterFileData(QFileDialog):
    def __init__(self, parent=None):
        QFileDialog.__init__(self, parent)
        self.setNameFilter(self.tr("Geospatial raster data format (*.tfw *.tif *.jp2 *.jpx *.drg"))
        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setFileMode(QFileDialog.ExistingFile)
