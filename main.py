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
        pass
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
