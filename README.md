# Kuga DBMS

Kuga DBMS is a simple database management system implemented in Python. It allows users to create tables, insert data, update records, delete records, search for records, and export/import data from CSV files.

## How to Execute

1. **Prerequisites**: Make sure you have Python installed on your system.

2. **Clone the Repository**: Clone this repository to your local machine using the following command:
    ```
    git clone https://github.com/kushalMundra26/kuga-dbms.git
    ```

3. **Navigate to the Directory**: Enter the cloned directory:
    ```
    cd kuga-dbms
    ```

4. **Execute the Code**: Run the `main.py` file using Python:
    ```
    python kuga.py
    ```

5. **Enter Queries**: Once the program is running, you can enter queries in the command line interface. Follow the specified formats described below.

## Query Formats

### 1. Create Table
```
create table <table_name> <column_headings>
```

- `<table_name>`: Name of the table to be created.
- `<column_headings>`: Comma-separated list of column headings enclosed in parentheses. Example: `(Name, Age, Gender)`

### 2. Insert Data
```
insert in <table_name> (<data_entries>)
```

- `<table_name>`: Name of the table to insert data into.
- `<data_entries>`: Comma-separated list of data entries enclosed in parentheses. Example: `(John, 30, Male)`

### 3. Update Data
```
update <table_name> <column_name> <new_value> where <condition_column> = <condition_value>
```

- `<table_name>`: Name of the table to update.
- `<column_name>`: Name of the column to update.
- `<new_value>`: New value to set for the specified column.
- `<condition_column>`: Column to use for the condition.
- `<condition_value>`: Value that must match the condition column for the update to occur.

### 4. Delete Data
```
delete from <table_name> where <condition_column> = <condition_value>
```

- `<table_name>`: Name of the table to delete data from.
- `<condition_column>`: Column to use for the condition.
- `<condition_value>`: Value that must match the condition column for the deletion to occur.

### 5. Print the entire table
```
select * from <table_name>
```

- `<table_name>`: Name of the table to search.

### 6. Print Specific Columns
```
select <column_names> from <table_name>
```

- `<column_names>` : List of columns that you want to print. Example: `id,first_name,gender`
- `<table_name>`: Name of the table to search.

### 7. Search Data
```
select * from <table_name> where <condition_column> = <condition_value>
```

- `<table_name>`: Name of the table to search.
- `<condition_column>`: Column to use for the condition.
- `<condition_value>`: Value to search for in the condition column.

### 8. Search and print specific columns with conditions
```
select <column_names> from <table_name> where <condition_column> = <condition_value>
```

- `<column_names>` : List of columns that you want to print. Example: `id,first_name,gender`
- `<table_name>`: Name of the table to search.
- `<condition_column>`: Column to use for the condition.
- `<condition_value>`: Value to search for in the condition column.

### 9. Export Data to CSV
```
export to <csv_file_name> from <table_name>
```

- `<csv_file_name>`: Name of the CSV file to export data to.
- `<table_name>`: Name of the table to export data from.

### 10. Import Data from CSV
```
import <csv_file_name> as <table_name>
```

- `<csv_file_name>`: Name of the CSV file to import data from.
- `<table_name>`: Name of the table to import data into.
