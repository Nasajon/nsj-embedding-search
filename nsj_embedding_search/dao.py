from nsj_sql_utils_lib.dbadapter3 import DBAdapter3


class DAO:
    def __init__(self, dbconn):
        self._db = DBAdapter3(dbconn)
