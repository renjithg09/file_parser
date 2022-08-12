# Import-data-into-PostgreSQL-from-CSV-file-using-python


## Introduction:
Our aim is to import data into PostgreSQL database from all CSV files which are present in a folder.

## Prerequisites
This would be running in docker.

## Table details

call_log :
Call Date/Time, Call Disposition, Phone Number, First Name, Last Name, Address1, Address2, City, State, Zip data will be imported from csv file.

imported_files:
imported_datetime, filename, total_rowcount, imported_rowcount will be inserted while importhing above data for tracking purpose/

## Running the tests

tablecreate.py : In this python file, we are creating tables (if already not exist) on database fileparser.We are keeping our PostgreSQL queries into a dictionary named"TABLES={}"
By using for loop we are executing the queries into database for creating table.

importcsv.py: In this python file, we are importing required data from CSV files to call_log table. Also insert the imported file information  into imported_files table for tracking purpose.

steps are below.

1. Get all csv files from the folder.
3. Connect to the db by using connection string URI from the environement variable.
4. Create the required tables if those are not already present.
4. Loop through the abovefetched files.
5. Verify whetherfile is already imported or not, if already imported then print a message and loop will go to next file.
6. if it's not already imported then read the csv data to a data frame.
7. Verify csv file is a valid one like mandatory fields are available. (most available name formats are handled with dict).
8. if mandatory fields are not available then print a message and loop will go to next file.
9. if mandatory fields are available then verifying nonmandatory fields, if missing create nonmanadatory columns in data frame,renaming columns aligned with db tables.
10. remove the rows which doesn't have required fields data empty.
11. After above steps will get the valid data frame to import.
12. if data frame is invalid go to next file.
13. Import the valid data frame to call_log table and also imsert imported file deatils to imported_files table.
14. Once all operations are done finally close the db connection.  

 
## Interpretation and Assumptions

csv files colum header names can be different for e.g. "disposition" colum name can be "status". Based on the  given csv files (which are in data folder) all names are handled. If we will have more name differences then add those to rename_dict,columndict dictionaries.i.e. values other than these dict will be considered 'unknown'.

regarding mandotry fields (Call Date/Time, Call Disposition, Phone Number,): Verified these columns are availabe in the csv file to import the file data. Also verified, these columns are available however the data is empty(""),  if it is empty then will skip that row to be imported.

Imported files are tracking in imported_files table. Currently verifying with file name to avoide duplicate import.In future we can do data unique comparing as well to avoid import duplicate file even it has a different  file name.   

Importing csv data to db in a single command i.e. not in a loop hence if any exception comes then that whole file import will be skipped and will try to import next file.(already above validation is in place exception could be some other reason.Note: Based on any future requirement we can change this row wise importing i.e. if any row has exception then skip and try to import other rows. )

Text 'NA' values are handled while reading from csv, else Text 'NA' will import as NaN.

Most of the exceptions are handled still there could be some exceptions can be handled in future like folder not avaialble etc.

Based on the end user requirements messages can be changed.


## Result screenshots

Reslults screen shots are available at https://github.com/renjithg09/file_parser/tree/master/results_screenshots

0_docker_builid.png : docker compose builing.
1_successfully_ran_reslut.png : psql connection successful and data imported successfully.
2-docker_connected_to_db : connected to psql and queried the data.
3_docker_imported_data.png : queried all imported data i.e. from call_log & imported_files
4_docker_GUI_run.png : run results from GUI
5_docker_GUI_containers.png : container information form GUI


## Future works

py unit test cases can be added.
Setup a CI/CD pipeline.
Add the ability to read from Google Cloud Storage.

