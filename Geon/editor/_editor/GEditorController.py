from Geon.core import GPostGISDatabase, GLayerSet, GVectorLayer


class GEditorController:
    def __init__(self):
        self._database = None
        self._layerSet = None

    # Add something to check if db is already connected
    def connectDatabase(self, host, port, database, user, password):
        # TODO Create a multi-database management functionality ?
        pgdb = GPostGISDatabase(host=host, port=port, database=database, user=user, passwd=password)
        if pgdb.isConnected():
            error = False
            self._database = pgdb
        else:
            error = pgdb.getError()
        return error

    def databaseTables(self):
        if self._database:
            return self._database.tables()
        else:
            return False

    def databaseName(self):
        return self._database.getName()

    def createLayerFromTable(self, tableName, subset):
        # FIXME error if database not connected
        if not self._layerSet:
            self._layerSet = GLayerSet()
        lay = GVectorLayer(postGISDatabase=self._database, table=tableName, baseName=tableName, subset=subset)
        self._layerSet.addLayers(lay)

    def layerSet(self):
        return self._layerSet
