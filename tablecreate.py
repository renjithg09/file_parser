import psycopg2
import os


def createtables(conn):

    # uri = os.environ.get("PGCONNECTION")
    # uri = os.environ.get("PGCONNECTION")
    # print(uri)
    # conn = psycopg2.connect(uri)
    cursor = conn.cursor()
    try:
        TABLES = {}
        TABLES["call_log"] = (
            "CREATE TABLE IF NOT EXISTS public.call_log"
            "(call_datetime timestamp,"
            "disposition VARCHAR(100),"
            "phonenumber VARCHAR(25),"
            "first_name VARCHAR(100),"
            "last_name VARCHAR(100),"
            "address1 VARCHAR(150),"
            "address2 VARCHAR(150),"
            "city VARCHAR(100),"
            "state VARCHAR(100),"
            "zipcode VARCHAR(10))"
        )

        TABLES["imported_files"] = (
            "CREATE TABLE IF NOT EXISTS public.imported_files"
            "(imported_datetime timestamp,"
            "filename VARCHAR(200),"
            "total_rowcount integer,"
            "imported_rowcount integer)"
        )

        for name, ddl in TABLES.items():
            print("Creating table {}: ".format(name))
            cursor.execute(ddl)

        conn.commit()
    finally:
        cursor.close()

# print(os.environ)
# createtables()
