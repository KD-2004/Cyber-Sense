import psutil
import socket
from tkinter import *
import tkinter as tk
from tkinter import ttk, font
from PIL import ImageTk, Image
from scapy.all import ARP, Ether, srp
import subprocess
import shutil
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import zipfile
thisPage = 1

root = Tk()
root.title("CyberSense ")
root.geometry("1270x720")

root.minsize(1270, 720)
root.maxsize(1270, 720)
root.configure(bg="#131314")

# Colors
backgroundColor = "#131314"
not_active_color = "#606060"
active_color = "#DCDCDD"
box_background = "#26262C"

def backup_system():
    source_dirs = []

    # Open a dialog to let the user select directories one by one
    while True:
        dir_selected = filedialog.askdirectory(title="Select a Directory to Back Up")
        if dir_selected:
            source_dirs.append(dir_selected)
        else:
            break  # Exit the loop if no directory is selected

    if not source_dirs:
        messagebox.showinfo("Backup", "No directories selected. Backup canceled.")
        return

    # Define backup directory and timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.expanduser("~/backup_root")
    backup_zip = os.path.join(backup_dir, f"backup_{timestamp}.zip")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Create a ZIP file for backup
    with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for src_dir in source_dirs:
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, src_dir)
                    zipf.write(file_path, arcname=os.path.join(os.path.basename(src_dir), arcname))

    messagebox.showinfo("Backup", f"Backup completed successfully!\nBackup saved to: {backup_zip}")

# Update the backup button to call the backup_system function
def on_backup_button_click():
    backup_system()

def update_label(label):
    cpu_usage = psutil.cpu_percent(interval=0.1)
    ram_usage = psutil.virtual_memory().percent
    info_text = f"CPU Usage: {cpu_usage}%\nRAM Usage: {ram_usage}%"
    label.config(text=info_text)
    root.after(300, lambda: update_label(label))

def hoverMenuButtons(event, i):
    global buttonsMain
    buttonsMain[i].config(font=("Lucida Sans", 16, "bold"), bg=backgroundColor, fg="#DEDEE0", activeforeground="#5A5A5B")
    if i == 0:
        buttonsMain[i].place(relx=0.05, rely=0.4)
    elif i == 1:
        buttonsMain[i].place(relx=0.064, rely=0.44)
    elif i == 2:
        buttonsMain[i].place(relx=0.065, rely=0.49)
    elif i == 3:
        buttonsMain[i].place(relx=0.069, rely=0.54)
    elif i == 4:
        buttonsMain[i].place(relx=0.063, rely=0.58)

def leaveMenuButtons(event, i):
    global buttonsMain
    buttonsMain[i].config(font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor)
    if i == 0:
        buttonsMain[i].place(relx=0.07, rely=0.4)
    elif i == 1:
        buttonsMain[i].place(relx=0.075, rely=0.45)
    elif i == 2:
        buttonsMain[i].place(relx=0.075, rely=0.50)
    elif i == 3:
        buttonsMain[i].place(relx=0.078, rely=0.55)
    elif i == 4:
        buttonsMain[i].place(relx=0.074, rely=0.595)

def nextPage(i):
    if i == 0 and thisPage != 1:
        root.destroy()
        import page1
    elif i == 1 and thisPage != 2:
        root.destroy()
        import page2
    elif i == 2 and thisPage != 3:
        root.destroy()
        import page3
    elif i == 3 and thisPage != 4:
        root.destroy()
        import page4
    elif i == 4 and thisPage != 5:
        root.destroy()
        import page5


def show_open_ports():
    open_ports = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'LISTEN':
            port = conn.laddr.port
            try:
                # Resolve the service name for the port number
                service = socket.getservbyport(port)
            except OSError:
                # If the service name cannot be resolved, use "Unknown"
                service = "Unknown"
            open_ports.append((port, service))
    
    # Create a new window to show open ports
    ports_window = Toplevel(root)
    ports_window.title("Open Ports")
    ports_window.geometry("400x300")
    ports_window.configure(bg="#131314")

    ports_label = Label(ports_window, text="Open Ports and Services:", font=('Lucida Sans', 12, 'bold'), bg="#131314", fg=active_color)
    ports_label.pack(pady=10)

    ports_list = Listbox(ports_window, bg="#26262C", fg=active_color, font=('Lucida Sans', 10))
    ports_list.pack(fill=BOTH, expand=True, padx=10, pady=10)

    for port, service in open_ports:
        ports_list.insert(END, f"Port {port}: {service}")

