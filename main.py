if True:
    import tkinter as tk
    from tkinter import PhotoImage
    from PyDataApp import PyData
    
    
splach_root = tk.Tk()
splach_root.overrideredirect(True)

splach_root.update_idletasks()
width = 400
frm_width = splach_root.winfo_rootx() - splach_root.winfo_x()
win_width = width + 2 * frm_width
height = 200
titlebar_height = splach_root.winfo_rooty() - splach_root.winfo_y()
win_height = height + titlebar_height + frm_width
x = splach_root.winfo_screenwidth() // 2 - win_width // 2
y = splach_root.winfo_screenheight() // 2 - win_height // 2
splach_root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
splach_root.deiconify()

splach_logo = PhotoImage(file="media/WML.png")
splach_logo = splach_logo.subsample(2, 2)

# afficher l'icone de progresql
print_img = tk.Label(splach_root, image=splach_logo, width=150, height=150)
print_img.place(relx=0.32, rely=0.04)

splach_label = tk.Label(splach_root, text="Machine Learnia", font=("Helvetica", 18)).place(relx=0.27, rely=0.7)


def main_window():
    splach_root.destroy()
    app = PyData()
    # app.root.mainloop()
    
splach_root.after(5000, main_window)

tk.mainloop()