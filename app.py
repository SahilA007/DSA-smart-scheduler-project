from settings import *
from db_setup import *
from logic import *
from table import generate_tables_template, fill_tables
import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry
from datetime import datetime
import calendar

import darkdetect #used to check if the system is using dark mode or not


class App(ctk.CTk):
    def __init__(self,is_dark = False, test=False):
        super().__init__(fg_color=(WHITE,BLACK))
        ctk.set_appearance_mode("dark" if is_dark else "light")
        ctk.set_default_color_theme("green")
        self.geometry("1200x600")
        self.resizable(False,False)
        self.title("")
        self.iconbitmap("images/blank.ico")

        #layout
        self.columnconfigure((0,1,2,3),weight=2,uniform="a")
        self.rowconfigure((0,1,2,3,4,5),weight=1,uniform="b")

        #database setup
        check_database()

        #data
        self.professors_list = get_professors()
        self.courses_list = get_courses()
        self.classrooms_list = get_classrooms() 

        #widgets
        self.create_widgets()

        #event
        self.bind("<Escape>", lambda event: self.quit())
        #test_mode
        if test:
            self.after(1000,self.quit)
        #run
        self.mainloop()
    
    def create_widgets(self):
        self.departement = TextInput(self,"Departement",row=0,col=0)
        self.semester = TextInput(self,"Semester",row=0,col=1)
        self.start_date = CalendarInput(self,"Start date",row=0,col=2)
        self.end_date = CalendarInput(self,"End date",row=0,col=3)

        self.professors = MainContent(self,"Professors",row=1,col=0,data=self.professors_list,del_func=delete_professor,add_func=add_professor)
        #print(self.professors.get_selected_values())
        self.courses = MainContent(self,"Courses",row=1,col=1,data=self.courses_list,del_func=delete_course,add_func=add_course)
        #print(self.courses.get_selected_values())
        self.classrooms = MainContent(self,"Classrooms",row=1,col=2,data=self.classrooms_list,del_func=delete_classroom,add_func=add_classroom)
        #print(self.classrooms.get_selected_values())
        
        self.create_generate_frame(row=1,col=3)

    def create_generate_frame(self,row,col):

        #frame
        generate_frame = ctk.CTkFrame(master=self)
        
        #frame layout setup
        generate_frame.columnconfigure(0,weight=1)
        generate_frame.rowconfigure(0,weight=1)
        generate_frame.rowconfigure(1,weight=1)

        #widgets
        self.nbr_classes = NbrClassesInput(generate_frame,"Number of classes",row=0,col=0,fg_color="transparent")
        generate_button = ctk.CTkButton(generate_frame,text="Generate",command=self.generate_timetables)
        
        #layout
        generate_frame.grid(row=row, rowspan=5, column=col,sticky="nsew",padx=10)
        self.nbr_classes.grid(row=0,column=0,pady=10,padx=10)
        generate_button.grid(row=1,column=0,sticky="nsew",pady=10,padx=10)

    def generate_timetables(self):
        try:
            departement_data = self.departement.get_content() #str
            semester_data = self.semester.get_content() #str
            start_date,end_date = self.check_dates(self.start_date.get_content(),self.end_date.get_content()) #datetime.date
            selected_professors = self.professors.get_selected_values() #str list
            selected_courses = self.courses.get_selected_values() #str list
            selected_classrooms = self.classrooms.get_selected_values() #str list
            nbr_classes_data = self.nbr_classes.get_content() #int

            #create the matrix for our tables
            matrix = create_timetable_matrix(nbr_classes_data)
            generate_tables(matrix,selected_courses,selected_professors,selected_classrooms)
            template = generate_tables_template("Timetable.docx",nbr_classes_data,departement_data)
            fill_tables(matrix,template,departement_data,semester_data,start_date,end_date)
            CTkMessagebox(title="Info",message=f"Timetables generated successfully and stored at {template}",sound=True)

            #empty input fields
            self.departement.input.delete(0,"end")
            self.semester.input.delete(0,"end")
            self.nbr_classes.input.delete(0,"end")

        except ValueError as e:
            CTkMessagebox(title="Warning",message=e,icon="warning",sound=True)

    def check_dates(self,start_date_str,end_date_str):
        start_date = datetime.strptime(start_date_str,"%Y/%m/%d").date()
        end_date = datetime.strptime(end_date_str,"%Y/%m/%d").date()
        if start_date.isocalendar()[1] == end_date.isocalendar()[1]:
            if start_date.isocalendar()[1] == datetime.today().isocalendar()[1] + 1:
                if calendar.day_name[start_date.weekday()] == "Monday":
                    if calendar.day_name[end_date.weekday()] == "Friday":
                        return (start_date,end_date)
                    else:
                        raise ValueError("End date must be a Saturday")    
                else:
                    raise ValueError("Start date must be a Monday")
            else:
                raise ValueError("The start date and end date should belong to the following week")
        else:
            raise ValueError("Start date and end date must be of the same week")
    

