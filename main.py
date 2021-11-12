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
# from PyDataApp import PyData


class Api:
    def __init__(self):
        self.okk = False
        # self.import_path_excel = None
        # self.import_path_csv = None
        # self.import_path_txt = None

    def Load_Path_Excel(self):
        """
        Cette fonction ouvrira l'explorateur de fichiers et 
        affectera le chemin de fichier choisi à label_file
        """
        self.path_filename = filedialog.askopenfilename(initialdir="E:\Total\Station Data\Master data\Data source",
                                                        title="Select A File",
                                                        filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))
        # if self.path_filename[-4:] == ".csv":
        self.import_path_csv = self.path_filename
        # test['text'] = self.path_filename
        # return self.import_path_csv

    def Load_excel_data_1(self, path):
        """Si le fichier sélectionné est valide, cela chargera le fichier"""
        file_path_1 = path
        try:
            excel_filename = r"{}".format(file_path_1)
            if excel_filename[-4:] == ".csv":
                df1 = pd.read_csv(excel_filename)
            else:

                df1 = pd.read_excel(excel_filename)

        except ValueError:
            tk.messagebox.showerror(
                "Information", "The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror(
                "Information", f"No such file as {file_path_1}")
            return None
        return df1

    def preview_data(self, root, path):
        new_interface = tk.Toplevel(root)
        new_interface.grab_set()
        new_interface.title("Previous Data")
        new_interface.iconbitmap('media/logo.ico')
        new_interface.geometry("600x250+15+15")
        new_interface.resizable(width=False, height=False)

        frame1 = tk.LabelFrame(new_interface, text=f"{path}")
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

        OkBtn_data = tk.Button(new_interface, text="Ok", background='#40A497', activeforeground='white', activebackground='#40A497',
                               command=lambda: ok_data).place(relx=0.4, rely=0.85, height=30, width=60)

        Cancel_data = tk.Button(new_interface, text="Cancel", background='#CCCCCC',
                                command=new_interface.destroy).place(relx=0.5, rely=0.85, height=30, width=60)

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
                tv1.heading(column, text=column)

            df_rows = df1.head().to_numpy().tolist()
            for row in df_rows:
                tv1.insert("", "end", values=row)

            return df1

        def clear_data():
            tv1.delete(*tv1.get_children())
            return None

        df = Load_excel_data_1()

        def ok_data(self, tv_All_Data):

            # df = pd.read_excel(path)

            clear_data()
            tv_All_Data["column"] = list(df.columns)
            tv_All_Data["show"] = "headings"
            for column in tv_All_Data["columns"]:
                tv_All_Data.heading(column, text=column)

            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                tv_All_Data.insert("", "end", values=row)
