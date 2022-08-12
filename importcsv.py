import os
import sys
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from datetime import datetime
import tablecreate


class CsvHandler:
    def __init__(self):
        self.totalrowcount = 0

    # List of tables where data to be imported
    table_list = ("public.call_log", "public.imported_files")
    # List of column where data to be imported
    call_log_column_list = (
        "call_datetime",
        "disposition",
        "phonenumber",
        "first_name",
        "last_name",
        "zip",
        "Address1",
        "Address2",
        "City",
        "State",
    )

    def renamenonmandatorycolumns(self, dtframe):
        # List of non mandatory columns which are not in format. Given csv files has these many different type format hence included these.
        rename_dict = {
            "first_name": ("First Name", "firstname", "first"),
            "last_name": ("Last Name", "lastname", "last"),
            "zipcode": ("zip", "Zipcode"),
        }
        # Loop through the non manadatory columns and rename to align with psql table column
        # print(dtframe.columns)
        for mkey, mvalue in rename_dict.items():
            for colname in mvalue:
                if colname in dtframe.columns:
                    dtframe.rename(columns={colname: mkey}, inplace=True)

    def verify_missing_mandatory_columns(self, dtframe):
        # ASSUMPTION :- cvs files will have columns name like this else will consider these columns are not available

        columndict = {
            "call_datetime": ("Call Date EST", "created_at"),
            "disposition": ("Disposition", "status"),
            "phonenumber": ("Phone Number", "phone1"),
        }
        result = ""
        # Loop through the manadatory columns and verify if those missing in csv
        for mkey, mvalue in columndict.items():
            reqcols = ""
            for colname in mvalue:
                if colname not in dtframe.columns:
                    if reqcols != "":
                        reqcols += "/"
                    reqcols += colname
                else:
                    reqcols = ""
                    dtframe.rename(columns={colname: mkey}, inplace=True)
                    break
            if reqcols != "":
                if result != "":
                    result += ", "
                result += reqcols
        return result

    # Nonmandatory columns can be missed in csv file, if so create those with empty data
    def create_missing_nonmandatory_columns(self, dtframe):
        # ASSUMPTION :- cvs files will have columns name like this else will consider these columns are not available
        columnlist = (
            "first_name",
            "last_name",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
        )
        for nonmandatorycolumns in columnlist:
            if nonmandatorycolumns not in dtframe.columns:
                dtframe.insert(0, nonmandatorycolumns, None)

    # Get the files for folders
    def get_the_files(self, folderpath):
        # list file and directories
        return os.listdir(folderpath)

    # Check file is already imported
    def is_file_aready_imported(self, filename, conn):
        # Prepare the sql to find importing file is already imported
        mysql = "SELECT 1 FROM {0} WHERE filename ='{1}'".format(
            self.table_list[1], filename
        )
        cursor = conn.cursor()
        try:
            dframe = cursor.execute(mysql)
            record = cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Call log Error: %s" % error)
            conn.rollback()
            cursor.close()
            return True

        if record:
            print("{0} file is already imported.".format(filename))
            return True
        else:
            return False
        cursor.close()

    def db_connect(self):
        """Connect to the PostgreSQL database server"""
        conn = None
        try:
            # connect to the PostgreSQL server
            # print("Connecting to the PostgreSQL database...")
            # Get the ps URI from env variable
            uri = os.environ.get("DB_URL")
            # print(uri)
            conn = psycopg2.connect(
                uri
                 #"postgresql://postgres:admin@localhost/fileparser"
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            sys.exit(1)
        # print("Connection successful")
        return conn

    def is_valid_csv_and_get_df(self, csvfilename):
        # Get the file name from whole path
        onlyfilename = os.path.split(csvfilename)[1]
        # Get the csv data, pass na_filter false to hand NA string
        calldata = pd.read_csv(csvfilename, na_filter=False)
        df = pd.DataFrame(calldata)
        ch.totalrowcount = 0

        # Verify any manadatory columns missig in the csv file
        validationresult = self.verify_missing_mandatory_columns(df)
        if validationresult != "":
            print(
                "{0} not find in the file {1}.".format(validationresult, onlyfilename)
            )
            # empty df to be returned if validation is not successful to don't import
            df = pd.DataFrame()
        else:
            # Rename the df columns as per db column name to import
            self.renamenonmandatorycolumns(df)
            # create missing nonmandatory fields if any
            self.create_missing_nonmandatory_columns(df)
            # Only select required columns from df to import
            df = df.loc[
                :,
                df.columns.isin(self.call_log_column_list),
            ]
            ch.totalrowcount = len(df)
            # Don't consider to import if below fields are empty
            df = df[df.call_datetime != ""]
            df = df[df.disposition != ""]
            df = df[df.phonenumber != ""]
        return df

    def import_csv_data(self, conn, filename, df):
        """
        Using psycopg2.extras.execute_values() to insert the dataframe
        """

        # Create a list of tupples from the dataframe values
        tuples = [tuple(x) for x in df.values.tolist()]

        # Comma-separated dataframe columns
        cols = ",".join(list(df.columns))
        # SQL query to execute
        query = "INSERT INTO %s(%s) VALUES %%s" % (self.table_list[0], cols)
        cursor = conn.cursor()
        try:
            extras.execute_values(cursor, query, tuples)
            conn.commit()
            impRow = cursor.rowcount
        except (Exception, psycopg2.DatabaseError) as error:
            print("Call log Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1
        query = "INSERT INTO {0} VALUES ('{1}','{2}',{3},{4})".format(
            self.table_list[1],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            filename,
            ch.totalrowcount,
            impRow,
        )
        try:
            cursor.execute(query, [])
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Imported files Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1

        print("{} file Data imported successfully.".format(filename))
        cursor.close()

    def close_db_connection(self):
        conn.close()


ch = CsvHandler()

impfolder = "/app/data"

impfiles = ch.get_the_files(impfolder)

impconn = ch.db_connect()  # connect the db
tablecreate.create_tables(impconn)
try:
    for ifile in impfiles:  # Loop through the folder where files are present
        impfilename = r"" + impfolder + "/" + ifile
        if impconn:
            if not ch.is_file_aready_imported(ifile, impconn):
                # Verify file is already imported
                csvdf = ch.is_valid_csv_and_get_df(
                    impfilename
                )  # get the data from csv file
                if not csvdf.empty:
                    ch.import_csv_data(impconn, ifile, csvdf)  # import data to db

finally:
    ch.close_db_connection  # close the conection
