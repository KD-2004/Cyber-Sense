import psutil
from tkinter import *
import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
from PIL import ImageTk, Image
import requests  # You need the 'requests' library for API calls
import os
import time
thisPage = 2

root = Tk()
root.title("Cyber Sense endpoint")
root.geometry("1270x720")

root.minsize(1270,720)
root.maxsize(1270,720)
root.configure(bg="#131314")


# Colors
backgroundColor = "#131314"
not_active_color = "#606060"
active_color = "#DCDCDD"
box_background = "#26262C"


# For the Nav buttons
def hoverMenuButtons(event,i):
    global buttonsMain

    if (i == 0):
        buttonsMain[i].config(font=("Lucida Sans",16,"bold"),bg=backgroundColor, fg="#DEDEE0", activeforeground="#5A5A5B")
        buttonsMain[i].place(relx=0.05,rely=0.4)

    elif (i == 1):
        buttonsMain[i].config(font=("Lucida Sans",16,"bold"),bg=backgroundColor, fg="#DEDEE0", activeforeground="#5A5A5B")
        buttonsMain[i].place(relx=0.064,rely=0.44)
    elif (i == 2):
        buttonsMain[i].config(font=("Lucida Sans",16,"bold"),bg=backgroundColor, fg="#DEDEE0", activeforeground="#5A5A5B")
        buttonsMain[i].place(relx=0.065,rely=0.49)
    elif (i == 3):
        buttonsMain[i].config(font=("Lucida Sans",16,"bold"),bg=backgroundColor, fg="#DEDEE0", activeforeground="#5A5A5B")
        buttonsMain[i].place(relx=0.069,rely=0.54)
    elif (i == 4):
        buttonsMain[i].config(font=("Lucida Sans",16,"bold"),bg=backgroundColor, fg="#DEDEE0", activeforeground="#5A5A5B")
        buttonsMain[i].place(relx=0.063,rely=0.58)


def leaveMenuButtons(event, i):
    global buttonsMain
    if (i == 0):
        root.after(50)
        buttonsMain[i].config(font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor)
        buttonsMain[i].place(relx=0.07, rely=0.4)
    elif (i == 1):
        root.after(50)
        buttonsMain[i].config(font=("Lucida Sans", 12, "bold"), fg=active_color, bg=backgroundColor)
        buttonsMain[i].place(relx=0.075, rely=0.45)
    elif (i == 2):
        root.after(50)
        buttonsMain[i].config(font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor)
        buttonsMain[i].place(relx=0.075, rely=0.50)
    elif (i == 3):
        root.after(50)
        buttonsMain[i].config(font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor)
        buttonsMain[i].place(relx=0.078, rely=0.55)
    elif (i == 4):
        root.after(50)
        buttonsMain[i].config(font=("Lucida Sans", 12), fg=not_active_color, bg=backgroundColor)
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


