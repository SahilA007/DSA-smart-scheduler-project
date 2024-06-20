import pytest
from db_setup import *

def test_add_course_valid_name():
    assert add_course("Introduction to Python and Programming Concepts") == True

def test_add_course_existing_value():
    with pytest.raises(ValueError):
        add_course("Introduction to Python and Programming Concepts") 

def test_add_course_empty_string():
    with pytest.raises(ValueError):
        add_course("") 

def test_add_course_whitesapce_string():
    with pytest.raises(ValueError):
        add_course(" ")

def test_delete_course_existant_course():
    assert delete_course("Introduction to Python and Programming Concepts") == True

def test_delete_course_non_existant_course():
    with pytest.raises(ValueError):
        delete_course("test")

def test_delete_course_empty_string():
    with pytest.raises(ValueError):
        delete_course("")

def test_delete_course_whitespace_string():
    with pytest.raises(ValueError):
        delete_course("  ")


def test_add_professor_valid_name():
    assert add_professor("Dr. Jack Smith") == True

def test_add_professor_existing_value():
    with pytest.raises(ValueError):
        add_professor("Dr. Jack Smith")

def test_add_professor_empty_string():
    with pytest.raises(ValueError):
        add_professor("") 

def test_add_professor_whitesapce_string():
    with pytest.raises(ValueError):
        add_professor(" ")

def test_delete_professor_existant_professor():
    assert delete_professor("Dr. Jack Smith") == True

def test_delete_professor_non_existant_professor():
    with pytest.raises(ValueError):
        delete_professor("Dr. test test") 

def test_delete_professor_empty_string():
    with pytest.raises(ValueError):
        delete_professor("")

def test_delete_professor_whitespace_string():
    with pytest.raises(ValueError):
        delete_professor("  ")



def test_add_classroom_valid_name():
    assert add_classroom("c 62") == True

def test_add_classroom_existing_value():
    with pytest.raises(ValueError):
        add_classroom("c 62")

def test_add_classroom_empty_string():
    with pytest.raises(ValueError):
        add_classroom("") 

def test_add_classroom_whitesapce_string():
    with pytest.raises(ValueError):
        add_classroom(" ")

def test_delete_classroom_existant_classroom():
    assert delete_classroom("c 62") == True

def test_delete_classroom_non_existant_professor():
    with pytest.raises(ValueError):
        delete_classroom("c 62") 

def test_delete_classroom_empty_string():
    with pytest.raises(ValueError):
        delete_classroom("")

def test_delete_classroom_whitespace_string():
    with pytest.raises(ValueError):
        delete_classroom("  ")