import os
import sqlite3
import tkinter as tk
import tempfile
import pandas as pd
import numpy as np
from tkinter import font
from tkinter.constants import RADIOBUTTON, RAISED
from tkinter import PhotoImage
from PIL import Image, ImageTk
# from tkinter_custom_button import TkinterCustomButton
from tkinter import filedialog, messagebox, ttk
from tkinter.constants import ACTIVE
from datetime import date, datetime
from openpyxl import load_workbook
from main import Api


class PyData:

    # color = {}

    def __init__(self):
        root = tk.Tk()
        self.root = root
        self.root.title("PyData Desktop")
        self.root.geometry("1400x800+5+5")
        self.root.iconbitmap('media/logo.ico')
        self.root.config(background="#FAEBD7")

        super().__init__()
        self.initUI()
        self.WedgetHome()
        self.widgetGetData()
        self.ViewData()

    def onExit(self):
        self.root.quit()

    def Load_Path_Excel(self):
        """
        Cette fonction ouvrira l'explorateur de fichiers et 
        affectera le chemin de fichier choisi à label_file
        """
        path_filename = filedialog.askopenfilename(initialdir="E:\Total\Station Data\Master data\Data source",
                                                   title="Select A File",
                                                   filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))
    # if self.path_filename[-4:] == ".csv":
    # self.import_path_csv = self.path_filename
        self.test['text'] = path_filename

    def initUI(self):

        self.menubar = tk.Menu(self.root, background='#856ff8', fg='white')
        self.root.config(menu=self.menubar)

        # instancier les menu
        self.fileMenu = tk.Menu(self.menubar, tearoff=0, bg='lightgray')
        self.HomeMenu = tk.Menu(self.menubar, tearoff=0, bg='lightgray')
        self.ToolsMenu = tk.Menu(self.menubar, tearoff=0, bg='lightgray')
        self.HelpMenu = tk.Menu(self.menubar, tearoff=0, bg='lightgray')

        self.menubar.add_cascade(label="File", menu=self.fileMenu)
        self.menubar.add_cascade(label="Home", menu=self.HomeMenu)
        self.menubar.add_cascade(label="Tools", menu=self.ToolsMenu)
        self.menubar.add_cascade(label="Help", menu=self.HelpMenu)

        self.fileMenu.add_command(label="New")
        self.fileMenu.add_command(label="Import")
        self.fileMenu.add_command(label="Export")
        self.fileMenu.add_command(label="Settings")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Quit", command=self.onExit)

        self.HomeMenu.add_command(label="View Data")
        self.HomeMenu.add_command(label="Data Transform")
        self.HomeMenu.add_command(label="Data Viz")

        # sous menu Machine learning
        self.menu_sub_ml = tk.Menu(self.HomeMenu, tearoff=0)
        self.HomeMenu.add_cascade(
            label="Machine Learning", menu=self.menu_sub_ml)
        # sous model
        self.menu_sub_model = tk.Menu(self.menu_sub_ml, tearoff=0)
        self.menu_sub_ml.add_cascade(
            label='Regressor', menu=self.menu_sub_model)
        self.menu_sub_model.add_command(label="LinearRegressor")
        self.menu_sub_model.add_command(label="RandomForestRegressor")
        self.menu_sub_model.add_command(label="KNeighborsRegressor")
        self.menu_sub_model.add_command(label="DecisionTreeRegressor")

        # sous model
        self.menu_sub_model = tk.Menu(self.menu_sub_ml, tearoff=0)
        self.menu_sub_ml.add_cascade(
            label='Classifier', menu=self.menu_sub_model)
        self.menu_sub_model.add_command(label="LogisticRegression")
        self.menu_sub_model.add_command(label="RandomForestClassifier")
        self.menu_sub_model.add_command(label="KNeighborsClassifier")
        self.menu_sub_model.add_command(label="DecisionTreeClassifier")
        self.menu_sub_model.add_command(label="SVM")

        # Barre entet
        self.barheader = tk.Frame(self.root, bd=20, bg='#FFA500', height=60)
        self.barheader.pack(side='top', fill='x')
        # titre
        self.maintitle = tk.Label(
            self.barheader, text='Welcome to Power Studio Data Desktop !', font=('Algeria 20'), bg='#FFA500')
        self.maintitle.pack(side='bottom', fill='x')

        # WidgetFrame = tk.Frame(self.root, bg='white').place(
        #     relx=0.05, rely=0.1)

    def widgetGetData(self):

        self.FrameGetData = tk.LabelFrame(
            self.root, text="Get Data", background="#FAEBD7").place(
            relx=0.035, rely=0.12, relheight=0.4, relwidth=0.4)

        self.title = tk.Label(
            self.FrameGetData, text="Once loaded, your data will be displayed below", background="#FAEBD7", height=3, font=('Algeria', 12)).place(
            relx=0.09, rely=0.165)

        # charger les icones images
        self.excelIcon = PhotoImage(file="media/excel.png")
        self.excelIcon = self.excelIcon.subsample(10, 10)

        self.csvIcon = PhotoImage(file="media/csv.png")
        self.csvIcon = self.csvIcon.subsample(10, 10)

        self.txtIcon = PhotoImage(file="media/txt.png")
        self.txtIcon = self.txtIcon.subsample(20, 20)

        self.postgreIcon = PhotoImage(file="media/postgresql.png")
        self.postgreIcon = self.postgreIcon.subsample(50, 50)

        self.mysqlIcon = PhotoImage(file="media/mysql.png")
        self.mysqlIcon = self.mysqlIcon.subsample(33, 33)

        self.mongodbIcon = PhotoImage(file="media/mongodb.png")
        self.mongodbIcon = self.mongodbIcon.subsample(13, 13)

        # cadre de boutons
        # self.FrameBtnImport_1 = tk.Frame(
        # self.FrameGetData).place(relx=0.1, rely=0.2)

        # Button import avec icon
        self.excelBtn = tk.Button(self.FrameGetData, image=self.excelIcon, text="Import data from Excel", compound='top',
                                  height=70, width=160, bd=1, bg="#DCDCDC", command=self.Load_Path_Excel).place(relx=0.049, rely=0.25)

        self.csvBtn = tk.Button(self.FrameGetData, image=self.csvIcon, text="Import data from CSV", compound='top',
                                height=70, width=160, bd=1, bg="#DCDCDC", command=self.test).place(relx=0.174, rely=0.25)

        self.txtbtn = tk.Button(self.FrameGetData, image=self.txtIcon, text="Import data from TXT", compound='top',
                                height=70, width=160, bd=1, bg="#DCDCDC", command=None).place(relx=0.299, rely=0.25)

        self.postgrebtn = tk.Button(self.FrameGetData, image=self.postgreIcon, text="Import data from PostgreSQL", compound='top',
                                    height=70, width=160, bd=1, bg="#DCDCDC", command=None).place(relx=0.049, rely=0.37)

        self.mysqlbtn = tk.Button(self.FrameGetData, image=self.mysqlIcon, text="Import data from MySQL", compound='top',
                                  height=70, width=160, bd=1, bg="#DCDCDC", command=None).place(relx=0.174, rely=0.37)

        self.mongobtn = tk.Button(self.FrameGetData, image=self.mongodbIcon, text="Import data from MongoDB", compound='top',
                                  height=70, width=160, bd=1, bg="#DCDCDC", command=None).place(relx=0.299, rely=0.37)

    def WedgetHome(self):

        self.FrameHomeTransData = tk.LabelFrame(
            self.root, text="Data Processing", background="#FAEBD7").place(
            relx=0.45, rely=0.12, relheight=0.4, relwidth=0.505)

        self.LabelCol = tk.Label(
            self.FrameHomeTransData, background="#FAEBD7", text="Columns :").place(relx=0.47, rely=0.15)

        self.RenameCol = tk.Label(
            self.FrameHomeTransData, background="#FAEBD7", text="Rename column").place(relx=0.63, rely=0.22)

        self.RomeveCol = tk.Label(
            self.FrameHomeTransData, background="#FAEBD7", text="Remove column").place(relx=0.63, rely=0.27)

        self.AddCol = tk.Label(
            self.FrameHomeTransData, background="#FAEBD7", text="Add column").place(relx=0.63, rely=0.32)

        self.Lbox = tk.Listbox(self.FrameHomeTransData, bg="#DCDCDC")
        self.Lbox.place(
            relx=0.46, rely=0.18, relheight=0.33, relwidth=0.15)

        self.treescrolly = tk.Scrollbar(
            self.Lbox, orient="vertical")
        self.treescrolly.configure(command=self.Lbox.yview)

        self.treescrollx = tk.Scrollbar(
            self.Lbox, orient="horizontal", command=self.Lbox.xview)

        self.Lbox.configure(xscrollcommand=self.treescrollx.set,
                            yscrollcommand=self.treescrolly.set)

        self.treescrollx.pack(side="bottom", fill="x")
        self.treescrolly.pack(side="right", fill="y")

        self.transformIcon = PhotoImage(file="media/transform.png")
        self.transformIcon = self.transformIcon.subsample(30, 30)

        self.refreshIcon = PhotoImage(file="media/refresh.png")
        self.refreshIcon = self.refreshIcon.subsample(25, 25)

        self.exportIcon = PhotoImage(file="media/export.png")
        self.exportIcon = self.exportIcon.subsample(25, 25)

        self.transformBtn = tk.Button(self.FrameHomeTransData, text="Transform Data", image=self.transformIcon, width=120,
                                      height=50, bg='#DCDCDC', bd=1, compound='top', command=None).place(relx=0.63, rely=0.44)
        self.refreshBtn = tk.Button(self.FrameHomeTransData, text="Refresh data", image=self.refreshIcon, width=120,
                                    height=50, bg='#DCDCDC', bd=1, compound='top', command=None).place(relx=0.73, rely=0.44)
        self.exportBtn = tk.Button(self.FrameHomeTransData, text="Export data", image=self.exportIcon, width=120,
                                   height=50, bg='#DCDCDC', bd=1, compound='top', command=None).place(relx=0.83, rely=0.44)

        test = tk.Label(self.FrameHomeTransData, text="dfcersgsze").place(
            relx=0.84, rely=0.3)

    def ViewData(self):

        self.FrameTableData = tk.LabelFrame(
            self.root, text="Data", background="#FAEBD7").place(
            relx=0.035, rely=0.54, relheight=0.44, relwidth=0.92)

    def test(self):
        self.df = Api.Load_excel_data_1()
        print(self.df.shape)


app = PyData()
app.root.mainloop()
