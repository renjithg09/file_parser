# Import-data-into-PostgreSQL-from-CSV-file-using-python


## Introduction:
Our aim is to import data into PostgreSQL database from CSV files which are present in a folder.

## Prerequisites
This would be running in docker.

## Running the tests

tablecreate.py in this python file we are creating tables (if already not exist) on database fileparser.We are keeping our PostgreSQL queries into a dictionary named"TABLES={}"
By using for loop we are executing the queries into database for creating table.

1. importcsv.py in this python file we are importing data from CSV files to call_log table. Also insert the imported file information  2. into imported_files table.
3. First we are connecting to db using connection string from environement variable.
4. Looping through the folder and getting the csv files.
5. Verifying whether file is already imported or not, if already imported then print a message and loop will go to next file.
6. if it's not already imported then verifying csv file is a valid one like mandatory fields are available (most available formats are handled.Handled with dict).
7. if mandatory fields are not available then print a message and loop will go to next file.
8. if mandatory fields are available then verifying nonmandatory fields, if missing create nonmanadatory columns in data frame,renaming columns as per db tables.
9. after above steps get the valid data  frame to import.
10. Import the data frame to call_log table and also imsert imported file deatils to imported_files table.
11. While importing if mandatory fields data is empty then avoiding those rows. 

 
## Interpretation and Assumptions

csv files colum header names can be different for e.g. "disposition" colum name can be "status". Based on the  given csv files (which are in data folder) all names are handled. If we will have more name differences then add those to rename_dict,columndict dictionaries.i.e. values other than these dict will be considered 'unknown'.

regarding mandotry fields (Call Date/Time, Call Disposition, Phone Number,): Verified these columns are availabe in the csv file to import the file data. Also verified, these columns are available however the data is empty(""),  if it is empty then will skip that row to be imported.

Imported files are tracking in imported_files table. Currently verifying with file name to avoide duplicate import.In future we can do data unique comparing as well to avoid import duplicate file even it has a different  file name.   

Importing csv data to db in a single command i.e. not in a loop hence if any exception comes then that whole file import will be skipped and will try to import next file.(already above validation is in place exception could be some other reason.Note: Based on any future requirement we can change this row wise importing i.e. if any row has exception then skip and try to import other rows. )

Most of the exceptions are handled still there could be some exceptions can be handled in future like folder not avaialble etc.

Based on the end user requirements messages can be changed.



## Result screenshots

Reslults screen shots are available at https://github.com/renjithg09/file_parser/tree/master/results_screenshots


## Future works

py unit test cases can be added.
Setup a CI/CD pipeline.
Add the ability to read from Google Cloud Storage.

