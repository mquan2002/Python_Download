import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pytube import YouTube, Playlist
from PIL import Image, ImageTk
import requests
from io import BytesIO

root = tk.Tk()
root.title("Ứng dụng tải video từ YouTube")

playlist = None
default_resolution = '360p'
is_playlist = False 


def fetch_resolutions(url):
    try:
        yt = YouTube(url)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')
        resolutions = list(set([stream.resolution for stream in streams]))
        return sorted(resolutions, reverse=True)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
        return []


def fetch_video_info(url):
    try:
        yt = YouTube(url)
        views = yt.views
        publish_date = yt.publish_date
        channel = yt.author
        thumbnail_url = yt.thumbnail_url

       
        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((200, 150))  
        img = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=img)
        thumbnail_label.image = img

        info_text = f"""
Lượt xem: {views}
Ngày đăng: {publish_date.strftime('%Y-%m-%d')}
Kênh: {channel}
"""
        video_info_label.config(text=info_text)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi lấy thông tin video: {e}")

# Hàm cập nhật các độ phân giải có sẵn của video
def update_resolutions(*args):
    url = url_entry.get()
    if url:
        resolutions = fetch_resolutions(url)
        resolution_combo['values'] = resolutions
        if resolutions:
            resolution_combo.current(0)
        else:
            resolution_combo.set('')

