from PyQt4.Qt import QColorDialog


class GDialColorSelection(QColorDialog):
    def __init__(self, parent=None):
        QColorDialog.__init__(self, parent)
