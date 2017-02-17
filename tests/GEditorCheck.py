import sip

for api in ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]:
    sip.setapi(api, 2)

from Geon.gui import *
from Geon.utils import *
from Geon.editor import *

app = GInit()

ctrl = GEditorController()
m = GEditorMainWindow(ctrl)
m.show()

app.exit(app.exec_())
