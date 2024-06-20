from db_setup import *
from course import Course
from settings import COURSES_TYPES
import random


def create_timetable_matrix(n):
    """
    create timetable matrix needed to contain the time table data
    :n: number of classes to generate
    """
    matrix = []
    for group in range(n):
        matrix.append([])
        for r in range(6):
            row = []
            for col in range(6):
                if col in [2,5] and r in [4,5]:
                    row.append("*")
                else:
                    row.append("-") 
            matrix[group].append(row)
    return matrix

def find_empty(matrix):
    """
    find the first empty cell in the timetable matrix
    :return: tuple (class,Row,Column)
    """
    for i,group in enumerate(matrix):
        for j,row in enumerate(group):
            for k,course in enumerate(row):
                if course == "-":
                    return (i,j,k)
    return None

def valid(course,pos,matrix):
    cl,row,col = pos
    # check if the same course does not already exists at that time
    for group in range(len(matrix)):
        if matrix[group][row][col] == course and group != cl:
            return False
    # make sure that the course does not repeat more then one time in the same week
    count = 0
    for i, r in enumerate(matrix[cl]):
        for c in r:
            if c == course:
                count+=1
    if count >1:
        return False
    
    #check if the course already exists in the same day
    for i in range(6):
        if matrix[cl][i][col] == course and i != row:
            return False
    return True

def generate_tables(matrix,courses_list,professors_list,classrooms_list):
    """
    This function is responsible of generating timetables for 
    the various classes using the backtracking algorithm 
    :input: a empty 3d matrix containing the structure of our timetable, 
    a list containg available courses, a list containg available professors, 
    a list containg available classrooms  
    :return: boolean
    """
    courses_types = COURSES_TYPES
    lectures = []

    # Find an empty cell in the matrix to fill
    find = find_empty(matrix)

    if not find:
        return True
    else:
        group, row, col = find 
    #creating a list of possible courses
    for _ in range(len(courses_list)):
        # choose a professor from professors_list
        prof = random.choice(professors_list)
        c = random.choice(courses_list)
        classroom = random.choice(classrooms_list).replace(" ","")
        c_type = random.choice(courses_types)
        lectures.append(Course(course=c,prof=prof,classroom=classroom,type=c_type))
    
    #executing the backtracking algorithm
    for lecture in lectures:
        if valid(lecture,(group,row,col),matrix):
            matrix[group][row][col] = lecture

            if generate_tables(matrix,courses_list,professors_list,classrooms_list):
                return True
        
    matrix[group][row][col] = "-"

    return False

    

def display_matrix(matrix):
    for i in range(len(matrix)):
        print(f"class {i+1}:")
        for j in range(6):
            for k in range(6):
                print(matrix[i][j][k], end=" ")
            print()
        print()