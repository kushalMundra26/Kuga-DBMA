# Kuga-DBMA
Kuga DBMS is a simple database management system implemented in Python. It allows users to create tables, insert data, update records, delete records, search for records, and export/import data from CSV files.

## How to Execute
Prerequisites: Make sure you have Python installed on your system.

Clone the Repository: Clone this repository to your local machine using the following command:

bash
Copy code
git clone https://github.com/your_username/kuga-dbms.git
Navigate to the Directory: Enter the cloned directory:

bash
Copy code
cd kuga-dbms
Execute the Code: Run the main.py file using Python:

css
Copy code
python main.py
Enter Queries: Once the program is running, you can enter queries in the command line interface. Follow the specified formats described below.

Query Formats
1. Create Table
lua
Copy code
create table <table_name> <column_headings>
<table_name>: Name of the table to be created.
<column_headings>: Comma-separated list of column headings enclosed in parentheses. Example: (Name, Age, Gender)
2. Insert Data
php
Copy code
insert in <table_name> (<data_entries>)
<table_name>: Name of the table to insert data into.
<data_entries>: Comma-separated list of data entries enclosed in parentheses. Example: (John, 30, Male)
3. Update Data
php
Copy code
update <table_name> <column_name> <new_value> where <condition_column> = <condition_value>
<table_name>: Name of the table to update.
<column_name>: Name of the column to update.
<new_value>: New value to set for the specified column.
<condition_column>: Column to use for the condition.
<condition_value>: Value that must match the condition column for the update to occur.
4. Delete Data
php
Copy code
delete from <table_name> where <condition_column> = <condition_value>
<table_name>: Name of the table to delete data from.
<condition_column>: Column to use for the condition.
<condition_value>: Value that must match the condition column for the deletion to occur.
5. Search Data
csharp
Copy code
select * from <table_name> where <condition_column> = <condition_value>
<table_name>: Name of the table to search.
<condition_column>: Column to use for the condition.
<condition_value>: Value to search for in the condition column.
6. Export Data to CSV
css
Copy code
export to <csv_file_name> from <table_name>
<csv_file_name>: Name of the CSV file to export data to.
<table_name>: Name of the table to export data from.
7. Import Data from CSV
javascript
Copy code
import <csv_file_name> as <table_name>
<csv_file_name>: Name of the CSV file to import data from.
<table_name>: Name of the table to import data into.
