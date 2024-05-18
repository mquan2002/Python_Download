import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3
import subprocess

def register():
    new_username = username_entry.get()
    new_password = password_entry.get()
        
        # Kết nối tới cơ sở dữ liệu và thêm người dùng mới
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if new_username == "" or new_password =="":
        messagebox.showerror("Error","Tài khoản và mật khẩu không được để trống")
    else:
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (new_username, new_password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
            root.destroy()  # Đóng cửa sổ đăng ký sau khi thành công
            subprocess.run(["python","Login.py"])
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

def login_form():
    root.destroy()
    subprocess.run(["python","Login.py"])

#giao diện

root = tk.Tk()
root.title("Ứng dụng tải video - Đăng ký")


username_lable =  tk.Label(root,text="Tên Đăng Nhập: ")
username_lable.grid(row=0, column=0, padx=10, pady=10)

username_entry = tk.Entry(root, width=50)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_lable =  tk.Label(root,text="Mật Khẩu: ")
password_lable.grid(row=1, column=0, padx=10, pady=10)

password_entry = tk.Entry(root, width=50)
password_entry.grid(row=1, column=1, padx=10, pady=10)


login_btn= tk.Button(root,text="Đăng nhập",command=login_form)
login_btn.grid(row=2,column=0, padx=10, pady=10)

register_btn= tk.Button(root,text="Đăng ký",command=register)
register_btn.grid(row=2,column=1, padx=10, pady=10 )

root.mainloop()