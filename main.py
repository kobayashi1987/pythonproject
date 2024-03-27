import json
import mysql.connector
from function_module import *


# The main function with the updated workflow
def main():

    print("First, we test the connection to mysql database")
    test_mysql_connection('localhost', 'ce201', '13579', 'project_data')

    # Connect to the database
    db_connection = connect_to_database()

    # Create all the necessary tables
    # All the codes for table creation should be used once only unless deleting them after testing


    # This is the delete table part
    # delete_table(db_connection, "Staff")
    # delete_table(db_connection, "Courses")



    # create the Table Schema

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



    # # Creating the Departments table, the following lines of codes could be only used once
    # together with delete Table part


    # create_new_table(db_connection, "Staff", staff_schema)
    # create_new_table(db_connection, "Courses", courses_schema)
    # create_new_table(db_connection, "HR_Officer", hr_officer_schema)
    # create_new_table(db_connection, "Departments", departments_schema)
    # create_new_table(db_connection, "HR_Supervisor", hr_supervisor_schema)
    # create_new_table(db_connection, "Staff_Course", staff_course_schema)

    # # This is the delete table part
    # delete_table(db_connection, "Staff")
    # delete_table(db_connection, "Courses")
    # delete_table(db_connection, "HR_Officer")
    # delete_table(db_connection, "Departments")
    # delete_table(db_connection, "HR_Supervisor")
    # delete_table(db_connection, "Staff_Course")






    #
    # # Get staff data from the user
    # staff_data_from_user = get_staff_data_from_user()
    #
    # # Save the staff data to a JSON file
    # save_data_to_json(staff_data_from_user)
    #
    # # Load the staff data from the JSON file
    # staff_data_from_file = load_data_from_json()
    #
    # # Insert staff data into the database
    # insert_multiple_staff_data(db_connection, staff_data_from_file)
    #
    # # Updating a staff member's department ID
    # update_values = {"departmentID": "77"}  # New department ID
    # condition = "staffID = 7"  # Assuming you want to update the staff with staffID 1
    #
    # update_table_record(db_connection, "Staff", update_values, condition)
    #
    # print('Staff data has been collected, saved to a JSON file, and inserted into the database.')

    print("test github")








if __name__ == '__main__':
    main()