def scan_network():
    devices = []

    # The 'arp -a' command lists all IP and MAC addresses on the local network
    result = subprocess.run(['arp', '-a'], capture_output=True, text=True)

    for line in result.stdout.splitlines():
        if 'dynamic' in line or 'static' in line:
            parts = line.split()
            devices.append({'ip': parts[0], 'mac': parts[1]})

    # Create a new window to show connected devices
    devices_window = Toplevel(root)
    devices_window.title("Connected Devices")
    devices_window.geometry("400x300")
    devices_window.configure(bg="#131314")

    devices_label = Label(devices_window, text="Connected Devices:", font=('Lucida Sans', 12, 'bold'), bg="#131314", fg=active_color)
    devices_label.pack(pady=10)

    devices_list = Listbox(devices_window, bg="#26262C", fg=active_color, font=('Lucida Sans', 10))
    devices_list.pack(fill='both', expand=True, padx=10, pady=10)

    for device in devices:
        devices_list.insert('end', f"IP: {device['ip']} - MAC: {device['mac']}")

# Create the Network Monitor label (this is labelTiny2)
labelTiny2 = Label(root, text="Network Monitor", bg="#131314", fg=active_color)
labelTiny2.place(rely=0.82, relx=0.8, anchor="center")

# Bind the click event to the scan_network function
labelTiny2.bind("<Button-1>", lambda event: scan_network())

image_frame = ImageTk.PhotoImage(Image.open("1x/Panel.png"))
main_frame = tk.Frame(root, bg="black")
main_frame.pack(side=tk.LEFT, fill=tk.Y)
main_frame.pack_propagate(FALSE)
main_frame.configure(width=275, height=720)

label = Label(main_frame, image=image_frame, borderwidth=0)
label.pack()

imgAnti = ImageTk.PhotoImage(Image.open("1x/AntiPanel.png"))
canvas = Canvas(root, bg="#131314", highlightthickness=0)
labelAnti = Label(root, fg="white", image=imgAnti, borderwidth=0)
labelAnti.pack(pady=20)

textAnit = Label(root, text="No active threats\n found", font=('Lucida Sans', 27, 'bold'), bg="#001C24", fg="white", justify="left")
textAnit.place(relx=0.72, rely=0.2, anchor="center")

C = Canvas(root, bg="#131314", width=992, height=512.5, highlightthickness=0)
C.place(rely=0.77, relx=0.61, anchor="center")

boxImage = ImageTk.PhotoImage(Image.open("1x/box.png"))
labelBox = Label(root, bg="#131314", image=boxImage, borderwidth=0)
labelBox.place(rely=0.52, relx=0.409, anchor="center")

labelBox2 = Label(root, bg="#131314", image=boxImage, borderwidth=0)
labelBox2.place(rely=0.52, relx=0.6, anchor="center")

labelBox3 = Label(root, bg="#131314", image=boxImage, borderwidth=0)
labelBox3.place(rely=0.52, relx=0.8, anchor="center")

bigBoxImage = ImageTk.PhotoImage(Image.open("1x/bigBox.png"))
labelBig = Label(root, bg="#131314", image=bigBoxImage, borderwidth=0)
labelBig.place(rely=0.77, relx=0.502, anchor="center")

text_big = Label(root, text="CyberSense", bg=backgroundColor, fg=active_color, borderwidth=0, font=("Lucida Sans", 14, "bold"))
text_big.place(relx=.33, rely=0.65)

desc_big = Label(root, text="A cloud database that contains information about the reputation of files,\nweb resources, and software", bg=backgroundColor, fg=active_color, borderwidth=0, font=("Lucida Sans", 8), justify=LEFT)
desc_big.place(relx=.33, rely=0.69)

tinyImage = ImageTk.PhotoImage(Image.open("1x/boxTiny.png"))
labelTiny = Label(root, bg="#131314", image=tinyImage, borderwidth=0)
labelTiny.place(rely=0.69, relx=0.8, anchor="center")

# Make the Application Activity Monitor clickable
labelTiny.bind("<Button-1>", lambda event: show_open_ports())

text_tiny = Label(root, text="Application Activity\nMonitor", bg="#131314", fg=active_color, borderwidth=0, justify=LEFT, font=("Lucida Sans", 9, "bold"))
text_tiny.place(relx=0.72, rely=0.66)

app_img = ImageTk.PhotoImage(Image.open("1x/icon4.png"))
Label(root, image=app_img, bg=backgroundColor).place(relx=0.848, rely=0.658)

labelTiny2 = Label(root, bg="#131314", image=tinyImage, borderwidth=0)
labelTiny2.place(rely=0.82, relx=0.8, anchor="center")

# Make the Network Monitor clickable
labelTiny2.bind("<Button-1>", lambda event: scan_network())

text_tiny2 = Label(root, text="Network Monitor", bg="#131314", fg=active_color, borderwidth=0, justify=LEFT, font=("Lucida Sans", 9, "bold"))
text_tiny2.place(relx=0.72, rely=0.8)

