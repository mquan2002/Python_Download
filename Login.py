import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3


def login():
    tnd = username_entry.get()
    mk = password_entry.get()
    

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (tnd, mk))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        root.destroy()  
        subprocess.run(["python", "Download.py"]) 
    else:
        messagebox.showerror("Error", "Tài khoản hoặc mật khẩu không đúng")

def register_form():
    root.destroy()
    subprocess.run("python","register.py")



root = tk.Tk()
root.title("Ứng dụng tải video - Đăng nhập")

username_lable =  tk.Label(root,text="Tên Đăng Nhập: ")
username_lable.grid(row=0, column=0, padx=10, pady=10)

username_entry = tk.Entry(root, width=50)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_lable =  tk.Label(root,text="Mật Khẩu: ")
password_lable.grid(row=1, column=0, padx=10, pady=10)

password_entry = tk.Entry(root, width=50)
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_btn= tk.Button(root,text="Đăng nhập",command=login)
login_btn.grid(row=2,column=1, padx=10, pady=10,)

register_btn= tk.Button(root,text="Đăng ký",command=register_form)
register_btn.grid(row=2,column=0, padx=10, pady=10 )

root.mainloop()