class TextInput(ctk.CTkFrame):
    def __init__(self,parent,title,row,col,fg_color=None):
        super().__init__(master=parent,fg_color=fg_color)

        #layout
        self.columnconfigure(0,weight=1)
        self.rowconfigure((0,1),weight=1,uniform="a")

        
        #data
        self.input_var = tk.StringVar()
        self.title = title
        #widgets
        self.create_widgets()

        #layout
        self.grid(row=row, column=col,sticky="nsew",padx=10,pady=10)

    def create_widgets(self):
        #font
        font = ctk.CTkFont(family=FONT_STATUS,size=NORMAL_FONT_SIZE,weight="bold")
        label_title = ctk.CTkLabel(self,text=self.title,font=font)
        self.input = ctk.CTkEntry(self,placeholder_text="Department name",corner_radius=2,border_width=1,textvariable=self.input_var)

        #layout
        label_title.grid(row = 0 ,column = 0,sticky="nsew")
        self.input.grid(row = 1,column = 0,sticky="nsew")

    def get_content(self):
        if self.input_var.get():
            return self.input_var.get()
        else: 
            raise ValueError(f"{self.title} field cannot be empty")


class NbrClassesInput(TextInput):
    def __init__(self,parent,title,row,col,fg_color=None):
        super().__init__(parent=parent,title=title,row=row,col=col,fg_color=fg_color)
    
    
    def get_content(self):
        if self.input_var.get():
            if self.input_var.get().isnumeric():
                if int(self.input_var.get()) > 0:
                    return int(self.input_var.get())
                else:
                    raise ValueError("Number of classes value must be greater than zero")

            else:
                raise ValueError("Number of classes value must be an integer") 
        else:
            raise ValueError(f"{self.title} field cannot be empty")

class CalendarInput(ctk.CTkFrame):
    def __init__(self,parent,title,row,col):
        super().__init__(master=parent)

        #layout
        self.columnconfigure(0,weight=2)
        self.rowconfigure((0,1),weight=2,uniform="a")

        #data
        self.input_var = tk.StringVar(value=0)

        #widgets        
        self.create_widgets(title=title)

         #layout
        self.grid(row=row, column=col,sticky="nsew",padx=10,pady=10)

    def create_widgets(self,title):
        #font
        font = ctk.CTkFont(family=FONT_STATUS,size=NORMAL_FONT_SIZE,weight="bold")
        
        #widgets
        label_title = ctk.CTkLabel(self,text=title,font=font) 
        calendar = DateEntry(self,firstweekday = "monday",weekenddays = [6,7],date_pattern = "y/mm/dd",textvariable=self.input_var,background="#343638")

        #layout
        label_title.grid(row = 0 ,column = 0,sticky="nsew")
        calendar.grid(row = 1, column = 0,sticky="nsew")

    def get_content(self):
        return self.input_var.get()
    
