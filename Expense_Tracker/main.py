import tkinter as tk
from tkinter import ttk
from datetime import date # To get current date
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
        self.home()

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

        with open ("Record.txt", 'a') as file: # writing data in file
            file.write(f"{date.today()},{cat},{rsn},{amt}\n")
            ttk.Label(frame, text="Data Added", font="Arial 20").pack(anchor="center")

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


    def home(self):
        frame = ttk.Frame(self.frame) # Bigger body frame
        frame.pack(side="top", fill="x")
        '''Category'''
        # catframe = ttk.Frame(frame, borderwidth=10, relief='solid')
        # catframe.grid(row=0, column=0)
        self.category = tk.Listbox(frame, width=10, height=5, font="Arial 14")
        self.category.insert(1,"Food")
        self.category.insert(2,"Laundary")
        self.category.insert(3,"Stationary")
        self.category.insert(4,"Person")
        self.category.insert(5,"Credit")
        self.category.insert(6,"Other")
        self.category.grid(row=0, column=0)
        
        # def show():
        #     if category.curselection():
        #         ttk.Label(self.frame, text=category.get(category.curselection())).pack()
        # ttk.Button(self.frame, text="Click", command=show).pack()
        
        '''Reason'''
        rsnframe = ttk.Frame(frame)
        rsnframe.grid(row=0,column = 1, padx=100)
        ttk.Label(rsnframe, text="Reason", font="Arial 14").pack()
        reasonV = tk.StringVar() # Stores value from the reason box but the value needs to be called by using ".get()"
        reasonW = ttk.Entry(rsnframe, textvariable=reasonV)
        reasonW.pack()

        '''Amount'''
        amtframe = ttk.Frame(frame)
        amtframe.grid(row =0 , column=2)
        ttk.Label(amtframe, text="Amount", font="Arial 14").pack()
        amountV = tk.StringVar() # Stores value from the amount box but the value needs to be called by using ".get()"
        amountW = ttk.Entry(amtframe, textvariable=amountV)
        amountW.pack()

        '''Add Button'''
        self.aframe = ttk.Frame(self.frame)
        self.aframe.pack(anchor="center")
        tk.Button(frame, text="Add", font="Arial 20", background="white", command=lambda: self.Add(reasonV.get(), amountV.get(), self.aframe)).grid(row=0, column=3, padx=100)
        
        '''View Button'''
        self.vframe = ttk.Frame(self.frame)
        self.vframe.pack(anchor="center")
        tk.Button(frame, text="View", font="Arial 20", background="white", command=lambda: self.View(self.vframe)).grid(row=0, column=4, padx=100)

Session = app()
Session.mainloop()