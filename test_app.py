import pytest
from app import *
import darkdetect

instance = App(test=True)

def test_app_properties():
    
    #check window properties
    assert isinstance(instance,App)
    assert instance.title() == ""
    assert instance.resizable()[0] == False
    assert instance.resizable()[0] == False
    
    #check dark mode
    if darkdetect.isDark():
        assert instance._get_appearance_mode() == "dark"
    else:
        assert instance._get_appearance_mode() == "light"

def test_app_data():
    #check data
    assert instance.professors_list
    assert instance.courses_list
    assert instance.classrooms_list

def test_app_widgets():
    #check widgets
    assert isinstance(instance.departement,TextInput)
    assert isinstance(instance.semester,TextInput)
    assert isinstance(instance.start_date,CalendarInput)
    assert isinstance(instance.end_date,CalendarInput)

    assert isinstance(instance.professors,MainContent)
    assert isinstance(instance.courses,MainContent)
    assert isinstance(instance.classrooms,MainContent)
    

def test_check_date_valid_dates():
    assert instance.check_dates("2024/04/29","2024/05/04")[0] == datetime.strptime("2024/04/29","%Y/%m/%d").date()
    assert instance.check_dates("2024/04/29","2024/05/04")[1] == datetime.strptime("2024/05/04","%Y/%m/%d").date()

def test_check_date_invalid_start_date_not_monday():
    with pytest.raises(ValueError):
        instance.check_dates("2024/04/30","2024/05/04")

def test_check_date_invalid_end_date_not_saturday():
    with pytest.raises(ValueError):
        instance.check_dates("2024/04/29","2024/05/03")

def test_check_date_invalid_dates_not_same_week():
    with pytest.raises(ValueError):
        instance.check_dates("2024/04/22","2024/05/04")