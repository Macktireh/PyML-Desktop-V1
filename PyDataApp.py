# Importer les bibliothèque
if True:
    import os
    import sqlite3
    import tkinter as tk
    import tempfile
    import pandas as pd
    import numpy as np
    from tkinter import font
    from tkinter.constants import RADIOBUTTON, RAISED
    from tkinter.scrolledtext import ScrolledText
    from tkinter import PhotoImage
    from PIL import Image, ImageTk

    # from tkinter_custom_button import TkinterCustomButton
    from tkinter import filedialog, messagebox, ttk
    from tkinter.constants import ACTIVE
    from datetime import date, datetime
    from openpyxl import load_workbook
    import psycopg2


class PyData:

    # param = {'path': ""}
    let_user_through = False

    def __init__(self):
        root = tk.Tk()
        self.root = root
        # self.root.withdraw()
        self.root.title("PyData Desktop")
        self.root.geometry("1400x800+5+5")
        self.root.iconbitmap("media/logo.ico")
        self.root.config(background="#FAEBD7")
        self.path_import = None
        self.path_export = None
        self.typefile = None
        self.df = ""
        self.data_origine = pd.DataFrame()
        self.data_pre = pd.DataFrame()
        self.dct = {"id": "", "name": ""}

        super().__init__()
        self.initUI()
        self.WedgetHome()
        self.widgetGetData()
        self.ViewData()

    def onExit(self):
        """cette fonction permet de quiter la logiciel"""
        self.root.quit()

    def Data_Viz(self):
        self.window_data_viz = tk.Toplevel(self.root)
        self.window_data_viz.grab_set()
        self.window_data_viz.title("Data Visualization")
        self.window_data_viz.iconbitmap("media/logo.ico")
        self.window_data_viz.geometry("800x600+15+15")
        self.window_data_viz.resizable(width=False, height=False)

    def Load_Data_PosgreSQL(self):
        self.window_postgresql = tk.Toplevel(self.root)
        self.window_postgresql.grab_set()
        self.window_postgresql.title("PostgreSQL database")
        self.window_postgresql.iconbitmap("media/logo.ico")
        self.window_postgresql.geometry("500x600+15+15")
        self.window_postgresql.resizable(width=False, height=False)

        def Cancel_widow_prosgresql():
            self.window_postgresql.destroy()

        def Requete_SQL():

            if (
                self.text_sql.get("1.0", "end-1c")
                and self.VarEntry_port.get()
                and self.VarEntry_dbname.get
                and self.VarEntryUser.get()
                and self.VarEntrypassword.get()
            ):
                try:

                    connexion = psycopg2.connect(
                        dbname=f"{self.VarEntry_dbname.get()}",
                        user=f"{self.VarEntryUser.get()}",
                        host=f"{self.VarEntry_host.get()}",
                        password=f"{self.VarEntrypassword.get()}",
                        port=f"{self.VarEntry_port.get()}",
                    )
                    cur = connexion.cursor()
                    cur.execute(f"{self.text_sql.get('1.0', 'end-1c')}")
                    row = cur.fetchall()

                    col_names = []
                    for elt in cur.description:
                        col_names.append(elt[0])

                    df = pd.DataFrame(
                        row,
                        columns=col_names,
                    )
                    df.reset_index(inplace=True)
                    df = df.rename(columns={"index": "Id"})

                    self.data_origine = df
                    self.data_pre = self.data_origine.copy()

                    self.path_import = f"Table data {self.VarEntry_dbname.get()} from the PostgreSQL database "

                    self.preview_data(self.path_import, self.data_pre)
                    self.window_postgresql.destroy()
                except:
                    tk.messagebox.showerror("Information", "Echec connexion !")
            else:
                tk.messagebox.showerror("Information", "some fields are not filled")

        # Importation de l'icone de progresql
        self.img = PhotoImage(file="media/postgresql.png")
        self.img = self.img.subsample(35, 35)

        # afficher l'icone de progresql
        self.print_img = tk.Label(
            self.window_postgresql, image=self.img, width=90, height=90
        )
        self.print_img.place(relx=0.01, rely=0.01)

        #  label de titre progresql
        self.lbl_title = tk.Label(
            self.window_postgresql, text="PostgreSQL database", font=("Helvetica", 16)
        )
        self.lbl_title.place(relx=0.25, rely=0.05)

        # label de host
        self.lbl_dbname = tk.Label(
            self.window_postgresql, text="Host", font=("Helvetica", 10)
        ).place(relx=0.07, rely=0.2)
        # Entry de host
        self.VarEntry_host = tk.StringVar()
        self.VarEntry_host.set("localhost")
        self.VarEntry_host = tk.Entry(
            self.window_postgresql, textvariable=self.VarEntry_host, width=40
        )
        self.VarEntry_host.place(relx=0.28, rely=0.2)

        # label de Database
        self.lbl_dbname = tk.Label(
            self.window_postgresql, text="Database", font=("Helvetica", 10)
        ).place(relx=0.07, rely=0.25)
        # Entry de Database
        self.VarEntry_dbname = tk.StringVar()
        self.VarEntry_dbname.set("covid")
        self.Entry_dbname = tk.Entry(
            self.window_postgresql, textvariable=self.VarEntry_dbname, width=40
        )
        self.Entry_dbname.place(relx=0.28, rely=0.25)

        # label de Port
        self.lbl_port = tk.Label(
            self.window_postgresql, text="Port", font=("Helvetica", 10)
        ).place(relx=0.07, rely=0.3)
        # Entry de Port
        self.VarEntry_port = tk.StringVar()
        self.VarEntry_port.set("5444")
        self.Entry_port = tk.Entry(
            self.window_postgresql, textvariable=self.VarEntry_port, width=40
        )
        self.Entry_port.place(relx=0.28, rely=0.3)

        # Username
        self.lbl_user = tk.Label(
            self.window_postgresql, text="User Name", font=("Helvetica", 10)
        ).place(relx=0.07, rely=0.35)
        self.VarEntryUser = tk.StringVar()
        self.VarEntryUser.set("enterprisedb")
        self.EntryUser = tk.Entry(
            self.window_postgresql, textvariable=self.VarEntryUser, width=40
        ).place(relx=0.28, rely=0.35)

        # password
        self.lbl_password = tk.Label(
            self.window_postgresql, text="Password", font=("Helvetica", 9)
        ).place(relx=0.07, rely=0.4)
        self.VarEntrypassword = tk.StringVar()
        self.VarEntrypassword.set("charco97")
        self.Entrypassword = tk.Entry(
            self.window_postgresql,
            textvariable=self.VarEntrypassword,
            width=40,
            show="*",
        ).place(relx=0.28, rely=0.4)

        # label Text Widget pour ecrire su sql
        self.lbl_sql = tk.Label(
            self.window_postgresql,
            text="Please write your SQL query",
            font=("Helvetica", 12),
        ).place(relx=0.1, rely=0.48)
        # Text Widget pour ecrire su sql
        self.text_sql = ScrolledText(self.window_postgresql, font=("Helvetica", 10))
        self.text_sql.place(relx=0.1, rely=0.52, relwidth=0.8, relheight=0.35)

        self.OkPogreSQL = tk.Button(
            self.window_postgresql,
            text="OK",
            background="#6DA3F4",
            activebackground="#0256CD",
            foreground="white",
            activeforeground="white",
            width=12,
            height=1,
            command=Requete_SQL,
        )
        self.OkPogreSQL.place(relx=0.31, rely=0.9)

        self.CacelPogreSQL = tk.Button(
            self.window_postgresql,
            text="Cancel",
            background="#CCCCCC",
            width=12,
            height=1,
            command=Cancel_widow_prosgresql,
        )
        self.CacelPogreSQL.place(relx=0.50, rely=0.9)
        # pass

    def switchButtonState(self):

        """Cette fonction de switcher les boutons dans le volet transformation de deactive en active. Elle est appeler lorsque on clique on valide le chargement de données (le bouton ok dans le preview data)"""

        if self.RenameCol["state"] == "disabled":
            self.RenameCol["state"] = "normal"
        else:
            self.RenameCol["state"] = "normal"

        if self.RomeveCol["state"] == "disabled":
            self.RomeveCol["state"] = "normal"
        else:
            self.RomeveCol["state"] = "normal"

        if self.AddCol["state"] == "disabled":
            self.AddCol["state"] = "normal"
        else:
            self.AddCol["state"] = "normal"

        if self.transformBtn["state"] == "disabled":
            self.transformBtn["state"] = "normal"
        else:
            self.transformBtn["state"] = "normal"

        if self.saveBtn["state"] == "disabled":
            self.saveBtn["state"] = "normal"
        else:
            self.saveBtn["state"] = "normal"

        if self.exportBtn["state"] == "disabled":
            self.exportBtn["state"] = "normal"
        else:
            self.exportBtn["state"] = "normal"

    def Load_data_file(self):

        """
        Cette grosse fonction permet d'abord d'ouvrir l'explorateur et parcourir le schéma du fichier, enssuite de le prévisualiser les 5 premières lignes et enfin les données sont ok elle permet d'importer toutes les données

        Données : Excel, CSV, TXT
        """

        # global data_origine, data_pre

        if self.typefile == "Excel":
            path_filename = filedialog.askopenfilename(
                initialdir="E:\Total\Station Data\Master data\Data source",
                title="Select A File",
                filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")),
            )

        elif self.typefile == "CSV":
            path_filename = filedialog.askopenfilename(
                initialdir="E:\Total\Station Data\Master data\Data source",
                title="Select A File",
                filetype=(("csv files", "*.csv"), ("All Files", "*.*")),
            )

        elif self.typefile == "TXT":
            path_filename = filedialog.askopenfilename(
                initialdir="E:\Total\Station Data\Master data\Data source",
                title="Select A File",
                filetype=(("txt files", "*.txt"), ("All Files", "*.*")),
            )

        else:
            path_filename = filedialog.askopenfilename(
                initialdir="E:\Total\Station Data\Master data\Data source",
                title="Select A File",
                filetype=(("All Files", "*.*")),
            )

        if path_filename:
            # self.test['text'] = path_filename
            self.path_import = path_filename

            def Load_excel_data_1(path):
                """Si le fichier sélectionné est valide, cela chargera le fichier"""

                try:
                    excel_filename = r"{}".format(path)
                    if excel_filename[-4:] == ".csv":
                        df = pd.read_csv(excel_filename)
                        df.reset_index(inplace=True)
                        df = df.rename(columns={"index": "Id"})

                    elif excel_filename[-4:] == ".txt":
                        df = pd.read_table(excel_filename)
                        df.reset_index(inplace=True)
                        df = df.rename(columns={"index": "Id"})

                    else:
                        # if sheet == "":
                        df = pd.read_excel(excel_filename)
                        df.reset_index(inplace=True)
                        df = df.rename(columns={"index": "Id"})

                        # else:
                        #     df1 = pd.read_excel(
                        #         excel_filename, sheet_name=sheet)

                except ValueError:
                    tk.messagebox.showerror(
                        "Information", "The file you have chosen is invalid"
                    )
                    return None
                except FileNotFoundError:
                    tk.messagebox.showerror("Information", f"No such file as {path}")
                    return None
                return df

            # df = Load_excel_data_1()
            self.data_origine = Load_excel_data_1(self.path_import)
            self.data_pre = self.data_origine.copy()
            self.preview_data(self.path_import, self.data_pre)

        else:
            tk.messagebox.showerror("Information", "You did not choose a file")

    def preview_data(self, path, df):

        """
        Cette sous fonction de la fonction Load_data_file() permet d'imorter les données et d'ouvrir une petite fenetre afin de prévisualiser les 5 premières lignes et enfin les données sont ok elle permet d'importer toutes les données
        """

        # global df

        self.preview = tk.Toplevel(self.root)
        self.preview.grab_set()
        self.preview.title("Previous Data")
        self.preview.iconbitmap("media/logo.ico")
        self.preview.geometry("600x250+15+15")
        self.preview.resizable(width=False, height=False)

        def clear_data():
            tv1.delete(*tv1.get_children())
            return None

        def clear_data_Table_Listbox():
            self.tv_All_Data.delete(*self.tv_All_Data.get_children())
            self.Lbox.delete(0, "end")
            # self.Lbox.delete()
            return None

        def ok_data_V():

            """Cette fonction valide les données et affiche toutes les données. Elle est relier au bouton ok pour valider"""
            global count
            count = 0

            self.tv_All_Data.tag_configure("oddrow", background="white")
            self.tv_All_Data.tag_configure("evenrow", background="#D3D3D3")

            clear_data_Table_Listbox()
            self.tv_All_Data["column"] = list(df.columns)
            self.tv_All_Data["show"] = "headings"

            for column in self.tv_All_Data["columns"]:
                self.tv_All_Data.column(column, anchor="w")
                self.tv_All_Data.heading(column, anchor="w", text=column)

            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                if count % 2 == 0:
                    self.tv_All_Data.insert(
                        "",
                        "end",
                        iid=count,
                        values=row,
                        tags=("evenrow",),
                    )
                else:
                    self.tv_All_Data.insert(
                        "",
                        "end",
                        iid=count,
                        values=row,
                        tags=("oddrow",),
                    )
                count += 1

            self.tv_All_Data.insert("", "end", values="")

            for id, column in enumerate(df.columns):
                col_typ = f" {column}  : {np.dtype(df[column])}     "
                self.Lbox.insert(id, col_typ)

            self.switchButtonState()

            self.preview.destroy()
            return df

        frame1 = tk.LabelFrame(self.preview, text=f"{path}")
        frame1.place(height=180, width=530, rely=0.05, relx=0.05)

        tv1 = ttk.Treeview(frame1)
        tv1.place(relheight=1, relwidth=1)

        # commande signifie mettre à jour la vue de l'axe y du widget
        treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview)

        # commande signifie mettre à jour la vue axe x du widget
        treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview)

        # affecter les barres de défilement au widget Treeview
        tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)

        # faire en sorte que la barre de défilement remplisse l'axe x du widget Treeview
        treescrollx.pack(side="bottom", fill="x")

        # faire en sorte que la barre de défilement remplisse l'axe y du widget Treeview
        treescrolly.pack(side="right", fill="y")

        OkBtn_data = tk.Button(
            self.preview,
            # text="Ok",
            # background="#40A497",
            # activeforeground="white",
            # activebackground="#40A497",
            text="OK",
            background="#6DA3F4",
            activebackground="#0256CD",
            foreground="white",
            activeforeground="white",
            width=12,
            height=1,
            command=lambda: df == ok_data_V(),
        ).place(relx=0.32, rely=0.85)

        Cancel_data = tk.Button(
            self.preview,
            text="Cancel",
            background="#CCCCCC",
            width=12,
            height=1,
            command=self.CancelPreviwData,
        ).place(relx=0.48, rely=0.85)

        clear_data()
        tv1["column"] = list(df.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.column(column, anchor="center")
            tv1.heading(column, text=column)

        df_rows = df.head().to_numpy().tolist()
        for row in df_rows:
            tv1.insert("", "end", values=row)

        return None

    def Excel(self):
        self.typefile = "Excel"
        self.Load_data_file()
        # self.preview_data(self.path_import, self.data_pre)

    def CSV(self):
        self.typefile = "CSV"
        self.Load_data_file()
        # self.preview_data(self.path_import, self.data_pre)

    def TXT(self):
        self.typefile = "TXT"
        self.Load_data_file()
        # self.preview_data(self.path_import, self.data_pre)

    def PostgreSQL(self):
        self.Load_Data_PosgreSQL()
        # self.preview_data(self.path_import, self.data_pre)

    def CancelPreviwData(self):
        self.data_origine = pd.DataFrame()
        self.data_pre = pd.DataFrame()
        self.preview.destroy()

    def initUI(self):

        self.menubar = tk.Menu(self.root, background="#856ff8", fg="white")
        self.root.config(menu=self.menubar)

        # instancier les menu
        self.fileMenu = tk.Menu(self.menubar, tearoff=0, bg="lightgray")
        self.HomeMenu = tk.Menu(self.menubar, tearoff=0, bg="lightgray")
        self.ToolsMenu = tk.Menu(self.menubar, tearoff=0, bg="lightgray")
        self.HelpMenu = tk.Menu(self.menubar, tearoff=0, bg="lightgray")

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
        self.HomeMenu.add_command(label="Data Viz", command=self.Data_Viz)

        # sous menu Machine learning
        self.menu_sub_ml = tk.Menu(self.HomeMenu, tearoff=0)
        self.HomeMenu.add_cascade(label="Machine Learning", menu=self.menu_sub_ml)
        # sous model
        self.menu_sub_model = tk.Menu(self.menu_sub_ml, tearoff=0)
        self.menu_sub_ml.add_cascade(label="Regressor", menu=self.menu_sub_model)
        self.menu_sub_model.add_command(label="LinearRegressor")
        self.menu_sub_model.add_command(label="RandomForestRegressor")
        self.menu_sub_model.add_command(label="KNeighborsRegressor")
        self.menu_sub_model.add_command(label="DecisionTreeRegressor")

        # sous model
        self.menu_sub_model = tk.Menu(self.menu_sub_ml, tearoff=0)
        self.menu_sub_ml.add_cascade(label="Classifier", menu=self.menu_sub_model)
        self.menu_sub_model.add_command(label="LogisticRegression")
        self.menu_sub_model.add_command(label="RandomForestClassifier")
        self.menu_sub_model.add_command(label="KNeighborsClassifier")
        self.menu_sub_model.add_command(label="DecisionTreeClassifier")
        self.menu_sub_model.add_command(label="SVM")

        # Barre entet
        self.barheader = tk.Frame(self.root, bd=20, bg="#FFA500", height=40)
        self.barheader.pack(side="top", fill="x")
        # # titre
        # self.maintitle = tk.Label(
        #     self.barheader,
        #     text="Welcome to Power Studio Data Desktop !",
        #     font=("Algeria 20"),
        #     bg="#FFA500",
        # )
        # self.maintitle.pack(side="bottom", fill="x")

        # WidgetFrame = tk.Frame(self.root, bg='white').place(
        #     relx=0.05, rely=0.1)

    def widgetGetData(self):

        self.FrameGetData = tk.LabelFrame(
            self.root, text="Get Data", background="#FAEBD7"
        )
        self.FrameGetData.place(relx=0.035, rely=0.06, relheight=0.4, relwidth=0.4)

        self.title = tk.Label(
            self.FrameGetData,
            text="Once loaded, your data will be displayed below",
            background="#FAEBD7",
            height=3,
            font=("Helvetica", 11),
        ).place(relx=0.09, rely=0.01)

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
        self.excelBtn = tk.Button(
            self.FrameGetData,
            image=self.excelIcon,
            text="Import data from Excel",
            compound="top",
            height=70,
            width=160,
            bd=1,
            bg="#DCDCDC",
            command=self.Excel,
        ).place(relx=0.025, rely=0.18)

        self.csvBtn = tk.Button(
            self.FrameGetData,
            image=self.csvIcon,
            text="Import data from CSV",
            compound="top",
            height=70,
            width=160,
            bd=1,
            bg="#DCDCDC",
            command=self.CSV,
        ).place(relx=0.35, rely=0.18)

        self.txtbtn = tk.Button(
            self.FrameGetData,
            image=self.txtIcon,
            text="Import data from TXT",
            compound="top",
            height=70,
            width=160,
            bd=1,
            bg="#DCDCDC",
            command=self.TXT,
        ).place(relx=0.675, rely=0.18)

        self.postgrebtn = tk.Button(
            self.FrameGetData,
            image=self.postgreIcon,
            text="Import data from PostgreSQL",
            compound="top",
            height=70,
            width=160,
            bd=1,
            bg="#DCDCDC",
            command=self.PostgreSQL,
        ).place(relx=0.025, rely=0.48)

        self.mysqlbtn = tk.Button(
            self.FrameGetData,
            image=self.mysqlIcon,
            text="Import data from MySQL",
            compound="top",
            height=70,
            width=160,
            bd=1,
            bg="#DCDCDC",
            command=None,
        ).place(relx=0.35, rely=0.48)

        self.mongobtn = tk.Button(
            self.FrameGetData,
            image=self.mongodbIcon,
            text="Import data from MongoDB",
            compound="top",
            height=70,
            width=160,
            bd=1,
            bg="#DCDCDC",
            command=None,
        ).place(relx=0.675, rely=0.48)

    def WedgetHome(self):

        self.FrameHomeTransData = tk.LabelFrame(
            self.root, text="Data Processing", background="#FAEBD7"
        )
        self.FrameHomeTransData.place(
            relx=0.45, rely=0.06, relheight=0.4, relwidth=0.505
        )

        self.LabelCol = tk.Label(
            self.FrameHomeTransData, background="#FAEBD7", text="Columns :"
        ).place(relx=0.03, rely=0.02)

        self.RenameCol = tk.Button(
            self.FrameHomeTransData,
            background="#DCDCDC",
            activebackground="#FFA500",
            activeforeground="white",
            text="Rename column",
            command=self.RenameColumnTable,
            state="disabled",
        )
        self.RenameCol.place(relx=0.65, rely=0.2, relheight=0.13, relwidth=0.18)

        self.VarEntryRename = tk.StringVar()
        self.Entry_RenameColumn = tk.Entry(
            self.FrameHomeTransData,
            textvariable=self.VarEntryRename,
            font=("Helvetica", 10),
        ).place(relx=0.3, rely=0.2, relheight=0.08, relwidth=0.3)

        self.RomeveCol = tk.Button(
            self.FrameHomeTransData,
            background="#DCDCDC",
            activebackground="#C60030",
            activeforeground="white",
            text="Remove column",
            command=self.DropColumn,
            state="disabled",
        )
        self.RomeveCol.place(relx=0.65, rely=0.34, relheight=0.13, relwidth=0.18)

        self.AddCol = tk.Button(
            self.FrameHomeTransData,
            background="#DCDCDC",
            activebackground="#004C8C",
            activeforeground="white",
            text="Add column",
            command=None,
            state="disabled",
        )
        self.AddCol.place(relx=0.65, rely=0.48, relheight=0.13, relwidth=0.18)

        self.Lbox = tk.Listbox(
            self.FrameHomeTransData, bg="#F5F5F5", width=1000, height=1
        )
        self.Lbox.place(relx=0.009, rely=0.1, relheight=0.85, relwidth=0.27)

        self.treescrolly = tk.Scrollbar(self.Lbox, orient="vertical")
        self.treescrolly.configure(command=self.Lbox.yview)

        self.treescrollx = tk.Scrollbar(
            self.Lbox, orient="horizontal", command=self.Lbox.xview
        )

        self.Lbox.configure(
            xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set
        )

        self.treescrollx.pack(side="bottom", fill="x")
        self.treescrolly.pack(side="right", fill="y")

        self.transformIcon = PhotoImage(file="media/transform.png")
        self.transformIcon = self.transformIcon.subsample(40, 40)

        self.saveIcon = PhotoImage(file="media/save.png")
        self.saveIcon = self.saveIcon.subsample(40, 40)

        self.exportIcon = PhotoImage(file="media/export.png")
        self.exportIcon = self.exportIcon.subsample(35, 35)

        self.transformBtn = tk.Button(
            self.FrameHomeTransData,
            text="Transform Data",
            image=self.transformIcon,
            width=120,
            height=40,
            bg="#DCDCDC",
            bd=1,
            compound="top",
            command=None,
            state="disabled",
        )
        self.transformBtn.place(relx=0.3, rely=0.8)

        self.saveBtn = tk.Button(
            self.FrameHomeTransData,
            text="Save",
            image=self.saveIcon,
            width=120,
            height=40,
            bg="#DCDCDC",
            bd=1,
            compound="top",
            command=None,
            state="disabled",
        )
        self.saveBtn.place(relx=0.5, rely=0.8)

        self.exportBtn = tk.Button(
            self.FrameHomeTransData,
            text="Export data",
            image=self.exportIcon,
            width=120,
            height=40,
            bg="#DCDCDC",
            bd=1,
            compound="top",
            command=self.ExportData,
            state="disabled",
        )
        self.exportBtn.place(relx=0.7, rely=0.8)

        self.Lbox.bind("<Double-Button-1>", self.Def_edit_name_col_in_entry)

        # self.test = tk.Label(self.FrameHomeTransData, text="dfcersgsze")
        # self.test.place(
        #     relx=0.74, rely=0.3)

    def ViewData(self):

        self.FrameTableData = tk.LabelFrame(
            self.root, text="Data", background="#FAEBD7"
        )
        self.FrameTableData.place(relx=0.035, rely=0.47, relheight=0.5, relwidth=0.92)

        # Add Some Style
        style = ttk.Style()

        # Pick A Theme
        style.theme_use("clam")

        # Configure the Treeview Colors
        style.configure(
            "Treeview.Heading",
            background="lightblue",
            foreground="black",
            rowheight=25,
            fieldbackground="white",
        )
        # style.theme_use("clam")
        # style.configure(
        #     "Treeview.Heading", background="lightblue", foreground="black"
        # )

        # Change Selected Color
        style.map("Treeview", background=[("selected", "#347083")])

        # label de rechercher
        self.label_Fx = tk.Label(
            self.FrameTableData, text="fx", font=("Helvetica", 10), background="#FAEBD7"
        ).place(relx=0.05, rely=0.007)

        # entry : bar de formule
        self.VarEntryFx = tk.StringVar()
        self.entry_Fx = tk.Entry(
            self.FrameTableData, textvariable=self.VarEntryFx, width=100
        )
        self.entry_Fx.place(relx=0.07, rely=0.01)

        # liste déroulente pour selectionner une colonne
        self.listderoulente_column = ttk.Combobox(self.FrameTableData)
        self.listderoulente_column.place(relx=0.6, rely=0)

        # button rechercher ou executer la formule
        self.button_executor_fx = tk.Button(
            self.FrameTableData,
            background="#DCDCDC",
            activebackground="#004C8C",
            activeforeground="white",
            text="Search",
            width=13,
            command=None,
        )
        self.button_executor_fx.place(relx=0.83, rely=0)

        # button appliquer la formule aux données
        self.button_apply_fx = tk.Button(
            self.FrameTableData,
            background="#DCDCDC",
            activebackground="#004C8C",
            activeforeground="white",
            text="Apply",
            width=13,
            command=None,
        )
        self.button_apply_fx.place(relx=0.91, rely=0)

        self.tv_All_Data = ttk.Treeview(self.FrameTableData)
        self.tv_All_Data.place(relx=0, rely=0.1, relheight=0.75, relwidth=1)

        # commande signifie mettre à jour la vue de l'axe y du widget
        treescrolly = tk.Scrollbar(
            self.tv_All_Data, orient="vertical", command=self.tv_All_Data.yview
        )

        # commande signifie mettre à jour la vue axe x du widget
        treescrollx = tk.Scrollbar(
            self.tv_All_Data, orient="horizontal", command=self.tv_All_Data.xview
        )

        # affecter les barres de défilement au widget Treeview
        self.tv_All_Data.configure(
            xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set
        )

        # faire en sorte que la barre de défilement remplisse l'axe x du widget Treeview
        treescrollx.pack(side="bottom", fill="x")

        # faire en sorte que la barre de défilement remplisse l'axe y du widget Treeview
        treescrolly.pack(side="right", fill="y")

    def Def_edit_name_col_in_entry(self, event):
        for i in self.Lbox.curselection():
            # var_col_name_1.set(box1.get(i))
            # self.VarEntryRename.set(i)

            self.VarEntryRename.set("")
            col_typ = self.Lbox.get(i).split("  : ")[0].strip()
            self.VarEntryRename.set(col_typ)
            self.dct["id"] = i
            self.dct["name"] = col_typ

    def RenameColumnTable(self):

        self.data_pre.rename(
            columns={
                self.data_pre.columns[int(self.dct["id"])]: self.VarEntryRename.get()
            },
            inplace=True,
        )

        # renommer dans le treeview
        # print(self.tv_All_Data.column(int(self.dct['id'])))
        self.tv_All_Data.heading(int(self.dct["id"]), text=self.VarEntryRename.get())
        # renommer dans la listbox
        for item in self.Lbox.curselection():
            self.Lbox.delete(item)
            col_typ = f" {self.VarEntryRename.get()}  : {np.dtype(self.data_pre[self.VarEntryRename.get()])}     "
            self.Lbox.insert(int(self.dct["id"]), col_typ)
        # renommer dans le données

    def clear_data_Table(self):
        self.tv_All_Data.delete(*self.tv_All_Data.get_children())

    def DropColumn(self):

        global ColSup
        nb = 0

        for i in self.Lbox.curselection():
            ColSup = self.Lbox.get(i).split("  : ")[0].strip()
            self.Lbox.delete(i)

        # supprimer la colonne dans le données
        self.data_pre.drop(ColSup, axis=1, inplace=True)
        # print(data.head(3))

        self.tv_All_Data.tag_configure("oddrow", background="white")
        self.tv_All_Data.tag_configure("evenrow", background="#D3D3D3")

        # supprimer dans le treeview
        self.clear_data_Table()
        self.tv_All_Data["column"] = list(self.data_pre.columns)
        self.tv_All_Data["show"] = "headings"

        for column in self.tv_All_Data["columns"]:
            self.tv_All_Data.column(column, anchor="center")
            self.tv_All_Data.heading(column, text=column)

        df_rows = self.data_pre.to_numpy().tolist()
        for row in df_rows:
            if nb % 2 == 0:
                self.tv_All_Data.insert(
                    "",
                    "end",
                    iid=nb,
                    values=row,
                    tags=("evenrow",),
                )
            else:
                self.tv_All_Data.insert(
                    "",
                    "end",
                    iid=nb,
                    values=row,
                    tags=("oddrow",),
                )
            nb += 1
        self.tv_All_Data.insert("", "end", values="")

    def ExportData(self):
        def ExportGUI(self):

            # def update_observer_path_folder(*args):
            #     self.path_export = self.VarEntry_path_export.get()

            def h():
                if self.VarRadioInt.get():
                    print(
                        f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.xlsx"
                    )
                else:
                    print(
                        f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.csv"
                    )

            def browse_button():
                pth = filedialog.askdirectory()
                self.VarEntry_path_export.set(pth)

            def CancelExport():
                self.Exportation.destroy()

            def OkExport():
                try:
                    if self.VarEntry_path_export.get():
                        if self.VarEntry_name_file.get():

                            self.path_export = (
                                self.VarEntry_path_export.get()
                                + "/"
                                + self.VarEntry_name_file.get()
                            )
                            try:
                                if self.VarRadioInt.get():
                                    try:
                                        self.data_pre.to_excel(
                                            f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.xlsx",
                                            index=False,
                                        )

                                        self.Exportation.destroy()
                                    except NameError or TypeError or FileNotFoundError:
                                        tk.messagebox.showerror(
                                            "Information", "There is no data to export"
                                        )
                                else:
                                    try:
                                        self.data_pre.to_csv(
                                            f"{self.VarEntry_path_export.get()}/{self.VarEntry_name_file.get()}.csv",
                                            index=False,
                                        )

                                        self.Exportation.destroy()
                                    except NameError or TypeError or FileNotFoundError:
                                        tk.messagebox.showerror(
                                            "Information", "There is no data to export"
                                        )
                            except ValueError & FileNotFoundError:
                                tk.messagebox.showerror(
                                    "Information", "incorrect destination path"
                                )

                            # except FileNotFoundError:
                            #     tk.messagebox.showerror(
                            #         "Information", f"No such file as {self.path_export}.xlsx")
                        else:
                            tk.messagebox.showerror(
                                "Information", "Please give a name to the file"
                            )
                    else:
                        tk.messagebox.showerror(
                            "Information", "Please choose a destination folder"
                        )
                except:
                    tk.messagebox.showerror("Information", "incorrect destination path")

            self.Exportation = tk.Toplevel(self.root)
            self.Exportation.grab_set()
            self.Exportation.title("Previous Data")
            self.Exportation.iconbitmap("media/logo.ico")
            self.Exportation.geometry("500x200+15+15")
            # self.Exportation.config(background="#CCCCCC")
            self.Exportation.resizable(width=False, height=False)

            self.f_ex_1 = tk.Frame(self.Exportation)
            self.f_ex_1.place(relx=0.05, rely=0.1)

            self.btn_path_export = tk.Button(
                self.f_ex_1, text="Browse", width=8, height=1, command=browse_button
            )
            self.btn_path_export.grid(row=0, column=0)

            self.VarEntry_path_export = tk.StringVar()
            # self.VarEntry_path_export.trace('w', update_observer_path_folder)
            self.Entry_path_export = tk.Entry(
                self.f_ex_1,
                textvariable=self.VarEntry_path_export,
                width=60,
                background="#F1F1F1",
            )
            self.Entry_path_export.grid(row=0, column=1, padx=5)

            self.VarRadioInt = tk.IntVar()
            self.RadioBtnCSV = tk.Radiobutton(
                self.Exportation, text="CSV", value=0, variable=self.VarRadioInt
            ).place(relx=0.05, rely=0.35)

            self.RadioBtnExcel = tk.Radiobutton(
                self.Exportation, text="Excel", value=1, variable=self.VarRadioInt
            ).place(relx=0.05, rely=0.45)

            self.lbl_name = tk.Label(self.Exportation, text="Name file :").place(
                relx=0.25, rely=0.4
            )

            self.VarEntry_name_file = tk.StringVar()
            self.Entry_name_file = tk.Entry(
                self.Exportation, width=30, textvariable=self.VarEntry_name_file
            ).place(relx=0.4, rely=0.4)

            self.OkExportBtn = tk.Button(
                self.Exportation,
                text="OK",
                background="#6DA3F4",
                activebackground="#0256CD",
                foreground="white",
                activeforeground="white",
                width=12,
                height=1,
                command=OkExport,
            ).place(relx=0.31, rely=0.8)

            self.CancelExportBtn = tk.Button(
                self.Exportation,
                text="Cancel",
                background="#CCCCCC",
                width=12,
                height=1,
                command=CancelExport,
            ).place(relx=0.50, rely=0.8)

        ExportGUI(self)

    # ------------ Fx : formul
