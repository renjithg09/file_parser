# Import-data-into-PostgreSQL-from-CSV-file-using-python


## Introduction:
Our aim is to import data into PostgreSQL database from CSV files which are present in a folder.

## Prerequisites
To do this work we have to do first install python on our machine, also have setup PostgreSQL, pandas, psycopg2. Congigure an environment variable "PGCONECTION" with postgress uri details.

## Running the tests

tablecreate.py in this python file we are creating tables on database.We are keeping our PostgreSQL queries into a dictionary named"TABLES={}"
By using for loop we are executing the queries into database for creating table.

1. importcsv.py in this python file we are importing data from CSV files to call_log table. Also insert the imported file information  2. into imported_files table.
3. First we are connecting to db using connection string from environement variable.
4. Looping through the folder and getting the csv files.
5. Verifying whether file is already imported or not, if already imported then print a message and loop will go to next file.
6. if it's not already imported then verifying csv file is a valid one like mandatory fields are available etc.
7. if mandatory fields are not available then print a message and loop will go to next file.
8. if mandatory fields are available then verifying nonmandatory fields, if missing create nonmanadatory columns in data frame,renaming columns as per db tables.
9. after above steps get the valid data  frame to import.
10. Import the data frame to call_log table and also imsert imported file deatils to imported_files table.

 
## After inserting data the database screenshot

