qgisPath = "/home/yop/anaconda2/pkgs/qgis-2.18.2-py27_0"

verbose = True

defaultHost = "localhost"
defaultPort = "5432"
defaultDatabase = "NYC"
defaultUser = "postgres"
defaultPassword = ""



def printf(msg, flag="Ok"):
    if verbose:
        print "[" + flag + "] " + str(msg)