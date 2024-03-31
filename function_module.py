import json
import mysql.connector
from mysql.connector import Error


# Establish a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="ce201",  # Replace with your MySQL username
        password="13579",  # Replace with your MySQL password
        database="project_data"  # Replace with the name of your database
    )



# function to create a table
def create_new_table(db_connection, table_name, schema):
    """
    Creates a new table in the database.

    :param db_connection: The database connection object.
    :param table_name: The name of the table to create.
    :param schema: A dictionary representing the table schema, where keys are column names and values are their SQL types and constraints.
    """
    columns = ",\n  ".join([f"{column} {details}" for column, details in schema.items()])
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
      {columns}
    )
    """
    cursor = db_connection.cursor()
    cursor.execute(create_table_query)
    db_connection.commit()
    cursor.close()
    print(f"Table '{table_name}' created successfully.")


# function to delete a table
def delete_table(db_connection, table_name):
    """
    Deletes a table from the database.

    :param db_connection: The database connection object.
    :param table_name: The name of the table to delete.
    """
    delete_table_query = f"DROP TABLE IF EXISTS {table_name}"
    cursor = db_connection.cursor()
    cursor.execute(delete_table_query)
    db_connection.commit()
    cursor.close()
    print(f"Table '{table_name}' has been deleted.")




def test_mysql_connection(host_name, user_name, user_password, db_name):
    """
    Test connection to a MySQL database.

    :param host_name: MySQL server host
    :param user_name: MySQL username
    :param user_password: MySQL password
    :param db_name: Database name
    :return: None
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record}")
    except Error as e:
        print(f"Error: '{e}' occurred while connecting to MySQL")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")





# create table from schema

