from geon.utils import *
from qgis.core import QgsDataSourceURI
from psycopg2 import connect, DatabaseError

class PostGISDatabase():
    def __init__(self, database=defaultDatabase, host=defaultHost, port=defaultPort, user=defaultUser, passwd=defaultPassword):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._passwd = passwd
        self._uri = QgsDataSourceURI()
        self._uri.setConnection(self._host, self._port, self._database, self._user, self._passwd)
        self._isConnected = True
        try:
            self._con = connect(host=self._host, port=self._port, database=self._database, user=self._user, password=self._passwd)
            printf("Database " + self._database + " connected.")
        except DatabaseError, e:
            printf("!!", "Database error : " + e)
            self._isConnected = False

    def __del__(self):
        if self._con:
            self._con.close()

    def sqlRequest(self, sqlString):
        cursor = self._con.cursor()
        cursor.execute(sqlString)
        result = cursor.fetchall()
        return result

    def _getUri(self):
        return self._uri

    getUri = property(_getUri)



