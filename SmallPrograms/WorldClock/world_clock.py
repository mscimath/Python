import tkinter as tk
from time import strftime
from pytz import timezone
from datetime import datetime

def update_time():
    # Polish time
    poland_tz = timezone('Europe/Warsaw')
    poland_time = datetime.now(poland_tz).strftime('%H:%M:%S')
    poland_label.config(text=f"Poland: {poland_time}")

    # Japanese time
    japan_tz = timezone('Asia/Tokyo')
    japan_time = datetime.now(japan_tz).strftime('%H:%M:%S')
    japan_label.config(text=f"Japan: {japan_time}")

    # Chinease time
    china_tz =timezone('Asia/Shanghai')
    china_time = datetime.now(china_tz).strftime('%H:%M:%S')
    china_label.config(text=f"China: {china_time}")

    # update every 1000 ms
    root.after(1000, update_time)

root = tk.Tk()
root.title('World Clock')

# Label for Poland
poland_label = tk.Label(root, font=('calibri', 20, 'bold'), background = 'purple', foreground='yellow')
poland_label.pack(anchor='center')

# Label for Japan
japan_label = tk.Label(root, font=('calibri', 20, 'bold'), background = 'yellow', foreground='purple')
japan_label.pack(anchor='center')

# Label for China
china_label = tk.Label(root, font=('calibri', 20, 'bold'), background = 'grey', foreground='violet')
china_label.pack(anchor='center')

# Call the function to update time
update_time()

root.mainloop()
