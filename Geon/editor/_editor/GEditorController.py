from Geon.core import GPostGISDatabase


class GEditorController:
    def __init__(self):
        self._database = None

    # Add something to check if db is already connected
    def connectDatabase(self, host, port, database, user, password):
        self._database = GPostGISDatabase(host=host, port=port, database=database, user=user, passwd=password)
        if self._database.isConnected():
            error = False
        else:
            error = self._database.getError()
        return error
