from PyQt4.Qt import QFileDialog


class GDialImportVectorFileData(QFileDialog):
    def __init__(self, parent=None):
        QFileDialog.__init__(self, parent)
        self.setNameFilter(self.tr("Geospatial vector data format (*.shp *.kml *.geojson *.svg)"))
        self.setAcceptMode(QFileDialog.AcceptOpen)
        self.setFileMode(QFileDialog.ExistingFile)