# New Function: File Scanner
def scanner():
    def update_progress_label(value):
        return f"Current Progress: {value}%"
    
    def progress(value):
        if value <= 100:
            progress_bar['value'] = value
            label.config(text=update_progress_label(value))
            root.after(1000, lambda: progress(value + 10))
        else:
            progress_bar.stop()

    # File Dialog to Select File
    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("Executable files", "*.exe"), ("All files", "*.*"))
        )
        if file_path:
            check_virus(file_path)
        else:
            messagebox.showerror("Error", "No file selected.")
    
    # Check file for viruses using API
    def check_virus(file_path):
        api_key = "b3e1117b497e46edaf24e9a3d0a804fbb1bc93acb76c9120be147863ddcb3616"  # Replace this with your actual VirusTotal API key
        url_scan = "https://www.virustotal.com/vtapi/v2/file/scan"
        url_report = "https://www.virustotal.com/vtapi/v2/file/report"
        
        # Check if file size exceeds the limit (e.g., VirusTotal has a 32MB limit for free API users)
        max_file_size = 32 * 1024 * 1024  # 32MB in bytes
        file_size = os.path.getsize(file_path)

        if file_size > max_file_size:
            messagebox.showerror("Error", f"File size exceeds the 32MB limit. Please choose a smaller file.")
            return
        
        try:
            with open(file_path, 'rb') as file_to_scan:
                files = {'file': file_to_scan}
                params = {'apikey': api_key}

                response = requests.post(url_scan, files=files, params=params)

                if response.status_code == 200:
                    result = response.json()
                    scan_id = result.get('scan_id')
                    messagebox.showinfo("Scan Submitted", f"Scan submitted successfully. Scan ID: {scan_id}")
                    
                    # After successful submission, fetch the report
                    fetch_report(scan_id, api_key)
                else:
                    messagebox.showerror("API Error", f"Failed to scan file. Error code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Function to fetch the scan report
    def fetch_report(scan_id, api_key):
        url_report = "https://www.virustotal.com/vtapi/v2/file/report"
        
        params = {'apikey': api_key, 'resource': scan_id}
        
        try:
            # Polling the API to get the report (wait a few seconds before the first try)
            time.sleep(10)  # Wait for the scan to complete (adjust this as needed)

            while True:
                response = requests.get(url_report, params=params)
                
                if response.status_code == 200:
                    result = response.json()
                    response_code = result.get('response_code')
                    
                    if response_code == 1:  # 1 means the scan report is ready
                        positives = result.get('positives')
                        total = result.get('total')
                        
                        if positives > 0:
                            # Collect detailed information about which engines flagged the file
                            detections = []
                            for scanner, report in result['scans'].items():
                                if report['detected']:
                                    detections.append(f"{scanner}: {report['result']}")
                            
                            detection_info = "\n".join(detections)
                            messagebox.showwarning("Virus Detected", f"The file is flagged as a virus by {positives} out of {total} scanners.\n\nDetails:\n{detection_info}")
                        else:
                            messagebox.showinfo("Scan Result", f"The file is clean according to {total} scanners.")
                        break
                    else:
                        messagebox.showinfo("Pending", "The scan is still being processed. Trying again in 10 seconds...")
                        time.sleep(10)  # Wait and try again in 10 seconds
                else:
                    messagebox.showerror("Error", f"Failed to get scan report. Error code: {response.status_code}")
                    break
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Request Error", f"An error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    # GUI window for scanning
    top = Toplevel()
    top.title("Scanning")
    top.geometry("600x600")
    top.configure(bg="#131314")
    
    progress_bar = ttk.Progressbar(top, orient='horizontal', mode='determinate', length=400)
    progress_bar.place(relx=0.15, rely=0.35)
    
    label = Label(top, text=update_progress_label(0), font=("Lucida Sans", 12), fg=active_color, bg=backgroundColor)
    label.place(relx=0.33, rely=0.4)
    
    select_button = Button(top, text="Select File", fg=active_color, bg=backgroundColor, font=("Lucida Sans", 12), command=select_file)
    select_button.place(relx=0.4, rely=0.45)


image_frame = ImageTk.PhotoImage(Image.open("1x/Panel.png"))
main_frame = tk.Frame(root, bg="black")
main_frame.pack(side=tk.LEFT, fill=tk.Y)
main_frame.pack_propagate(FALSE)
main_frame.configure(width=275, height=720)

label = Label(main_frame, image=image_frame, borderwidth=0)
label.pack()

# SCAN box
img_scan = ImageTk.PhotoImage(Image.open("1x/scan.png"))
button_scan = Button(root, image=img_scan, bg=backgroundColor, width=671, borderwidth=0, height=436, command=scanner, activebackground=backgroundColor)
button_scan.place(relx=0.35, rely=0.16)


# The Name of the Program
nameAnti = Label(
    root,
    text="Cyber Sense",
    font=('Century Gothic', 30, "bold"),
    bg=backgroundColor,
    fg=active_color,
    pady=0,
    padx=0
)

nameAnti.place(
    relx=0.02,
    rely=0.08
)

desAnti = Label(
    root,
    text="Endpoint Security",
    font=('Century Gothic', 13),
    bg=backgroundColor,
    fg="#5A5A5B",
    pady=0,
    padx=0
)

desAnti.place(
    relx=0.02,
    rely=0.155
)


# Nav buttons
buttonsMain = ["button_monitoring", "button_security", "button_update", "button_task", "button_license"]

buttonsMain[0] = Button(
    root,
    text="Monitoring",
    font=("Lucida Sans", 12),
    fg=not_active_color,
    bg=backgroundColor,
    activebackground=backgroundColor,
    highlightthickness=0,
    borderwidth=0,
    command=lambda: nextPage(0)
)

buttonsMain[0].place(
    relx=0.07,
    rely=0.4
)

buttonsMain[1] = Button(
    root,
    text="Security",
    font=("Lucida Sans", 12, "bold"),
    fg=active_color,
    bg=backgroundColor,
    activebackground=backgroundColor,
    highlightthickness=0,
    borderwidth=0,
    command=lambda: nextPage(1)
)

buttonsMain[1].place(
    relx=0.075,
    rely=0.45
)

buttonsMain[2] = Button(
    root,
    text="Update",
    font=("Lucida Sans", 12),
    fg=not_active_color,
    bg=backgroundColor,
    activebackground=backgroundColor,
    highlightthickness=0,
    borderwidth=0,
    command=lambda: nextPage(2)
)

buttonsMain[2].place(
    relx=0.075,
    rely=0.50
)

buttonsMain[3] = Button(
    root,
    text="Tasks",
    font=("Lucida Sans", 12),
    fg=not_active_color,
    bg=backgroundColor,
    activebackground=backgroundColor,
    highlightthickness=0,
    borderwidth=0,
    command=lambda: nextPage(3)
)

buttonsMain[3].place(
    relx=0.078,
    rely=0.55
)

buttonsMain[4] = Button(
    root,
    text="License",
    font=("Lucida Sans", 12),
    fg=not_active_color,
    bg=backgroundColor,
    activebackground=backgroundColor,
    highlightthickness=0,
    borderwidth=0,
    command=lambda: nextPage(4)
)

buttonsMain[4].place(
    relx=0.074,
    rely=0.595
)

buttonsMain[0].bind("<Enter>", lambda event, i=0: hoverMenuButtons(event, i))
buttonsMain[0].bind("<Leave>", lambda event, i=0: leaveMenuButtons(event, i))

buttonsMain[1].bind("<Enter>", lambda event, i=1: hoverMenuButtons(event, i))
buttonsMain[1].bind("<Leave>", lambda event, i=1: leaveMenuButtons(event, i))

buttonsMain[2].bind("<Enter>", lambda event, i=2: hoverMenuButtons(event, i))
buttonsMain[2].bind("<Leave>", lambda event, i=2: leaveMenuButtons(event, i))

buttonsMain[3].bind("<Enter>", lambda event, i=3: hoverMenuButtons(event, i))
buttonsMain[3].bind("<Leave>", lambda event, i=3: leaveMenuButtons(event, i))

buttonsMain[4].bind("<Enter>", lambda event, i=4: hoverMenuButtons(event, i))
buttonsMain[4].bind("<Leave>", lambda event, i=4: leaveMenuButtons(event, i))


root.mainloop()
