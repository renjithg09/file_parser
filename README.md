# Import-data-into-PostgreSQL-from-CSV-file-using-python
<img src="https://github.com/renjithg09/file_parser/blob/master/image_csv.png">

## Introduction:
Our aim is to import data into PostgreSQL database from all CSV files which are present in a folder.
## Prerequisites
This would be running in docker.

## Table details:

call_log :
Call Date/Time, Call Disposition, Phone Number, First Name, Last Name, Address1, Address2, City, State, Zip data will be imported from csv file.

imported_files:
imported_datetime, filename, total_rowcount, imported_rowcount will be inserted while importing above data for tracking purpose/

## File/Folder details:

requirements.txt : It consists, packages to be pip installed.

tablecreate.py : In this python file, we are creating tables (if already not exist) on database fileparser.We are keeping our PostgreSQL queries into a dictionary named"TABLES={}"
By using for loop we are executing the queries into database for creating table.

importcsv.py : In this python file, we are importing required data from CSV files to call_log table. Also insert the imported file information  into imported_files table for tracking purpose.

dockerfile : It contains commands that are used to assemble an image.

docker-compose.yml : Build the component images using dockerfile. Contains environment variable, connection to postgres db.

results_screenshots : It consists, test results screen shots

data: csv files are present in this folder.

README.md : describes the whole project.

image_csv.png : image to display in README.md 

## Running the tests:

1. Get all csv files from the folder.
2. Connect to the db by using connection string URI from the environment variable.
3. Create the required tables if those are not already present.
4. Loop through the abovefetched files.
5. Verify whether the file is already imported or not, if already imported then print a message and loop will go to next file.
6. if it's not already imported then read the csv data to a data frame.
7. Verify csv file is a valid one like mandatory fields are available. (most available name formats are handled with dict).
8. if mandatory fields are not available then print a message and loop will go to next file.
9. if mandatory fields are available then verifying nonmandatory fields, if missing create nonmanadatory columns in data frame,renaming columns aligned with db tables.
10. remove the rows which doesn't have required fields data empty.
11. After above steps will get the valid data frame to import.
12. if data frame is invalid go to next file.
13. Import the valid data frame to call_log table and also insert imported file details to imported_files table.
14. Once all operations are done finally close the db connection.  

 
## Interpretation and Assumptions

CSV files column header names can be different for e.g. "disposition" column name can be "status". Based on the  given csv files (which are in data folder) all names are handled. If we will have more name differences then add those to rename_dict,columndict dictionaries.i.e. values other than these dict will be considered 'unknown'.

Regarding mandatory fields (Call Date/Time, Call Disposition, Phone Number,): Verified these columns are available in the csv file to import the file data. Also verified, these columns are available however the data is empty(""),  if it is empty then will skip that row to be imported.

Imported files are tracking in imported_files table. Currently verifying with file name (case sensitive now can be changed to case insensitive if required) to avoid duplicate import.In future we can do data unique comparing as well to avoid import duplicate file even it has a different  file name.   

Importing csv data to db in a single command i.e. not in a loop hence if any exception comes then that whole file import will be skipped and will try to import next file.(already above validation is in place exception could be some other reason.Note: Based on any future requirement we can change this row wise importing i.e. if any row has exception then skip and try to import other rows. )

Text 'NA' values are handled while reading from csv to avoid the 'NA' to import as NaN.

Many other things also can be done like imported files move to another folder(like processed), show reason for not exporting row (if any) etc. 

This project runs in docker.

Most of the exceptions are handled still there could be some exceptions can be handled in future like folder not available etc.

Based on the end user requirements messages can be changed.


## Result screenshots

Results screen shots are available at https://github.com/renjithg09/file_parser/tree/master/results_screenshots

0_docker_builid.png : docker compose building.
1_successfully_ran_reslut.png : psql connection successful and data imported successfully.
2-docker_connected_to_db : connected to psql and queried the data.
3_docker_imported_data.png : queried all imported data i.e. from call_log & imported_files
4_docker_GUI_run.png : run results from GUI
5_docker_GUI_containers.png : container information from GUI


## Future works

py unit test cases can be added.
Setup a CI/CD pipeline.
Add the ability to read from Google Cloud Storage.
