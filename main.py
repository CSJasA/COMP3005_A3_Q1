# Jasmine Abuel 101300495
# 2026-11-10

import psycopg2 #Python Postgres database adapter and driver

# Connects to local Postgres database
def connectDatabase():
    # This is where you will input your database connection informations
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="Bunny0624", port="5432")

# Opens sql files
def load_sql_file(filepath):
    with open(filepath, "r") as file:
        return file.read()

#Initalizaes the database
def initialize_database(conn, cursor):

    #Check if the database already exists
    # Select from the information schema to check if the table, 'students' exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'students'
        );
    """)

    tableExists = cursor.fetchone()[0]

    # If it does not exist then create the table
    if not tableExists:
        #print("Creating table...")

        with open("students.sql", "r") as file:
            cursor.execute(file.read())

        conn.commit()

    # Check if the table has data already
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]

    # Reset the data if there is data
    if count > 0:
        #print("Resetting data...")

        cursor.execute("""
            TRUNCATE TABLE students
            RESTART IDENTITY;
        """)
        # We use TRUNCATE to remove ALL data from the table and RESTART to reset the auto-incrementing primary key.

        conn.commit()

    with open("studentsData.sql", "r") as file:
        cursor.execute(file.read())

    conn.commit()

    #print("Database ready.")

# Retrieves all the students in the database
def getAllStudents(cursor):

    cursor.execute("""
        SELECT *
        FROM students
        ORDER BY student_id;
    """)
    # Select alll(*) students by order of their id

    students = cursor.fetchall()

    print("\n===== STUDENTS =====")

    for student in students:
        print(student+"\n")

# Adds a student
def addStudents(conn, cursor, first_name, last_name, email, enrollment_date):

    cursor.execute("""
        INSERT INTO students
        (first_name, last_name, email, enrollment_date)
        VALUES (%s, %s, %s, %s);
    """,
    (first_name, last_name, email, enrollment_date ))
    # Insert the student into the database with the given information

    conn.commit()

    print(f"Added {first_name} {last_name}")

# Updates student email
def updateStudentEmail(conn, cursor, student_id, new_email):

    cursor.execute("""
        UPDATE students
        SET email = %s
        WHERE student_id = %s;
    """,
    (new_email, student_id))
    #Update the student's email in the database with the given student id and new email

    conn.commit()

    print(f"Updated student {student_id}")

# Removes a student
def deleteStudent(conn, cursor, student_id):

    cursor.execute("""
        DELETE FROM students
        WHERE student_id = %s;
    """,
    (student_id,))
    #Delete the student from the database with the given student id

    conn.commit()

    print(f"Deleted student {student_id}")

# main function
def main():
    conn = None
    cursor = None

    try:
        conn = connectDatabase()
        cursor = conn.cursor()
        exit = False # exit condition

        initialize_database(conn, cursor) # set up the databases

        #print("inital data")
        getAllStudents(cursor)

        while (not exit):
            # Menu for easy showcasing of the functionalities
            print("\n-Menu-\n1) Get all Students\n2) Add Student\n3) Update Student Email\n4) Delete Student\n5) Exit")
            choice = input("Enter option: ")

            match choice:
                case "1":
                    getAllStudents(cursor)

                case "2":
                    print("\nAdding Student")

                    FName = input("First name: ")
                    LName = input("Last name: ")
                    Email = input("Email: ")
                    EnDate = input("Enrollment date: ")

                    addStudents(conn, cursor, FName, LName, Email, EnDate)

                case "3":
                    print("\nUpdating Email")
                    StuId = input("Student id: ")

                    #check if student exists
                    cursor.execute("""
                        SELECT *
                        FROM students
                        WHERE student_id = %s;
                    """,
                    (StuId,)
                    )
                    
                    studentExists = cursor.fetchone()

                    # if the student exists
                    if studentExists:
                        Email = input("Email: ")
                        updateStudentEmail(conn, cursor, StuId, Email)
                    else:
                        print("Not a valid student id")
                    
                case "4":
                    print("\nDeleting Student")
                    StuId = input("Student id: ")

                    #check if student exists
                    cursor.execute("""
                        SELECT *
                        FROM students
                        WHERE student_id = %s;
                    """,
                    (StuId,)
                    )
                    
                    studentExists = cursor.fetchone()
                    
                    #check if student exists
                    if studentExists:
                        deleteStudent(conn, cursor, StuId)
                    else:
                        print("Not a valid student id")
                        
                case "5":
                    exit = True

                case _:
                    print("\nNot a valid choice\n")

    except Exception as e:
        print("Error:", e) # catches errors

    #close the cursor and connection
    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

# run main
if __name__ == "__main__":
    main()