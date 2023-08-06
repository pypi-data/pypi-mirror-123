import mysql.connector
import cx_Oracle
from src.database.utils import DatabaseConfig


class Connection:
    def __init__(self, db_config: DatabaseConfig):
        self.db_type = db_config.db_type.lower()
        if self.db_type == 'mysql':
            self.conn = get_mysql_connection(db_config.db_host, db_config.db_name, db_config.db_user, db_config.db_pwd)
        elif self.db_type == 'oracle':
            self.conn = get_oracle_client_connection(db_config.db_host, db_config.db_user, db_config.db_pwd, db_config.db_client)

    def get_conect(self):
        return self.conn


def get_mysql_connection(db_host: str, db_name: str, db_user: str, db_pwd):
    return mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_pwd)


def get_oracle_connection(db_host: str, db_user: str, db_pwd):
    conn_str = db_user + '/' + db_pwd + '@' + db_host
    return cx_Oracle.connect(conn_str)


def get_oracle_client_connection(db_client: str, db_user: str, db_pwd: str, db_host: str):
    if globals()['is_connected_oracle_client'] is False:
        cx_Oracle.init_oracle_client(lib_dir=rf'{db_client}')
        globals()['is_connected_oracle_client'] = True

    return cx_Oracle.connect(user=db_user,
                             password=db_pwd,
                             dsn=db_host)