def create_table_from_schema(db_connection, table_name, schema):
    columns = ",\n  ".join([f"{column} {details}" for column, details in schema.items()])
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
      {columns}
    )
    """
    cursor = db_connection.cursor()
    cursor.execute(create_table_query)
    db_connection.commit()
    cursor.close()

# get data from user


def get_data_from_user(schema):
    data = {}
    for column, details in schema.items():
        if "AUTO_INCREMENT" not in details:  # Skip auto-increment fields
            data[column] = input(f"Enter {column} ({details}): ")
    return data


def save_data_to_json(data, filename='data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_data_from_json(filename='data.json'):
    with open(filename, 'r') as file:
        return json.load(file)



def insert_data(db_connection, table_name, data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor = db_connection.cursor()
    cursor.execute(insert_query, tuple(data.values()))
    db_connection.commit()
    cursor.close()



def delete_all_tables_from_schema(db_connection):
    cursor = db_connection.cursor()
    delete_table(db_connection, "Staff")
    delete_table(db_connection, "Courses")
    delete_table(db_connection, "HR_Officer")
    delete_table(db_connection, "Departments")
    delete_table(db_connection, "HR_Supervisor")
    delete_table(db_connection, "Staff_Course")
    print("all tables deleted")



### data manipulation part

def retrieve_data(db_connection, json_filename='retrieved_data.json'):

    table_name = input("please enter a table name from which you want to retrieve the data: ")
    condition = input("please enter the condition to retrieve the data: ")
    query = f"SELECT * FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"

    cursor = db_connection.cursor(dictionary=True)  # Fetch results as dictionaries
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()

    # Saving to JSON
    with open(json_filename, 'w') as file:
        json.dump(records, file, indent=4, default=str)  # default=str to handle datetime objects

    # Printing the data
    print("Retrieved data:")
    for record in records:
        print(record)

    print(f"\nData has been saved to {json_filename}.")


def save_data_to_json(data, filename='insert_data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def load_data_from_json(filename='insert_data.json'):
    with open(filename, 'r') as file:
        return json.load(file)


def insert_data_from_json(db_connection, table_name, data, json_filename='insert_data.json'):
    # Step 1: Save the data to a JSON file
    save_data_to_json(data, json_filename)

    # Step 2: Read the data from the JSON file
    data_from_file = load_data_from_json(json_filename)

    # Step 3: Insert the data into the MySQL database
    if isinstance(data_from_file, list):  # If multiple records
        for record in data_from_file:
            _insert_single_record(db_connection, table_name, record)
    else:  # If a single record
        _insert_single_record(db_connection, table_name, data_from_file)


def _insert_single_record(db_connection, table_name, data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor = db_connection.cursor()
    cursor.execute(query, tuple(data.values()))
    db_connection.commit()
    cursor.close()


## insert data part

staff_schema = {
    "staffID": "INT PRIMARY KEY",
    "staffName": "VARCHAR(50) NOT NULL",
    "staffUsername": "VARCHAR(50) NOT NULL",
    "staffPassword": "VARCHAR(50) NOT NULL",
    "departmentID": "INT NOT NULL",
}

courses_schema = {
    "course_id": "INT PRIMARY KEY",
    "course_name": "VARCHAR(255) NOT NULL",
    "category": "ENUM('core','soft') NOT NULL",
    "total_hours": "INT NOT NULL",
    "department_id": "INT NOT NULL"
}

hr_officer_schema = {
    "officerID": "INT PRIMARY KEY",
    "officerName": "VARCHAR(50) NOT NULL",
    "officerUsername": "VARCHAR(50) NOT NULL",
    "officerPassword": "INT NOT NULL",
    "departmentID": "INT NOT NULL"
}

departments_schema = {
    "departmentID": "INT PRIMARY KEY",
    "departmentName": "VARCHAR(50) NOT NULL"
}

hr_supervisor_schema = {
    "hrSupervisorID": "INT AUTO_INCREMENT PRIMARY KEY",
    "userID": "INT NOT NULL",
    "userPassword": "VARCHAR(50) NOT NULL"
}

staff_course_schema = {
    "staffCourseID": "INT AUTO_INCREMENT PRIMARY KEY",
    "staffID": "INT NOT NULL",
    "courseID": "VARCHAR(50) NOT NULL",
    "dateEnrolled": "DATE",
}

# A global dictionary to hold all schemas
SCHEMAS = {
    "Staff": staff_schema,
    "Courses": courses_schema,
    "HROfficer": hr_officer_schema,
    "Departments": departments_schema,
    "HrSupervisor": hr_supervisor_schema,
    "StaffCourse": staff_course_schema,
}


def get_table_schema(table_name):
    """
    Retrieves the schema for a specified table.

    :param table_name: The name of the table for which to retrieve the schema.
    :return: The schema dictionary if found, otherwise None.
    """
    return SCHEMAS.get(table_name)





def prompt_data_from_user(schema):
    data = {}
    for column, details in schema.items():
        if "AUTO_INCREMENT" not in details:  # Skip auto-increment fields
            value = input(f"Enter {column} ({details}): ")
            data[column] = value
    return data


def save_data_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_data_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def insert_data_into_db(db_connection, table_name, data):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor = db_connection.cursor()
    cursor.execute(query, tuple(data.values()))
    db_connection.commit()
    cursor.close()


def enhanced_insert_data(db_connection):
    table_name = input("Enter the table name into which the data will be inserted: ")
    schema = get_table_schema(table_name)
    if not schema:
        print(f"Schema for table {table_name} not found.")
        return

    data = prompt_data_from_user(schema)
    json_filename = f"{table_name.lower()}_new_record.json"

    save_data_to_json(data, json_filename)
    data_from_file = read_data_from_json(json_filename)
    insert_data_into_db(db_connection, table_name, data_from_file)

    print(f"Data for {table_name} has been successfully inserted into the database.")


## update data part


def prompt_update_info(schema):
    condition = input("Enter the condition to select the record(s) to update (e.g., 'staffID = 1'): ")
    print("Enter the new values for the fields you wish to update:")
    updates = prompt_data_from_user(schema)
    return condition, updates

def update_data_into_db(db_connection, table_name, condition, updates):
    set_clause = ", ".join([f"{column} = %s" for column in updates])
    values = list(updates.values())
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
    cursor = db_connection.cursor()
    cursor.execute(query, values)
    db_connection.commit()
    cursor.close()

def enhanced_update_data(db_connection):
    table_name = input("Enter the table name from which the data will be updated: ")
    schema = get_table_schema(table_name)
    if not schema:
        print(f"Schema for table {table_name} not found.")
        return

    condition, updates = prompt_update_info(schema)
    update_info = {"condition": condition, "updates": updates}
    json_filename = f"{table_name.lower()}_update_info.json"

    save_data_to_json(update_info, json_filename)
    update_info_from_file = read_data_from_json(json_filename)
    update_data_into_db(db_connection, table_name, update_info_from_file["condition"], update_info_from_file["updates"])

    print(f"Data for {table_name} has been successfully updated in the database.")


## delete data part

def prompt_delete_condition():
    condition = input("Enter the condition to select the record(s) to delete (e.g., 'staffID = 3'): ")
    return condition

def delete_data_from_db(db_connection, table_name, condition):
    query = f"DELETE FROM {table_name} WHERE {condition}"
    cursor = db_connection.cursor()
    cursor.execute(query)
    db_connection.commit()
    cursor.close()

def enhanced_delete_data(db_connection):
    table_name = input("Enter the table name from which the data will be deleted: ")
    if table_name not in SCHEMAS:
        print(f"Schema for table {table_name} not found.")
        return

    condition = prompt_delete_condition()
    delete_info = {"table_name": table_name, "condition": condition}
    json_filename = f"{table_name.lower()}_delete_info.json"

    save_data_to_json(delete_info, json_filename)
    delete_info_from_file = read_data_from_json(json_filename)
    delete_data_from_db(db_connection, delete_info_from_file["table_name"], delete_info_from_file["condition"])

    print(f"Record(s) satisfying the condition '{condition}' have been deleted from '{table_name}'.")
