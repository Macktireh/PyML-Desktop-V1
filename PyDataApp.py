import os
import sqlite3
import tkinter as tk
import tempfile
from tkinter.constants import RADIOBUTTON, RAISED


class PyData:
    def __init__(self):
        root = tk.Tk()
        self.root = root
        self.root.title("PyData Desktop")
        self.root.geometry("1400x800+5+5")
        self.root.iconbitmap('logo.ico')

        super().__init__()
        self.initUI()

    def onExit(self):
        self.root.quit()

    def initUI(self):

        menubar = tk.Menu(self.root, background='#856ff8', fg='white')
        self.root.config(menu=menubar)

        # instancier les menu
        fileMenu = tk.Menu(menubar, tearoff=0, bg='lightgray')
        HomeMenu = tk.Menu(menubar, tearoff=0, bg='lightgray')
        ToolsMenu = tk.Menu(menubar, tearoff=0, bg='lightgray')
        HelpMenu = tk.Menu(menubar, tearoff=0, bg='lightgray')

        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Home", menu=HomeMenu)
        menubar.add_cascade(label="Tools", menu=ToolsMenu)
        menubar.add_cascade(label="Help", menu=HelpMenu)

        fileMenu.add_command(label="New")
        fileMenu.add_command(label="Import")
        fileMenu.add_command(label="Export")
        fileMenu.add_command(label="Settings")
        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=self.onExit)

        HomeMenu.add_command(label="View Data")
        HomeMenu.add_command(label="Data Transform")
        HomeMenu.add_command(label="Data Viz")

        # sous menu Machine learning
        menu_sub_ml = tk.Menu(HomeMenu, tearoff=0)
        HomeMenu.add_cascade(label="Machine Learning", menu=menu_sub_ml)
        # sous model
        menu_sub_model = tk.Menu(menu_sub_ml, tearoff=0)
        menu_sub_ml.add_cascade(label='Regressor', menu=menu_sub_model)
        menu_sub_model.add_command(label="LinearRegressor")
        menu_sub_model.add_command(label="RandomForestRegressor")
        menu_sub_model.add_command(label="KNeighborsRegressor")
        menu_sub_model.add_command(label="DecisionTreeRegressor")

        # sous model
        menu_sub_model = tk.Menu(menu_sub_ml, tearoff=0)
        menu_sub_ml.add_cascade(label='Classifier', menu=menu_sub_model)
        menu_sub_model.add_command(label="LogisticRegression")
        menu_sub_model.add_command(label="RandomForestClassifier")
        menu_sub_model.add_command(label="KNeighborsClassifier")
        menu_sub_model.add_command(label="DecisionTreeClassifier")
        menu_sub_model.add_command(label="SVM")

        # self.root.config(menu=mainMenu)

        # title = tk.Label(self.root, text="Gestion de Paie de Professeurs", bd=20,
        #                  relief=RAISED, font=('Algerian', 45), bg='cyan', fg='black')
        # title.pack(side='top', fill='x')


app = PyData()
app.root.mainloop()
