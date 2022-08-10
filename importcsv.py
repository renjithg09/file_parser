import os
import sys
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from datetime import datetime


class csvhandler:
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
    # List of columns which are not in format
    rename_dict = {
        "Call Date EST": "call_datetime",
        "Disposition": "disposition",
        "Phone Number": "phonenumber",
        "First Name": "first_name",
        "Last Name": "last_name",
    }

    def verifymissingmandatorycolumns(self, dtframe):
        # ASSUMPTION :- cvs files will have columns name like this else will consider these columns are not available
        columnlist = ("Call Date EST", "Disposition", "Phone Number")
        result = ""
        # Loop through the manadatory columns and get if those missing in csv
        for mandatorycolumns in columnlist:
            if mandatorycolumns not in dtframe:
                if result != "":
                    result += ", "
                result += str(mandatorycolumns)

        return result

    # Nonmandatory columns can be missed in csv file, if so create those with empty data
    def createmissingnonmandatorycolumns(self, dtframe):
        # ASSUMPTION :- cvs files will have columns name like this else will consider these columns are not available
        columnlist = (
            "First Name",
            "Last Name",
            "Address1",
            "Address2",
            "City",
            "State",
            "Zipcode",
        )
        for nonmandatorycolumns in columnlist:
            if nonmandatorycolumns not in dtframe:
                dtframe.insert(0, nonmandatorycolumns, None)

    # Get the files for folders
    def getthefiles(self, folderpath):
        # list file and directories
        return os.listdir(folderpath)

    # Check file is already imported
    def isfileareadyimported(self, filename, conn):
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

    def dbconnect(self):
        """Connect to the PostgreSQL database server"""
        conn = None
        try:
            # connect to the PostgreSQL server
            print("Connecting to the PostgreSQL database...")
            uri = os.environ.get("PGCONNECTION")
            # print(uri)
            conn = psycopg2.connect(
                uri
            )  # "postgresql://postgres:admin@localhost/fileparser")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            sys.exit(1)
        print("Connection successful")
        return conn

    def isvalidcsvandgetdf(self, csvfilename):
        # Get the file name from whole path
        onlyfilename = os.path.split(csvfilename)[1]
        calldata = pd.read_csv(csvfilename)
        df = pd.DataFrame(calldata)
        # Verify any manadatory columns missig in the csv file
        validationresult = self.verifymissingmandatorycolumns(df)
        if validationresult != "":
            print(
                "{0} not find in the file {1}.".format(validationresult, onlyfilename)
            )
            # empty df to be returned if validation is not successful to don't import
            df = pd.DataFrame()
        else:
            # if vlidation is successfull create missing nonmandatory fields if any
            self.createmissingnonmandatorycolumns(df)
            # Rename the df columns as per db column name to import
            df = df.rename(columns=self.rename_dict)
            # Only select required columns from df to import
            df = df.loc[
                :,
                df.columns.isin(self.call_log_column_list),
            ]
        return df

    def ImportcsvData(self, conn, filename, df):
        """
        Using psycopg2.extras.execute_values() to insert the dataframe
        """
        totalRow = len(df)
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
            totalRow,
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

    def closedbconnection(self):
        conn.close()


ch = csvhandler()

impfolder = ".\data"
impfiles = ch.getthefiles(impfolder)

impconn = ch.dbconnect()  # connect the db
try:
    for ifile in impfiles:  # Loop through the folder where files are present
        impfilename = r"" + impfolder + "\\" + ifile
        if impconn:
            if not ch.isfileareadyimported(
                ifile, impconn
            ):  # Verify file is already imported
                csvdf = ch.isvalidcsvandgetdf(impfilename)  # get the data from csv file
                if not csvdf.empty:
                    ch.ImportcsvData(impconn, ifile, csvdf)  # import data to db
finally:
    ch.closedbconnection  # close the conection
