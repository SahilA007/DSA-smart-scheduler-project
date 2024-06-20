import sqlite3
import re
import os
from settings import IT_COURSES,PROFESSOR_NAMES


def check_database():
    if not os.path.exists("university.db"):
        db_create_tables()
        fill_db_courses(IT_COURSES)
        fill_db_professors(PROFESSOR_NAMES)
        fill_db_classrooms()
    else:
        return True


def db_create_tables():
    #connect to database
    conn = sqlite3.connect('university.db')
    # create a cursor
    cursor = conn.cursor()
    #create a table professor
    # data types in sqllite3: NULL, INTEGER, REAL, TEXT, BLOB
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS professors (
                title TEXT,
                first_name TEXT,
                last_name TEXT)
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses(name TEXT)
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classrooms(bloc TEXT, room INTEGER)
    """)

    #execute command
    conn.commit()
    #close connection
    conn.close()

# fill methods
    
def fill_db_professors(profnames):
    prof_list = []
    for name in profnames:
        title,fullname = name.split(".")
        first_name,last_name = fullname.strip().split(" ")
        prof_list.append((title,first_name,last_name))
    
    #Insert the data into the professors db table
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO professors VALUES (?,?,?)",prof_list)
    conn.commit()
    print("Insert complete")
    conn.close()

def fill_db_courses(courses):
    courses_list = [(course,) for course in courses]
    
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO courses (name) VALUES (?)",courses_list)
    conn.commit()
    print("Insert complete")
    conn.close()

def fill_db_classrooms():
    class_list = []
    for room in range(1,61):
        class_list.append(("c",room))
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO classrooms (bloc,room) VALUES (?,?)",class_list)
    conn.commit()
    print("insert complete")
    conn.close()

# add methhods
    
def add_course(course):
    if course and not course.isspace():
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        #check if the course already exists in the db
        cursor.execute("SELECT * FROM courses where name = ?",(course,))
        if len(cursor.fetchall()) != 0:
            raise ValueError("Course already exists")
        else:
            cursor.execute("INSERT INTO courses (name) VALUES (?)",(course,))
            conn.commit()
        conn.close()
        return True
    else:
        raise ValueError ("Invalid course name")
    
def add_professor(professor):
    #check if professor name is a valid name
    pattern = r"^(Prof.|Dr.){1}\s[a-zA-Z]+\s[a-zA-Z]+$"
    if re.match(pattern,professor):
        #check if the professor already exists in the db
        title,fullname = professor.title().split(".")
        first_name,last_name = fullname.strip().split(" ")

        conn= sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("""SElECT * FROM professors where 
                       title = ? 
                       AND first_name = ?
                       AND last_name = ? """,(title,first_name,last_name))
        if len(cursor.fetchall()) != 0:
            raise ValueError("Professor name already exists")
        else:
            cursor.execute("INSERT INTO professors VALUES (?,?,?)",(title,first_name,last_name))
            conn.commit()
        conn.close()
        return True
    else:
        raise ValueError("Invalid professor name")

def add_classroom(classroom):
    #check if the classroom is valid
    pattern = r'^[a-z]+\s[0-9]+$'
    if re.match(pattern,classroom):
        #check if the classroom already exists in the database
        bloc,room = classroom.split(' ')
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM classrooms where
                       bloc = ?
                       AND room = ?""",(bloc,room))
        if len(cursor.fetchall()) != 0:
            raise ValueError("classroom already exists")
        else:
            cursor.execute("INSERT INTO classrooms VALUES (?,?)",(bloc,room))
            conn.commit()
        conn.close()
        return True
    else:
        raise ValueError("Invalid classroom number")

#delete methods
def delete_course(course):
    if course and not course.isspace():
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses where name = ?",(course,))
        if len(cursor.fetchall()) != 0:
            cursor.execute("DELETE FROM courses WHERE NAME = ?",(course,))
            conn.commit()
            conn.close()
            return True
        else:
            raise ValueError("Course does not exist")
    else:
        raise ValueError("Invalid course name")

def delete_professor(prof):
    #check if professor name is a valid name
    pattern = r"^(Prof.|Dr.){1}\s[a-zA-Z]+\s[a-zA-Z]+$"
    if re.match(pattern,prof):
        title,fullname = prof.title().split(".")
        first_name,last_name = fullname.strip().split(" ")
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("""SElECT * FROM professors where 
                       title = ? 
                       AND first_name = ?
                       AND last_name = ? """,(title,first_name,last_name))
        if len(cursor.fetchall()) != 0:
            cursor.execute("DELETE FROM professors WHERE title = ? AND first_name = ? AND last_name = ?",(title,first_name,last_name))
            conn.commit()
            conn.close()
            return True
        else:
            raise ValueError("Professor does not exist")
    else:
        raise ValueError("Invalid professor name")

def delete_classroom(classroom):
    #check if the classroom number is valid
    pattern = r"^[a-zA-Z]{1}\s[0-9]+$"
    if re.match(pattern,classroom):
        bloc,number = classroom.split(" ")
        conn = sqlite3.connect("university.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM classrooms where
                       bloc = ?
                       AND room = ?""",(bloc,number))
        if len(cursor.fetchall()) != 0:
            cursor.execute("DELETE FROM classrooms WHERE bloc = ? AND room = ?",(bloc,number))
            conn.commit()
            conn.close()
            return True
        else:
            raise ValueError("Classroom does not exist")
    else:
        raise ValueError("Invalid classroom number")
    
#display methods
def display_professors_table():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professors")
    for item in cursor.fetchall():
        print(f"{item[0]}---{item[1]}---{item[2]}")
    conn.close()

def display_courses_table():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    for item in cursor.fetchall():
        print(f"{item[0]}")
    conn.close()

def display_classrooms_table():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classrooms")
    for item in cursor.fetchall():
        print(f"{item[0]}{item[1]}")
    conn.close()

#get methods
def get_professors():
    professors=[]
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professors")
    for item in cursor.fetchall():
        professors.append(f"{item[0]}. {item[1]} {item[2]}")
    conn.close()
    return professors

def get_courses():
    courses=[]
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    for item in cursor.fetchall():
        courses.append(f"{item[0]}")
    conn.close()
    return courses

def get_classrooms():
    classrooms = []
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classrooms")
    for item in cursor.fetchall():
        classrooms.append(f"{item[0]} {item[1]}")
    conn.close()
    return classrooms
