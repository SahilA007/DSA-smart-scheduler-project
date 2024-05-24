import sqlite3
import itertools
import customtkinter as ctk
from tkinter import ttk

# Database setup
conn = sqlite3.connect('scheduler.db')

# Fetch data from the database
def fetch_data():
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM venues")
    venues = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT slot FROM time_slots")
    time_slots = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT name FROM classes")
    classes = [row[0] for row in cursor.fetchall()]
    
    return venues, time_slots, classes

venues, time_slots, classes = fetch_data()

class Scheduler:
    def __init__(self, venues, time_slots, classes):
        self.venues = venues
        self.time_slots = time_slots
        self.classes = classes
        self.schedule = {}
        self.all_assignments = list(itertools.product(classes, venues, time_slots))
    
    def is_valid(self, class_name, venue, time_slot):
        for (c, v, t) in self.schedule:
            if t == time_slot and v == venue:
                return False
        return True
    
    def backtrack(self, assignment_index=0):
        if assignment_index == len(self.classes):
            return True
        
        class_name = self.classes[assignment_index]
        
        for venue in self.venues:
            for time_slot in self.time_slots:
                if self.is_valid(class_name, venue, time_slot):
                    self.schedule[(class_name, venue, time_slot)] = class_name
                    if self.backtrack(assignment_index + 1):
                        return True
                    del self.schedule[(class_name, venue, time_slot)]
        
        return False
    
    def solve(self):
        if self.backtrack():
            return self.schedule
        else:
            return None

scheduler = Scheduler(venues, time_slots, classes)
solution = scheduler.solve()

class SchedulerGUI:
    def __init__(self, master, solution):
        self.master = master
        self.solution = solution
        self.create_widgets()
    
    def create_widgets(self):
        self.master.title("Class Scheduling")
        self.master.geometry("600x400")
        
        if not self.solution:
            ctk.CTkLabel(self.master, text="No valid schedule found.", font=('Helvetica', 16)).pack(pady=20)
            return
        
        tree = ttk.Treeview(self.master, columns=('Class', 'Venue', 'Time'), show='headings')
        tree.heading('Class', text='Class')
        tree.heading('Venue', text='Venue')
        tree.heading('Time', text='Time')
        
        for (class_name, venue, time_slot) in self.solution:
            tree.insert('', 'end', values=(class_name, venue, time_slot))
        
        tree.pack(fill='both', expand=True)

if __name__ == "__main__":
    root = ctk.CTk()
    
    scheduler = Scheduler(venues, time_slots, classes)
    solution = scheduler.solve()
    
    app = SchedulerGUI(root, solution)
    
    root.mainloop()
