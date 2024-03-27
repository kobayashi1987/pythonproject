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


# Prompt the user for staff data
def get_staff_data_from_user():
    staff_list = []
    number_of_staff = int(input("Enter the number of staff members: "))
    for i in range(number_of_staff):
        print(f"Enter details for staff member {i + 1}:")
        staff_data = {
            'staffID': input("Enter staff ID: "),
            'staffName': input("Enter staff name: "),
            'staffUsername': input("Enter staff username: "),
            'staffPassword': input("Enter staff password: "),
            'departmentID': input("Enter department ID: ")
        }
        staff_list.append(staff_data)
    return staff_list


# Save staff data to a JSON file
def save_data_to_json(staff_list, filename='data.json'):
    with open(filename, 'w') as file:
        json.dump(staff_list, file, indent=4)


# Load staff data from a JSON file
def load_data_from_json(filename='data.json'):
    with open(filename, 'r') as file:
        staff_list = json.load(file)
    return staff_list


# Insert multiple staff members' data into the database
def insert_multiple_staff_data(db_connection, staff_list):
    cursor = db_connection.cursor()
    insert_query = """
    INSERT INTO Staff (staffID, staffName, staffUsername, staffPassword, departmentID)
    VALUES (%s, %s, %s, %s, %s)
    """
    # Convert the staff list to a list of tuples for insertion
    staff_data_tuples = [(staff['staffID'], staff['staffName'], staff['staffUsername'],
                          staff['staffPassword'], staff['departmentID']) for staff in staff_list]

    cursor.executemany(insert_query, staff_data_tuples)
    db_connection.commit()
    cursor.close()


def update_table_record(db_connection, table_name, update_values, condition):
    """
    Updates records in the specified table.

    :param db_connection: The database connection object.
    :param table_name: The name of the table to update.
    :param update_values: A dictionary where keys are column names to update, and values are the new values.
    :param condition: A string representing the SQL condition to select the record(s) to update.
    """
    set_clause = ", ".join([f"{column} = %s" for column in update_values])
    values = list(update_values.values())

    update_query = f"""
    UPDATE {table_name}
    SET {set_clause}
    WHERE {condition}
    """
    cursor = db_connection.cursor()
    cursor.execute(update_query, values)
    db_connection.commit()
    cursor.close()
    print(f"Record(s) updated successfully in '{table_name}'.")


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
