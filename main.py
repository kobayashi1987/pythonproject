import json
import mysql.connector


# Establish a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="ce201",  # Replace with your MySQL username
        password="13579",  # Replace with your MySQL password
        database="project_data"  # Replace with the name of your database
    )


# Create the Staff table in the database
def create_staff_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Staff (
      staffID INT PRIMARY KEY,
      staffName VARCHAR(50) NOT NULL,
      staffUsername VARCHAR(50) NOT NULL,
      staffPassword VARCHAR(50) NOT NULL,
      departmentID INT NOT NULL)
    """)
    db_connection.commit()
    cursor.close()


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


# The main function with the updated workflow
def main():
    # Connect to the database
    db_connection = connect_to_database()

    # Create the Staff table
    create_staff_table(db_connection)

    # Get staff data from the user
    staff_data_from_user = get_staff_data_from_user()

    # Save the staff data to a JSON file
    save_data_to_json(staff_data_from_user)

    # Load the staff data from the JSON file
    staff_data_from_file = load_data_from_json()

    # Insert staff data into the database
    insert_multiple_staff_data(db_connection, staff_data_from_file)

    print('Staff data has been collected, saved to a JSON file, and inserted into the database.')

    print("test github")


if __name__ == '__main__':
    main()