# Hàm cập nhật thông tin của video
def update_video_info(video):
    try:
        views = video.views
        publish_date = video.publish_date
        channel = video.author
        thumbnail_url = video.thumbnail_url

        # Tải hình ảnh thumbnail
        response = requests.get(thumbnail_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((200, 150))  # Điều chỉnh kích thước của hình ảnh
        img = ImageTk.PhotoImage(img)
        thumbnail_label.config(image=img)
        thumbnail_label.image = img

        info_text = f"""
Lượt xem: {views}
Ngày đăng: {publish_date.strftime('%Y-%m-%d')}
Kênh: {channel}
"""
        video_info_label.config(text=info_text)
        stream = video.streams.filter(progressive=True, file_extension='mp4').first()
        resolution_label.config(text=f"Độ phân giải: {stream.resolution if stream else 'Không có độ phân giải phù hợp'}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi cập nhật thông tin video: {e}")

# Hàm chọn video tiếp theo trong playlist
def next_video():
    current_index = playlist_combo.current()
    if current_index is not None and current_index < len(playlist_combo['values']) - 1:
        playlist_combo.current(current_index + 1)
        if playlist:
            update_video_info(playlist.videos[current_index + 1])
        else:
            update_playlist_info(url_entry.get())

# Hàm chọn video trước đó trong playlist
def prev_video():
    current_index = playlist_combo.current()
    if current_index is not None and current_index > 0:
        playlist_combo.current(current_index - 1)
        if playlist:
            update_video_info(playlist.videos[current_index - 1])
        else:
            update_playlist_info(url_entry.get())

# Hàm cập nhật thông tin video và các độ phân giải
def update_info_and_resolutions():
    global is_playlist
    url = url_entry.get()
    if url:
        if 'playlist' in url:
            is_playlist = True
            update_playlist_info(url)
            resolution_combo.config(state='disabled')  # Khóa khung chọn độ phân giải
            resolution_label.grid_remove()  # Ẩn nhãn độ phân giải
        else:
            is_playlist = False
            resolution_combo.config(state='readonly')  # Mở khóa khung chọn độ phân giải
            resolution_label.grid()  # Hiện nhãn độ phân giải
            prev_button.grid_remove()
            fetch_video_info(url)
            update_resolutions()

# Hàm cập nhật thông tin của playlist
def update_playlist_info(url):
    try:
        global playlist
        playlist = Playlist(url)
        if not playlist.videos:
            messagebox.showwarning("Cảnh báo", "Danh sách phát không có video nào.")
            return
        playlist_titles = [video.title for video in playlist.videos]
        playlist_combo['values'] = playlist_titles
        playlist_combo.current(0)
        update_video_info(playlist.videos[0])
        return playlist  # Trả về playlist để sử dụng sau này
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi cập nhật thông tin playlist: {e}")

# Hàm tải video từ YouTube
def download_video():
    url = url_entry.get()
    output_path = output_label.cget("text")
    if is_playlist:
        download_playlist(url, output_path, default_resolution)
    else:
        resolution = resolution_combo.get() if resolution_combo.get() else default_resolution
        download_youtube_video(url, output_path, resolution)

# Hàm tải video từ YouTube
def download_youtube_video(url, output_path, resolution=None):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, res=resolution).first()
        if not stream:
            stream = yt.streams.filter(progressive=True).first()
        stream.download(output_path)
        messagebox.showinfo("Thông báo", "Tải video từ YouTube thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

# Hàm tải danh sách phát từ YouTube
def download_playlist(url, output_path, resolution=None):
    try:
        playlist = Playlist(url)
        for video in playlist.videos:
            stream = video.streams.filter(progressive=True, res=resolution).first()
            if not stream:
                stream = video.streams.filter(progressive=True).first()
            stream.download(output_path)
        messagebox.showinfo("Thông báo", "Tải danh sách phát từ YouTube thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

# Hàm chọn thư mục lưu video
def browse_output_path():
    directory = filedialog.askdirectory()
    if directory:
        output_label.config(text=directory)
        
        
def download_selected_video():
    try:
        global playlist
        selected_index = playlist_combo.current()
        if selected_index is not None:
            video = playlist.videos[selected_index]
            output_path = output_label.cget("text")
            resolution = resolution_combo.get() if resolution_combo.get() else default_resolution
            download_youtube_video(video.watch_url, output_path, resolution)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
        
# Hàm tải toàn bộ playlist
def download_whole_playlist():
    url = url_entry.get()
    output_path = output_label.cget("text")
    if not url:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập URL playlist!")
        return
    if output_path == "Chưa chọn thư mục":
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục lưu trữ!")
        return
    try:
        global playlist
        playlist = Playlist(url)
        for video in playlist.videos:
            stream = video.streams.filter(progressive=True).first()
            if stream:
                stream.download(output_path)
        messagebox.showinfo("Thông báo", "Tải toàn bộ playlist thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")


url_label = tk.Label(root, text="Nhập URL video:")
url_label.grid(row=0, column=0, padx=10, pady=10)

# Khung nhập URL video
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)
url_entry.bind("<FocusOut>", lambda e: update_info_and_resolutions())

# Nút chọn thư mục lưu video
output_button = tk.Button(root, text="Chọn thư mục lưu video", command=browse_output_path)
output_button.grid(row=1, column=0, padx=10, pady=10)

# Nhãn hiển thị đường dẫn thư mục lưu video
output_label = tk.Label(root, text="Chưa chọn thư mục")
output_label.grid(row=1, column=1, padx=10, pady=10)

# Nhãn hiển thị hình ảnh thumbnail và thông tin video
thumbnail_label = tk.Label(root)
thumbnail_label.grid(row=2, column=0, padx=10, pady=10, rowspan=3)

# Nút Tiến
next_button = tk.Button(root, text="Tiến", command=next_video)
next_button.grid(row=8, column=0, padx=10, pady=10)

# Nút Lùi
prev_button = tk.Button(root, text="Lùi", command=prev_video)
prev_button.grid(row=8, column=1, padx=10, pady=10)

# Nhãn hiển thị thông tin video
video_info_label = tk.Label(root, text="", justify=tk.LEFT, anchor="w")
video_info_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Nhãn hiển thị độ phân giải video
resolution_label = tk.Label(root, text="")
resolution_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")
resolution_label.grid_remove()  # Ẩn mặc định

# Nút tải video
download_button = tk.Button(root, text="Tải video", command=download_video)
download_button.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

download_selected_button = tk.Button(root, text="Tải video từ playlist", command=download_selected_video)
download_selected_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

download_whole_playlist_button = tk.Button(root, text="Tải toàn bộ playlist", command=download_whole_playlist)
download_whole_playlist_button.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Combobox chọn video trong playlist
playlist_combo = ttk.Combobox(root, state='readonly')
playlist_combo.grid(row=3, column=1, padx=10, pady=10)

# Combobox chọn độ phân giải
tk.Label(root, text="Độ phân giải:").grid(row=5, column=0)
resolution_combo = ttk.Combobox(root, state='readonly')
resolution_combo.grid(row=5, column=1, padx=10, pady=10)

# Thanh tiến trình tải
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate', variable=progress_var)
progress_bar.grid(row=6, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()
