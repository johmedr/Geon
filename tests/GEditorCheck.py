import sip

for api in ["QDate", "QDateTime", "QString", "QTextStream", "QTime", "QUrl", "QVariant"]:
    sip.setapi(api, 2)

from Geon.editor import *
from Geon.utils import *

app = GInit()

m = GEditorMainWindow()
m.show()

app.exit(app.exec_())
