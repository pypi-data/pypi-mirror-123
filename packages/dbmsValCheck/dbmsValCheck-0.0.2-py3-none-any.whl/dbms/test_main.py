from dbms.mysql_con import MYSQLdb
from dbms.sf_con import Snowflakedb
import json

if __name__ == "__main__":
    with open("dbinfo.json") as con:
        dbinfo = json.loads(con.read())
    print(dbinfo)
    MYSQLdb.validate(user=dbinfo['MYSQL_USER'], pwd=dbinfo['MYSQL_PWD'], host=dbinfo['MYSQL_HOST'], port=dbinfo['MYSQL_PORT'], db=dbinfo['MYSQL_DB'])