class MainContent(ctk.CTkFrame):
    def __init__(self,parent,title,row,col,data,del_func,add_func):
        super().__init__(master=parent)
        
        #layout
        self.columnconfigure(0,weight=2)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=5)
        self.rowconfigure(2,weight=1)

        #widgets
        self.create_widgets(title,data,del_func,add_func)

        self.grid(row=row, rowspan=5, column=col, sticky="nsew", padx= 10)

    def create_widgets(self,title,data,del_func,add_func):
        #font
        font = ctk.CTkFont(family=FONT_STATUS,size=NORMAL_FONT_SIZE,weight="bold")
        font2 = ctk.CTkFont(family=FONT_STATUS,size=SELECT_ALL_BUTTON_FONT_SIZE,weight="normal")
        
        #data
        self.title = title
        self.select_all = True

        #widgets
        title_frame = ctk.CTkFrame(master=self,fg_color="transparent")
        label_title = ctk.CTkLabel(master=title_frame,text=title,font=font)
        select_all_button = ctk.CTkButton(master=title_frame,text="Select All",corner_radius=0,font=font2,width=90,command=self.select_deselect_all)

        #main_data frame
        self.data_frame = ctk.CTkScrollableFrame(self,corner_radius=0)
        self.load_data(self.data_frame,data,del_func)

        add_frame = AddDataFrame(self,row=2,col=0,del_func=del_func,add_func=add_func,data_frame=self.data_frame)

        #layout
        title_frame.grid(row = 0 ,column = 0,sticky = "nsew")
        label_title.pack(expand=True,fill="both",side="left")
        select_all_button.pack(fill="y",side="left")
        
        self.data_frame.grid(row=1,column=0,sticky = "nsew")
        
    def load_data(self,data_frame,data,del_func):
        for i in data:
            DataLineFrame(data_frame,val=i,del_func=del_func).pack(expand=True,fill="both")    

    def get_selected_values(self):
        selected_values = []
        for line_frame in self.data_frame.winfo_children():
            val = line_frame.val_status()
            if val[1] == 1:
                selected_values.append(val[0])
        if len(selected_values)>=3:
            return selected_values
        else:
            raise ValueError(f"You need to select at least 3 {self.title.lower()}")

    def select_deselect_all(self):
        if self.select_all:
            for line_frame in self.data_frame.winfo_children():
                line_frame.deselect_val()
            self.select_all = False
        else:
            for line_frame in self.data_frame.winfo_children():
                line_frame.select_val()
            self.select_all = True
        self.update_idletasks()


class DataLineFrame(ctk.CTkFrame):
    def __init__(self,parent,val,del_func):
        super().__init__(master=parent,fg_color="transparent")
        
        self.value = val 
        self.create_widgets(self.value,del_func)

        self.pack(expand=True, fill="x",padx=5,pady=5)
    
    def create_widgets(self,val,del_func):
        #widgets
        self.value_box = ctk.CTkCheckBox(self,text=val)
        self.value_box.select()
        self.delete = ctk.CTkButton(self,text="X",width=20,height=20,fg_color="#E81123",hover_color="#E81123",command=lambda: self.delete_line(del_func,val=val))

        #layout
        self.value_box.pack(expand=True,fill="both",side="left")
        self.delete.pack(side="left")

    def val_status(self):
        return (self.value,self.value_box.get())

    def select_val(self):
        self.value_box.select()
    
    def deselect_val(self):
        self.value_box.deselect()

    def delete_line(self,func,val):
        func(val)
        self.pack_forget()

class AddDataFrame(ctk.CTkFrame):
    def __init__(self,parent,row,col,add_func,del_func,data_frame): 
        super().__init__(master=parent,fg_color="transparent")

        #data
        self.input_var = tk.StringVar()

        self.create_widgets(add_func,del_func,data_frame)

        self.grid(row=row, column=col, sticky="nsew",padx=10,pady=10)

    def create_widgets(self,add_func,del_func,data_frame):
        self.add_input = ctk.CTkEntry(self,corner_radius=2,border_width=1,textvariable=self.input_var)
        self.add_button = ctk.CTkButton(self,corner_radius=0,text="Add",width=20,height=20,command=lambda: self.add_data(add_func,del_func,data_frame)) #,command=lambda: self.delete_line(del_func,val=val)
        self.add_input.pack(expand=True,fill="both",side="left")
        self.add_button.pack(side="left",fill="y")
    
    def add_data(self,add_func,del_func,data_frame):
        try:
            add_func(self.input_var.get())
            DataLineFrame(data_frame,self.input_var.get(),del_func)
            self.add_input.delete(0,"end")
            data_frame.update_idletasks()
        except ValueError as e:
            CTkMessagebox(title="Warning",message=e,icon="warning",sound=True)


def main():
    App(darkdetect.isDark())

if __name__ =="__main__":
    main()