net_img = ImageTk.PhotoImage(Image.open("1x/icon5.png"))
Label(root, image=net_img, bg=backgroundColor).place(relx=0.848, rely=0.787)

text_Info = Label(root, text="Reports", bg=box_background, fg=active_color, font=("Lucida Sans", 11, "bold"))
text_Info.place(relx=0.34, rely=0.46)

report_img = ImageTk.PhotoImage(Image.open("1x/icon1.png"))
Label(root, image=report_img, bg=box_background).place(relx=0.458, rely=0.45)

info_label = Label(root, bg=box_background, fg="#989899", font=("Lucida Sans", 11, "bold"), justify=LEFT)
info_label.place(relx=0.35, rely=0.517)

update_label(info_label)

button_Info2 = Button(root, bg=box_background, fg=active_color, font=("Lucida Sans", 11, "bold"), activebackground=box_background, borderwidth=0, activeforeground=active_color, padx=97, pady=45, command=backup_system)
button_Info2.place(relx=0.52, rely=0.443)

backup_img = ImageTk.PhotoImage(Image.open("1x/icon2.png"))
Label(root, image=backup_img, bg=box_background).place(relx=0.65, rely=0.45)

text_Info2 = Label(root, text="Backup", fg=active_color, font=("Lucida Sans", 11, "bold"), bg=box_background)
text_Info2.place(relx=0.53, rely=0.463)

button_Info3 = Button(root, bg=box_background, borderwidth=0, fg=active_color, font=("Lucida Sans", 11, "bold"), activebackground=box_background, activeforeground=active_color, padx=97, pady=45)
button_Info3.place(relx=0.72, rely=0.443)

text_Info3 = Label(root, text="Threat detection\ntechnologies", fg=active_color, font=("Lucida Sans", 12, "bold"), bg=box_background, justify=LEFT)
text_Info3.place(relx=0.726, rely=0.463)

threat_img = ImageTk.PhotoImage(Image.open("1x/icon3.png"))
Label(root, image=threat_img, bg=box_background).place(relx=0.848, rely=0.45)

nameAnti = Label(root, text="CyberSense", font=('Century Gothic', 30, "bold"), bg=backgroundColor, fg=active_color, pady=0, padx=0)
nameAnti.place(relx=0.02, rely=0.08)

desAnti = Label(root, text=" Security", font=('Century Gothic', 13), bg=backgroundColor, fg="#5A5A5B", pady=0, padx=0)
desAnti.place(relx=0.02, rely=0.155)

buttonsMain = ["button_monitoring", "button_security", "button_update", "button_task", "button_license"]

buttonsMain[0] = Button(root, text="Monitoring", font=("Lucida Sans", 12, "bold"), fg=active_color, bg=backgroundColor, activebackground=backgroundColor, highlightthickness=0, borderwidth=0, command=lambda: nextPage(0))
buttonsMain[0].place(relx=0.07, rely=0.4)

buttonsMain[1] = Button(root, text="Security", font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor, activebackground=backgroundColor, highlightthickness=0, borderwidth=0, command=lambda: nextPage(1))
buttonsMain[1].place(relx=0.075, rely=0.45)

buttonsMain[2] = Button(root, text="Update", font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor, activebackground=backgroundColor, highlightthickness=0, borderwidth=0, command=lambda: nextPage(2))
buttonsMain[2].place(relx=0.075, rely=0.50)

buttonsMain[3] = Button(root, text="Tasks", font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor, activebackground=backgroundColor, highlightthickness=0, borderwidth=0, command=lambda: nextPage(3))
buttonsMain[3].place(relx=0.078, rely=0.55)

buttonsMain[4] = Button(root, text="License", font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor, activebackground=backgroundColor, highlightthickness=0, borderwidth=0, command=lambda: nextPage(4))
buttonsMain[4].place(relx=0.074, rely=0.595)

buttonsMain[0].bind("<Enter>", lambda event, i=0: hoverMenuButtons(event, i))
buttonsMain[0].bind("<Leave>", lambda event, i=0: leaveMenuButtons(event, i))

buttonsMain[1].bind("<Enter>", lambda event, i=1: hoverMenuButtons(event, i))
buttonsMain[1].bind("<Leave>", lambda event, i=1: leaveMenuButtons(event, i))

buttonsMain[2].bind("<Enter>", lambda event, i=2: hoverMenuButtons(event, i))
   
buttonsMain[3].bind("<Enter>", lambda event, i=3: hoverMenuButtons(event, i))
buttonsMain[3].bind("<Leave>", lambda event, i=3: leaveMenuButtons(event, i))

buttonsMain[4].bind("<Enter>", lambda event, i=4: hoverMenuButtons(event, i))
buttonsMain[4].bind("<Leave>", lambda event, i=4: leaveMenuButtons(event, i))

root.mainloop()
