class SchedulerGUI:
    def __init__(self, master, solution):
        self.master = master
        self.solution = solution
        self.create_widgets()
    
    def create_widgets(self):
        self.master.title("Class Scheduling")
        
        if not self.solution:
            Label(self.master, text="No valid schedule found.", font=('Helvetica', 16)).pack(pady=20)
            return
        
        tree = ttk.Treeview(self.master, columns=('Class', 'Venue', 'Time'), show='headings')
        tree.heading('Class', text='Class')
        tree.heading('Venue', text='Venue')
        tree.heading('Time', text='Time')
        
        for (class_name, venue, time_slot) in self.solution:
            tree.insert('', 'end', values=(class_name, venue, time_slot))
        
        tree.pack(fill='both', expand=True)

if __name__ == "__main__":
    root = Tk()
    
    scheduler = Scheduler(venues, time_slots, classes)
    solution = scheduler.solve()
    
    app = SchedulerGUI(root, solution)
    
    root.mainloop()
