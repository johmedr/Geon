from os import system

from PyQt4.QtCore import QFileInfo
from psycopg2 import connect, DatabaseError, ProgrammingError
from qgis.core import QgsDataSourceURI

from Geon.utils import *


class GPostGISDatabase:
    def __init__(self, database=DEFAULT_DATABASE, host=DEFAULT_HOST, port=DEFAULT_PORT, user=DEFAULT_USER,
                 passwd=DEFAULT_PASSWORD):
        self._host = host
        self._port = port
        self._database = database
        self._user = user
        self._passwd = passwd
        self._uri = QgsDataSourceURI()
        self._uri.setConnection(self._host, self._port, self._database, self._user, self._passwd)
        self._isConnected = True
        self._cursor = None
        try:
            self._con = connect(host=self._host, port=self._port, database=self._database, user=self._user,
                                password=self._passwd)
            GPrint("Database " + self._database + " connected.")
        except DatabaseError, e:
            GPrint("!!", "Database error : " + str(e))
            self._isConnected = False

        if self._isConnected:
            self._cursor = self._con.cursor()

    def sqlRequest(self, sqlString):
        self._cursor.execute(sqlString)
        result = None
        try:
            result = self._cursor.fetchall()
        except ProgrammingError, e:
            GPrint(e, "EE")

        return result

    def existsTable(self, tableName):
        exists = True
        try:
            self._cursor.execute("select exists(select * from information_schema.tables where table_name=%s)",
                                 (tableName,))
            exists = self._cursor.fetchone()[0]
        except ProgrammingError, e:
            GPrint(e, "EE")
        return exists

    def tables(self):
        tables = []
        ans = self.sqlRequest("SELECT relname FROM pg_stat_user_tables \
                                WHERE schemaname='public' AND relname!='spatial_ref_sys'")
        for a in ans:
            tables.append(a[0])
        return tables

    def loadShapefile(self, path, preserveSqlFile=False):
        fileInfo = QFileInfo(path)
        if not self.existsTable(fileInfo.baseName()):
            sqlFilePath = str(fileInfo.absolutePath()) + "/" + str(fileInfo.baseName()) + ".sql"
            system("shp2pgsql -c " + path + " > " + sqlFilePath)
            cursor = self._con.cursor()
            cursor.execute(open(sqlFilePath, 'r').read())
            if not preserveSqlFile:
                system("rm -f " + sqlFilePath)

            GPrint("Shapefile " + fileInfo.baseName() + ".shp successfully loaded in database " + str(self))

        else:
            GPrint(fileInfo.baseName() + " exists in " + str(self), "EE")

    def __del__(self):
        if self._con:
            self._con.close()

    def __str__(self):
        return "PostGISDatabase<" + self._uri.connectionInfo() + ">"

    def _getUri(self):
        return self._uri

    def _getUser(self):
        return self._user

    uri = property(_getUri)
    user = property(_getUser)
