verbose = True
defaultHost = "localhost"
defaultPort = "5432"
defaultDatabase = "postgres"
defaultUser = "postgres"
defaultPassword = ""



def printf(msg, flag="Ok"):
    if verbose:
        print "[" + flag + "] " + msg