import tkinter as tk
from tkinter import ttk
from datetime import date, datetime # To get current date
class app(tk.Tk):
    def ratio_converter(self, iwidth, iheight): # Ration converter for optimum window-size according to screen
        fwidth = int(iwidth * (8/10))
        fheight = int(iheight * (7/10))
        ratio = fwidth/fheight
        return (fwidth, fheight)

    def __init__(self):
        super().__init__()
        screenH = self.winfo_screenheight()
        screenW = self.winfo_screenwidth()
        # print(self.ratio_converter(screenW, screenH), screenW/screenH)
        (winW, winH) = self.ratio_converter(screenW, screenH)
        self.geometry(f"{winW}x{winH}")
        self.frame = tk.Frame(self)
        self.frame.pack(fill="both")
        self.home(self.frame)
        self.menu()

    def Add(self,rsn, amt, frame): 
        for widget in frame.winfo_children(): # Refresh the Data Added or Invalid entry line
            widget.destroy()
        selection = self.category.curselection() #This gets the index of selected item in category when the add button is pressed
        if selection == (): 
            ttk.Label(frame, text="No Category Selected", font="Arial 20").pack(anchor="center")
            return None
        else: 
            cat = self.category.get(selection) # this gets the selected item value from the index

        if amt.strip() == "" :  
            ttk.Label(frame, text="No Amount entered", font="Arial 20").pack(anchor="center") #If no amount entered
            return None
        if rsn.strip() == "" :  
            ttk.Label(frame, text="No Reason entered", font="Arial 20").pack(anchor="center") #If no reason entered
            return None
        '''Checking if the amount entered is valid'''
        if not amt.isdigit():
            try: 
                amt = float(amt)
                
                print(date.today(), cat,rsn,amt)
            except: 
                ttk.Label(frame, text="Invalid Amount Entered", font="Arial 20").pack(anchor="center")
                return None
        if int(amt) < 0: 
            ttk.Label(frame, text="Invalid Amount Entered", font="Arial 20").pack(anchor="center") #If amount entered is negavtive number
            return None

        # with open ("Record.txt", 'r+') as file: # writing data in file
        #     data = file.read() #To memorise data from file
        #     file.seek(0) #set cursor to 0
        #     file.truncate() #delete all data from the cursor to end of file
        #     file.write(f"{date.today()},{cat},{rsn},{amt}\n{data}") # Write as added data then memorised data
        self.order(f"{date.today()},{cat},{rsn},{amt}\n") # Add Month and Year to sort between records
        ttk.Label(frame, text="Data Added", font="Arial 20").pack(anchor="center")

        '''Storing Budget and making it change with the expense'''
        with open("budget.txt", 'r') as file:
            budget = file.read()
        if cat != "Credit": 
            with open("budget.txt", 'w') as file:
                # file.write(str(float(budget) - float(amt)))
                self.budget = tk.StringVar(value=str(float(budget) - float(amt)))
            self.Budget()
        else: 
            with open("budget.txt", 'w') as file:
                # file.write(str(float(budget) + float(amt)))
                self.budget = tk.StringVar(value=str(float(budget) + float(amt)))
            self.Budget()

    def View(self, frame):
        for widget in frame.winfo_children(): # Refresh the Text widget
            widget.destroy()
        with open("Record.txt", 'r') as file: # Create Text widget to show the records
            # Scrollbar on text widget
            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side="right", fill="y")

            show = tk.Text(frame, font="Arial 16")
            show.insert("1.0", file.read())
            show.pack(anchor="center", expand=True, fill="y")
            show['yscrollcommand'] = scrollbar.set

    def Budget(self):
        frame = self.bframe
        for widget in frame.winfo_children(): # Refresh the widgets used in Budget
            widget.destroy()
        ttk.Label(frame, text=f"Budget : {self.budget.get()}", font="Arial 18").grid(row=0, column=2)
        ttk.Entry(frame, textvariable=self.budget, font="Arial 18", width=10).grid(row=0, column=3, padx="30")
        tk.Button(frame, text="Set", font="Arial 18", command=lambda: self.Budget(frame)).grid(row=0, column=4)
        with open ("budget.txt", 'w') as file:
            file.write(self.budget.get())

    def home(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        frame = ttk.Frame(frame) # This creates a frame inside self.frame
        frame.pack(fill="x")

        '''Budget'''
        self.bframe = ttk.Frame(frame)
        self.bframe.grid(row=0, column=2)
        with open("budget.txt", 'r') as file:
            self.budget = tk.StringVar(value=file.read())
        ttk.Label(self.bframe, text=f"Budget : {self.budget.get()}", font="Arial 18").grid(row=0, column=2)
        ttk.Entry(self.bframe, textvariable=self.budget, font="Arial 18", width=10).grid(row=0, column=3, padx="30")
        tk.Button(self.bframe, text="Set", font="Arial 18", command=lambda: self.Budget()).grid(row=0, column=4)
        
        '''Category'''
        self.category = tk.Listbox(frame, width=10, height=5, font="Arial 14")
        self.category.insert(1,"Food")
        self.category.insert(2,"Laundary")
        self.category.insert(3,"Stationary")
        self.category.insert(4,"Person")
        self.category.insert(5,"Credit")
        self.category.insert(6,"Other")
        self.category.grid(row=1, column=0)
        
        
        '''Reason'''
        rsnframe = ttk.Frame(frame)
        rsnframe.grid(row=1,column = 1, padx=100)
        ttk.Label(rsnframe, text="Reason", font="Arial 18").pack()
        reasonV = tk.StringVar() # Stores value from the reason box but the value needs to be called by using ".get()"
        reasonW = ttk.Entry(rsnframe, textvariable=reasonV, font="Arial 18", width=13)
        reasonW.pack()

        '''Amount'''
        amtframe = ttk.Frame(frame)
        amtframe.grid(row =1, column=2)
        ttk.Label(amtframe, text="Amount", font="Arial 18").pack()
        amountV = tk.StringVar() # Stores value from the amount box but the value needs to be called by using ".get()"
        amountW = ttk.Entry(amtframe, textvariable=amountV, font = "Arial 18", width=8)
        amountW.pack()

        '''Add Button'''
        self.aframe = ttk.Frame(self.frame)
        self.aframe.pack(anchor="center")
        tk.Button(frame, text="Add", font="Arial 20", background="white", command=lambda: self.Add(reasonV.get(), amountV.get(), self.aframe)).grid(row=1, column=3, padx=100)
        
        '''View Button'''
        self.vframe = ttk.Frame(self.frame)
        self.vframe.pack(anchor="center")
        tk.Button(frame, text="View", font="Arial 20", background="white", command=lambda: self.View(self.vframe)).grid(row=1, column=4, padx=100)

    def menu(self): 
        '''Menubar'''
        menubar = tk.Menu(font="Arial 15 bold") # Menubar created, Font size determine the menubar size
        self.config(menu=menubar) # Menubar added in root window
        menubar.add_separator() # Adds a horizontal line in bottom separating menubar from the rest
        menubar.add_command(label="Home", command=lambda: self.home(self.frame)) # Home Option
        menubar.add_command(label="Analytics", command=lambda: self.analytics(self.frame)) # Home Option
    
    def analytics(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
        from matplotlib import pyplot as plt
        import numpy as np
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        with open("Record.txt", 'r') as file:
            tasks = file.readlines()
        record = {}
        for task in tasks:
            try:
                if task.split(',')[1] not in record:
                    # category.append(task.split(',')[1])
                    # amount.append(int(task.split(',')[3][:-1]))
                    record[task.split(',')[1]] = int(task.split(',')[3][:-1]) # Adds the new category with its amount in dictionary
                else:
                    record[task.split(',')[1]] = int(record[task.split(',')[1]]) + int(task.split(',')[3][:-1]) # Adds the last amount to new amount in integer form
            except: continue
        print(record.keys(), record.values())
        
        fig = Figure(figsize=(10,10))
        ax = fig.add_subplot(111)
        ax.pie(record.values(), radius = 1, labels=record.keys(), autopct="%0.2f%%")
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def order(self, line): # Add Month and Year to sort between records
        month_year = ""
        with open("Record.txt", 'r+') as file:
            # last_date = file.readline().split(',')[0]
            # last_date = last_date.split('-')[0:2]
            cur_date = datetime.now().strftime('%B %Y') # Get current month and year
            file.readline()
            data = file.read() # get file data
            file.seek(0) # set cursor to start
            file.truncate() # delete file content
            
            if month_year != cur_date: # If the month and year of latest updated record is different than already stored than it adds new month and year
                month_year = cur_date+"\n"

            file.write(month_year+line+data) # Write the new data with month and year

Session = app()
Session.mainloop()