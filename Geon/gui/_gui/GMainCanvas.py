from qgis.gui import QgsMapCanvas

from Geon.core import GLayerSet


class GMainCanvas(QgsMapCanvas):
    def __init__(self):
        self._layerSet = None
        self._displayDict = dict()
        QgsMapCanvas.__init__(self)

    def setLayerSet(self, layerSet):
        self._layerSet = layerSet
        for l in layerSet:
            self._displayDict.update({l: True})
        self.refresh()

    def hideLayer(self, layer):
        self._displayDict[layer] = False
        self.refresh()

    def showLayer(self, layer):
        self._displayDict[layer] = True
        self.refresh()

    def moveLayerUp(self, layer):
        newIndex = self._layerSet.index(layer) - 1
        if newIndex >= 0:
            self._layerSet.remove(layer)
            self._layerSet.insert(newIndex, layer)
            if newIndex - 1 >= 0:
                if self._displayDict[self._layerSet[newIndex - 1]]:
                    self.refresh()

    def moveLayerDown(self, layer):
        newIndex = self._layerSet.index(layer) + 1
        if newIndex < len(self._layerSet):
            self._layerSet.remove(layer)
            self._layerSet.insert(newIndex, layer)
            if newIndex + 1 < len(self._layerSet):
                if self._displayDict[self._layerSet[newIndex + 1]]:
                    self.refresh()

    def refresh(self):
        ls = GLayerSet()
        for l in self._layerSet:
            if self._displayDict[l]:
                ls.append(l)
        QgsMapCanvas.setLayerSet(self, ls)
        QgsMapCanvas.refresh(self)
