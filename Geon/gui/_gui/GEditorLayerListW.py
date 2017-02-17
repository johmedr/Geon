from PyQt4.Qt import QListWidget


class GEditorLayerListW(QListWidget):
    def __init__(self, parent, layerSet=None):
        QListWidget.__init__(self, parent)
        if layerSet:
            for l in layerSet.rawLayers:
                self.addItem(l.name())
        self.show()

    # TODO Add coordination with current layer view

    # FIXME Multi import error (this should not load the entire layerSet each time)
    def refresh(self, layerSet):
        for l in layerSet.rawLayers:
            self.addItem(l.name())
