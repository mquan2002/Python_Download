import tkinter as tk
from tkinter import messagebox
from facebook_scraper import get_posts
import requests
from pytube import YouTube

def download_facebook_video(url, output_path):
    try:
        for post in get_posts(url, pages=1):
            if post['video']:
                video_url = post['video']
                with open(output_path, 'wb') as f:
                    response = requests.get(video_url)
                    f.write(response.content)
                messagebox.showinfo("Thông báo", "Download video từ Facebook thành công!")
                return
        messagebox.showerror("Lỗi", "Không tìm thấy video trên trang.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

def download_youtube_video(url, output_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path)
        messagebox.showinfo("Thông báo", "Download video từ YouTube thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

def download_video():
    url = url_entry.get()
    output_path = output_entry.get()
    if url == "" or output_path == "":
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập URL video và đường dẫn lưu trữ!")
        return
    if var.get() == 1:
        download_facebook_video(url, output_path)
    elif var.get() == 2:
        download_youtube_video(url, output_path)

# Tạo giao diện
root = tk.Tk()
root.title("Ứng dụng tải video")

url_label = tk.Label(root, text="Nhập URL video:")
url_label.grid(row=0, column=0, padx=10, pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

output_label = tk.Label(root, text="Nhập đường dẫn lưu video:")
output_label.grid(row=1, column=0, padx=10, pady=10)

output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)

var = tk.IntVar()
facebook_radio = tk.Radiobutton(root, text="Facebook", variable=var, value=1)
facebook_radio.grid(row=2, column=0, padx=10, pady=5)

youtube_radio = tk.Radiobutton(root, text="YouTube", variable=var, value=2)
youtube_radio.grid(row=2, column=1, padx=10, pady=5)

download_button = tk.Button(root, text="Tải video", command=download_video)
download_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()