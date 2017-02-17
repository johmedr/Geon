from PyQt4.Qt import QListWidget, QListWidgetItem, QAbstractItemView

from Geon.core import GLayerSet


class GEditorLayerListW(QListWidget):
    def __init__(self, parent, layerSet=None):
        QListWidget.__init__(self, parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        if layerSet:
            self._layerSet = layerSet
        else:
            self._layerSet = GLayerSet()

        if layerSet:
            for l in layerSet.rawLayers:
                self.addItem(QListWidgetItem(l.name(), self))
        self.show()

    def selectionChanged(self, QItemSelection, QItemSelection_1):
        self.parent().parent().viewLayer(self.selectedItems()[0].text())

    def refreshList(self, layerSet):
        if layerSet:
            for l in layerSet.rawLayers:
                if not self._layerSet.contains(l):
                    print l.name()
                    self.addItem(QListWidgetItem(l.name(), self))
                    self._layerSet.addLayers(l)
