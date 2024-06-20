import pytest 
from course import Course

#testing the course class

#testing the course property
def test_course_property():
    c = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    assert c.course == "testcourse"

def test_course_empty_value():
    with pytest.raises(ValueError):
        Course(course="",prof="prof",classroom="c1",type="C")

def test_course_whitespace_value():
    with pytest.raises(ValueError):
        Course(course=" ",prof="prof",classroom="c1",type="C")

#testing the prof property    
def test_prof_property():
    c = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    assert c.prof == "prof"

def test_prof_empty_value():
    with pytest.raises(ValueError):
        Course(course="testcourse",prof="",classroom="c1",type="C")

def test_prof_whitespace_value():
    with pytest.raises(ValueError):
        Course(course="testcourse",prof=" ",classroom="c1",type="C")

#testing the classroom property
def test_classroom_property():
    c = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    assert c.classroom == "c1"

def test_classroom_empty_value():
    with pytest.raises(ValueError):
        Course(course="testcourse",prof="prof",classroom="",type="C")

def test_classroom_whitespace_value():
    with pytest.raises(ValueError):
        Course(course="testcourse",prof="prof",classroom=" ",type="C")

#testing the course type property
def test_course_type_property():
    c = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    assert c.type == "C"

def test_course_type_empty_value():
    with pytest.raises(ValueError):
        Course(course="testcourse",prof="prof",classroom="c1",type="")

def test_course_type_whitespace_value():
    with pytest.raises(ValueError):
        Course(course="testcourse",prof="prof",classroom="c1",type=" ")

def test_course_type_invalid_value():
    with pytest.raises(ValueError):
        Course(course="testcourse",prof="prof",classroom="c1",type="S")

#testing the color property
def test_color_value():
    c = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    assert c.color == "FB6266"
    c.type = "TD"
    c.set_color()  
    assert c.color == "80FF80"
    c.type = "CI"
    c.set_color()
    assert c.color == "868686"

def test__eq__():
    c1 = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    c2 = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    assert c1.__eq__(c2) == True

def test__eq__diffrent_course_objects():
    c1 = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    c2 = Course(course="testcourse2",prof="prof2",classroom="c2",type="C")
    assert c1.__eq__(c2) == False

def test__eq__diffrent_objects():
    c1 = Course(course="testcourse",prof="prof",classroom="c1",type="C")
    c2 = 1
    assert c1.__eq__(c2) == False

def test__str__():
    course_name = "testcourse"
    professor = "test prof"
    classroom = "c3"
    course_type = "TD"
    c1 = Course(course=course_name,prof=professor,classroom=classroom,type=course_type)
    assert c1.__str__() == f"course: {course_name} professor: {professor} classroom: {classroom} course type: {course_type}"