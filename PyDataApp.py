if True:
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
    # from main import Api

class PyData:

    # param = {'path': ""}
    let_user_through = False

    def __init__(self):
        root = tk.Tk()
        self.root = root
        # self.root.withdraw()
        self.root.title("PyData Desktop")
        self.root.geometry("1400x800+5+5")
        self.root.iconbitmap('media/logo.ico')
        self.root.config(background="#FAEBD7")
        self.path_import = None
        self.path_export = None
        self.df = ""
        self.dct = {
            'id': "", 'name': ""
        }

        super().__init__()
        self.initUI()
        self.WedgetHome()
        self.widgetGetData()
        self.ViewData()

    def onExit(self):
        self.root.quit()

    def selected_item_1(self):
        for i in self.Lbox.curselection():
            # var_col_name_1.set(box1.get(i))
            # self.VarEntryRename.set(i)

            self.VarEntryRename.set("")
            self.VarEntryRename.set(self.Lbox.get(i))
            self.dct['id'] = i
            self.dct['name'] = self.Lbox.get(i)

    def Load_Path_Excel(self):

        global data

        """
        Cette fonction ouvrira l'explorateur de fichiers et 
        affectera le chemin de fichier choisi à label_file
        """
        path_filename = filedialog.askopenfilename(initialdir="E:\Total\Station Data\Master data\Data source",
                                                   title="Select A File",
                                                   filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))
        if path_filename:
            # self.test['text'] = path_filename
            self.path_import = path_filename

            def preview_data(self, path):
                global df

                self.preview = tk.Toplevel(self.root)
                self.preview.grab_set()
                self.preview.title("Previous Data")
                self.preview.iconbitmap('media/logo.ico')
                self.preview.geometry("600x250+15+15")
                self.preview.resizable(width=False, height=False)

                def ok_data_V():
                    # df = pd.read_excel(self.path_import)

                    clear_data_Table_Listbox()
                    self.tv_All_Data["column"] = list(df.columns)
                    self.tv_All_Data["show"] = "headings"

                    for column in self.tv_All_Data["columns"]:
                        self.tv_All_Data.column(column, anchor='center')
                        self.tv_All_Data.heading(column, text=column)

                    df_rows = df.to_numpy().tolist()
                    for row in df_rows:
                        self.tv_All_Data.insert("", "end", values=row)

                    for id, column in enumerate(df.columns):
                        self.Lbox.insert(id, column)

                    self.preview.destroy()
                    return df

                frame1 = tk.LabelFrame(self.preview, text=f"{path}")
                frame1.place(height=180, width=530, rely=0.05, relx=0.05)

                tv1 = ttk.Treeview(frame1)
                tv1.place(relheight=1, relwidth=1)

                # commande signifie mettre à jour la vue de l'axe y du widget
                treescrolly = tk.Scrollbar(
                    frame1, orient="vertical", command=tv1.yview)

                # commande signifie mettre à jour la vue axe x du widget
                treescrollx = tk.Scrollbar(
                    frame1, orient="horizontal", command=tv1.xview)

                # affecter les barres de défilement au widget Treeview
                tv1.configure(xscrollcommand=treescrollx.set,
                              yscrollcommand=treescrolly.set)

                # faire en sorte que la barre de défilement remplisse l'axe x du widget Treeview
                treescrollx.pack(side="bottom", fill="x")

                # faire en sorte que la barre de défilement remplisse l'axe y du widget Treeview
                treescrolly.pack(side="right", fill="y")

                OkBtn_data = tk.Button(self.preview, text="Ok", background='#40A497', activeforeground='white', activebackground='#40A497',
                                       command=lambda: df == ok_data_V()).place(relx=0.4, rely=0.85, height=30, width=60)

                Cancel_data = tk.Button(self.preview, text="Cancel", background='#CCCCCC',
                                        command=self.preview.destroy).place(relx=0.5, rely=0.85, height=30, width=60)

                def Load_excel_data_1():
                    """Si le fichier sélectionné est valide, cela chargera le fichier"""

                    try:
                        excel_filename = r"{}".format(path)
                        if excel_filename[-4:] == ".csv":
                            df1 = pd.read_csv(excel_filename)

                        else:
                            # if sheet == "":
                            df1 = pd.read_excel(excel_filename)

                            # else:
                            #     df1 = pd.read_excel(
                            #         excel_filename, sheet_name=sheet)

                    except ValueError:
                        tk.messagebox.showerror(
                            "Information", "The file you have chosen is invalid")
                        return None
                    except FileNotFoundError:
                        tk.messagebox.showerror(
                            "Information", f"No such file as {path}")
                        return None

                    clear_data()
                    tv1["column"] = list(df1.columns)
                    tv1["show"] = "headings"
                    for column in tv1["columns"]:
                        tv1.column(column, anchor='center')
                        tv1.heading(column, text=column)

                    df_rows = df1.head().to_numpy().tolist()
                    for row in df_rows:
                        tv1.insert("", "end", values=row)

                    return df1

                def clear_data():
                    tv1.delete(*tv1.get_children())
                    return None

                df = Load_excel_data_1()
                return df

            data = preview_data(self, self.path_import)

            def clear_data_Table_Listbox():
                self.tv_All_Data.delete(*self.tv_All_Data.get_children())
                self.Lbox.delete(0, 'end')
                # self.Lbox.delete()
                return None
        else:
            tk.messagebox.showerror(
                "Information", "You did not choose a file")

    def clear_data_Table(self):
        self.tv_All_Data.delete(*self.tv_All_Data.get_children())

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
                                  height=70, width=160, bd=1, bg="#DCDCDC", command=lambda: self.df == self.Load_Path_Excel()).place(relx=0.049, rely=0.25)

        self.csvBtn = tk.Button(self.FrameGetData, image=self.csvIcon, text="Import data from CSV", compound='top',
                                height=70, width=160, bd=1, bg="#DCDCDC", command=None).place(relx=0.174, rely=0.25)

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

        self.RenameCol = tk.Button(
            self.FrameHomeTransData, background="#DCDCDC", activebackground="#FFA500", activeforeground='white', text="Rename column", command=self.selected_item_1).place(relx=0.63, rely=0.22, relheight=0.05, relwidth=0.08)

        self.VarEntryRename = tk.StringVar()
        self.Entry_RenameColumn = tk.Entry(self.FrameHomeTransData, textvariable=self.VarEntryRename).place(
            relx=0.72, rely=0.23, relheight=0.03, relwidth=0.17)

        self.RomeveCol = tk.Button(
            self.FrameHomeTransData, background="#DCDCDC", activebackground="#C60030", activeforeground='white', text="Remove column", command=self.DropColumn).place(relx=0.63, rely=0.27, relheight=0.05, relwidth=0.08)

        self.AddCol = tk.Button(
            self.FrameHomeTransData, background="#DCDCDC", activebackground="#004C8C", activeforeground='white', text="Add column", command=None).place(relx=0.63, rely=0.32, relheight=0.05, relwidth=0.08)

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

        self.refreshIcon = PhotoImage(file="media/save.png")
        self.refreshIcon = self.refreshIcon.subsample(30, 30)

        self.exportIcon = PhotoImage(file="media/export.png")
        self.exportIcon = self.exportIcon.subsample(25, 25)

        self.transformBtn = tk.Button(self.FrameHomeTransData, text="Transform Data", image=self.transformIcon, width=120,
                                      height=50, bg='#DCDCDC', bd=1, compound='top', command=self.RenameColumnTable).place(relx=0.63, rely=0.43)
        self.refreshBtn = tk.Button(self.FrameHomeTransData, text="Save", image=self.refreshIcon, width=120,
                                    height=50, bg='#DCDCDC', bd=1, compound='top', command=None).place(relx=0.73, rely=0.43)
        self.exportBtn = tk.Button(self.FrameHomeTransData, text="Export data", image=self.exportIcon, width=120,
                                   height=50, bg='#DCDCDC', bd=1, compound='top', command=self.ExportData).place(relx=0.83, rely=0.43)

        # self.test = tk.Label(self.FrameHomeTransData, text="dfcersgsze")
        # self.test.place(
        #     relx=0.74, rely=0.3)

    def ViewData(self):

        self.FrameTableData = tk.LabelFrame(
            self.root, text="Data", background="#FAEBD7")
        self.FrameTableData.place(
            relx=0.035, rely=0.54, relheight=0.44, relwidth=0.92)

        self.tv_All_Data = ttk.Treeview(self.FrameTableData)
        self.tv_All_Data.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

        # commande signifie mettre à jour la vue de l'axe y du widget
        treescrolly = tk.Scrollbar(
            self.tv_All_Data, orient="vertical", command=self.tv_All_Data.yview)

        # commande signifie mettre à jour la vue axe x du widget
        treescrollx = tk.Scrollbar(
            self.tv_All_Data, orient="horizontal", command=self.tv_All_Data.xview)

        # affecter les barres de défilement au widget Treeview
        self.tv_All_Data.configure(xscrollcommand=treescrollx.set,
                                   yscrollcommand=treescrolly.set)

        # faire en sorte que la barre de défilement remplisse l'axe x du widget Treeview
        treescrollx.pack(side="bottom", fill="x")

        # faire en sorte que la barre de défilement remplisse l'axe y du widget Treeview
        treescrolly.pack(side="right", fill="y")

    def RenameColumnTable(self):
        # renommer dans le treeview
        # print(self.tv_All_Data.column(int(self.dct['id'])))
        self.tv_All_Data.heading(
            int(self.dct['id']), text=self.VarEntryRename.get())
        # renommer dans la listbox
        for item in self.Lbox.curselection():
            self.Lbox.delete(item)
            self.Lbox.insert(int(self.dct['id']), self.VarEntryRename.get())
        # renommer dans le données
        data.rename(columns={
            data.columns[int(self.dct['id'])]: self.VarEntryRename.get()}, inplace=True)
        
    def DropColumn(self):
        
        global ColSup
        for i in self.Lbox.curselection():
            ColSup = self.Lbox.get(i)
            self.Lbox.delete(i)
            
        # supprimer la colonne dans le données
        data.drop(ColSup, axis=1, inplace=True) 
        # print(data.head(3))
        
            
        # supprimer dans le treeview
        self.clear_data_Table()
        self.tv_All_Data["column"] = list(data.columns)
        self.tv_All_Data["show"] = "headings"

        for column in self.tv_All_Data["columns"]:
            self.tv_All_Data.column(column, anchor='center')
            self.tv_All_Data.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.tv_All_Data.insert("", "end", values=row)

    def ExportData(self):
        def ExportGUI(self):
            
            # def update_observer_path_folder(*args):
            #     self.path_export = self.VarEntry_path_export.get()
            
            def h():
                if self.VarRadioInt.get():
                    print(f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.xlsx")
                else:
                    print(f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.csv")
            
            def browse_button():
                pth = filedialog.askdirectory()
                self.VarEntry_path_export.set(pth)
            
            def CancelExport():
                self.Exportation.destroy()
            
            def OkExport():
                if self.VarEntry_path_export.get():
                    if self.VarEntry_name_file.get():
                        
                        self.path_export = self.VarEntry_path_export.get() +'/'+ self.VarEntry_name_file.get()
                        try:
                            if self.VarRadioInt.get():
                                try:
                                    data.to_excel(f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.xlsx", index=False)
                                    
                                    self.Exportation.destroy()
                                except NameError or TypeError or FileNotFoundError:
                                    tk.messagebox.showerror(
                            "Information", "There is no data to export")
                            else:
                                try:
                                    data.to_csv(f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.csv", index=False)
                                    
                                    self.Exportation.destroy()
                                except NameError or TypeError or FileNotFoundError:
                                    tk.messagebox.showerror(
                            "Information", "There is no data to export")
                        except ValueError & FileNotFoundError:
                            tk.messagebox.showerror(
                            "Information", "incorrect destination path")
                            
                        # except FileNotFoundError:
                        #     tk.messagebox.showerror(
                        #         "Information", f"No such file as {self.path_export}.xlsx")
                    else:
                        tk.messagebox.showerror(
                "Information", "Please give a name to the file")
                else:
                    tk.messagebox.showerror(
                "Information", "Please choose a destination folder")
                
                

            self.Exportation = tk.Toplevel(self.root)
            self.Exportation.grab_set()
            self.Exportation.title("Previous Data")
            self.Exportation.iconbitmap('media/logo.ico')
            self.Exportation.geometry("500x200+15+15")
            # self.Exportation.config(background="#CCCCCC")
            self.Exportation.resizable(width=False, height=False)

            self.f_ex_1 = tk.Frame(self.Exportation)
            self.f_ex_1.place(relx=0.05, rely=0.1)
            
            self.btn_path_export = tk.Button(self.f_ex_1, text="Browse", width=8, height=1, command=browse_button)
            self.btn_path_export.grid(row=0, column=0)
            
            self.VarEntry_path_export = tk.StringVar()
            # self.VarEntry_path_export.trace('w', update_observer_path_folder)
            self.Entry_path_export = tk.Entry(self.f_ex_1, textvariable=self.VarEntry_path_export, width=60, background="#F1F1F1")
            self.Entry_path_export.grid(row=0, column=1, padx=5)
            
            self.VarRadioInt = tk.IntVar()
            self.RadioBtnCSV = tk.Radiobutton(self.Exportation, text='CSV', value=0, variable=self.VarRadioInt).place(relx=0.05, rely=0.35)
            
            self.RadioBtnExcel = tk.Radiobutton(self.Exportation, text='Excel', value=1, variable=self.VarRadioInt).place(relx=0.05, rely=0.45)
            
            self.lbl_name = tk.Label(self.Exportation, text='Name file :').place(relx=0.25, rely=0.4)
            
            self.VarEntry_name_file = tk.StringVar()
            self.Entry_name_file = tk.Entry(self.Exportation, width=30, textvariable=self.VarEntry_name_file).place(relx=0.4, rely=0.4)
            
            self.OkExportBtn = tk.Button(self.Exportation, text="OK", background="#6DA3F4", activebackground="#0256CD", foreground='white', activeforeground='white', width=12, height=1, command=OkExport).place(relx=0.3, rely=0.8)
            
            self.CancelExportBtn = tk.Button(self.Exportation, text="Cancel", background="#CCCCCC", width=12, height=1, command=CancelExport).place(relx=0.5, rely=0.8)
        
            
        ExportGUI(self)
    
app = PyData()
app.root.mainloop()