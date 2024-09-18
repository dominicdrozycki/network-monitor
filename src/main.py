import psutil
import time
import logging
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import pystray
from PIL import Image, ImageDraw
from datetime import datetime

# Initialize default thresholds for upload and download speeds (in Mbps)
UPLOAD_THRESHOLD = 200  # 200 Mbps
DOWNLOAD_THRESHOLD = 200

# Data lists for plotting
upload_data = []
download_data = []
time_data = []

# Initialize previous sent and received data
prev_sent = 0
prev_recv = 0

# Initialize variables for additional statistics
total_uploaded = 0
total_downloaded = 0
max_upload_speed = 0
max_download_speed = 0

# Average speed tracking
total_time = 0
average_upload_speed = 0
average_download_speed = 0

# Global variable to control logging and network interface selection
logging_enabled = True
selected_interface = None
app_running = True  # Global variable to control app state

# Function to get the current network usage statistics for a specific interface
def get_network_usage():
    global selected_interface
    counters = psutil.net_io_counters(pernic=True)
    if selected_interface in counters:
        iface_counters = counters[selected_interface]
        return iface_counters.bytes_sent, iface_counters.bytes_recv
    return 0, 0  # Default return if no interface is selected

# Function to calculate the upload and download speeds
def calculate_speed(sent, recv, prev_sent, prev_recv):
    upload_speed = (sent - prev_sent) * 8 / 1024 / 1024  # Convert to Mbps
    download_speed = (recv - prev_recv) * 8 / 1024 / 1024  # Convert to Mbps
    return upload_speed, download_speed

# Function to update the GUI and check the current network usage
def update_gui():
    global prev_sent, prev_recv, total_uploaded, total_downloaded
    global max_upload_speed, max_download_speed, total_time
    global average_upload_speed, average_download_speed

    if not app_running:
        return  # Stop updating when the app is minimized

    sent, recv = get_network_usage()
    upload_speed, download_speed = calculate_speed(sent, recv, prev_sent, prev_recv)

    # Update total data transferred
    total_uploaded += upload_speed
    total_downloaded += download_speed

    # Update max speeds
    max_upload_speed = max(max_upload_speed, upload_speed)
    max_download_speed = max(max_download_speed, download_speed)

    # Update average speeds
    total_time += 1  # We update every second
    average_upload_speed = total_uploaded / total_time
    average_download_speed = total_downloaded / total_time

    # Update GUI Labels for speeds
    upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
    download_label.config(text=f"Download Speed: {download_speed:.2f} Mbps")

    # Update GUI Labels for additional statistics
    total_uploaded_mb = total_uploaded
    total_downloaded_mb = total_downloaded
    total_data_label.config(text=f"Total Uploaded: {total_uploaded_mb:.2f} MB\n"
                                 f"Total Downloaded: {total_downloaded_mb:.2f} MB")
    avg_speed_label.config(text=f"Average Upload: {average_upload_speed:.2f} Mbps\n"
                                f"Average Download: {average_download_speed:.2f} Mbps")
    max_speed_label.config(text=f"Max Upload: {max_upload_speed:.2f} Mbps\n"
                                f"Max Download: {max_download_speed:.2f} Mbps")

    # Log network data if logging is enabled
    if logging_enabled:
        logging.info(f"Upload: {upload_speed:.2f} Mbps, Download: {download_speed:.2f} Mbps")

    # Display a warning if upload or download speed exceeds the threshold
    if upload_speed > UPLOAD_THRESHOLD:
        messagebox.showwarning("Alert", "Upload speed exceeded threshold!")
    if download_speed > DOWNLOAD_THRESHOLD:
        messagebox.showwarning("Alert", "Download speed exceeded threshold!")

    # Update the previous sent and received values
    prev_sent = sent
    prev_recv = recv

    # Append data for graphing
    upload_data.append(upload_speed)
    download_data.append(download_speed)
    time_data.append(datetime.now().strftime("%H:%M:%S"))

    # Call this function again after 1000 ms (1 second)
    root.after(1000, update_gui)

# Function to update the real-time graph
def update_graph(frame):
    plt.cla()  # Clear the current axes
    plt.plot(time_data[-60:], upload_data[-60:], label='Upload Speed (Mbps)')
    plt.plot(time_data[-60:], download_data[-60:], label='Download Speed (Mbps)')
    plt.xlabel('Time (H:M:S)')
    plt.ylabel('Speed (Mbps)')
    plt.title('Real-Time Network Speed')
    plt.legend()

# Function to apply custom thresholds from the GUI input fields
def apply_thresholds():
    global UPLOAD_THRESHOLD, DOWNLOAD_THRESHOLD
    try:
        # Convert input from Mbps
        UPLOAD_THRESHOLD = int(upload_threshold_entry.get())
        DOWNLOAD_THRESHOLD = int(download_threshold_entry.get())
        messagebox.showinfo("Success", "Thresholds updated successfully!")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for thresholds!")

# Function to toggle logging on or off
def toggle_logging():
    global logging_enabled
    logging_enabled = logging_var.get()
    if logging_enabled:
        messagebox.showinfo("Logging", "Logging enabled")
    else:
        messagebox.showinfo("Logging", "Logging disabled")

# Function to update the selected network interface from the dropdown
def update_interface_selection(event):
    global selected_interface
    selected_interface = interface_var.get()
    messagebox.showinfo("Network Interface", f"Selected interface: {selected_interface}")

# Create a system tray icon
def create_image():
    # Create an image with a red circle for the tray icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    draw.ellipse((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill='red')
    return image

# Function to minimize both the main window and the graph
def hide_window(icon, item):
    global app_running, graph_window
    app_running = False
    root.withdraw()  # Hide the main window

    if graph_window:
        graph_window.canvas.manager.window.withdraw()  # Hide the graph window

# Function to restore both the main window and the graph window
def show_window(icon, item):
    global app_running, graph_window
    app_running = True
    root.deiconify()  # Restore the main window
    root.state('normal')  # Ensure it's not minimized

    # Bring the graph window to the front
    if graph_window:
        graph_window.canvas.manager.window.deiconify()  # Show the graph window
        graph_window.canvas.manager.window.raise_()  # Bring it to the front

def quit_app(icon, item):
    icon.stop()
    root.quit()  # Properly stop the application

# Set up the system tray icon with pystray
def setup_tray():
    image = create_image()
    icon = pystray.Icon("network_monitor", image, menu=pystray.Menu(
        pystray.MenuItem("Show", show_window),
        pystray.MenuItem("Quit", quit_app)
    ))
    icon.run()

# Define a global variable to track the graph window
graph_window = None

def plot_graph():
    global graph_window
    fig = plt.figure()
    graph_window = plt.gcf()  # Get a reference to the current figure (graph window)
    ani = FuncAnimation(fig, update_graph, interval=1000)
    plt.show()

# Main program to create the GUI and start monitoring
if __name__ == "__main__":
    # Start the graph in a separate thread to avoid blocking the Tkinter window
    graph_thread = threading.Thread(target=plot_graph)
    graph_thread.start()

    # Get initial network statistics
    prev_sent, prev_recv = get_network_usage()

    # Create the main window
    root = tk.Tk()
    root.title("Network Monitoring Tool")  # Set the window title

    # Create and display the upload speed label
    upload_label = tk.Label(root, text="Upload Speed: Calculating...", font=('Helvetica', 12))
    upload_label.pack(pady=10)

    # Create and display the download speed label
    download_label = tk.Label(root, text="Download Speed: Calculating...", font=('Helvetica', 12))
    download_label.pack(pady=10)

    # Dropdown to select network interface
    tk.Label(root, text="Select Network Interface:", font=('Helvetica', 10)).pack(pady=5)
    interface_var = tk.StringVar(root)
    interfaces = list(psutil.net_if_addrs().keys())  # Get available network interfaces
    interface_dropdown = tk.OptionMenu(root, interface_var, *interfaces, command=update_interface_selection)
    interface_dropdown.pack(pady=5)

    # Input for upload speed threshold
    tk.Label(root, text="Upload Threshold (Mbps):", font=('Helvetica', 10)).pack(pady=5)
    upload_threshold_entry = tk.Entry(root)
    upload_threshold_entry.insert(0, str(UPLOAD_THRESHOLD))  # Set default value in Mbps
    upload_threshold_entry.pack(pady=5)

    # Input for download speed threshold
    tk.Label(root, text="Download Threshold (Mbps):", font=('Helvetica', 10)).pack(pady=5)
    download_threshold_entry = tk.Entry(root)
    download_threshold_entry.insert(0, str(DOWNLOAD_THRESHOLD))  # Set default value in Mbps
    download_threshold_entry.pack(pady=5)

    # Button to apply custom thresholds
    apply_button = tk.Button(root, text="Apply Thresholds", command=apply_thresholds)
    apply_button.pack(pady=10)

    # Checkbox to enable or disable logging
    logging_var = tk.IntVar(value=1)  # 1 = checked by default
    logging_checkbox = tk.Checkbutton(root, text="Enable Logging", variable=logging_var, command=toggle_logging)
    logging_checkbox.pack(pady=10)

    # Label for total data transferred
    total_data_label = tk.Label(root, text="Total Uploaded: 0.00 MB\nTotal Downloaded: 0.00 MB", font=('Helvetica', 10))
    total_data_label.pack(pady=10)

    # Label for average speeds
    avg_speed_label = tk.Label(root, text="Average Upload: 0.00 Mbps\nAverage Download: 0.00 Mbps", font=('Helvetica', 10))
    avg_speed_label.pack(pady=10)

    # Label for max speeds
    max_speed_label = tk.Label(root, text="Max Upload: 0.00 Mbps\nMax Download: 0.00 Mbps", font=('Helvetica', 10))
    max_speed_label.pack(pady=10)

    # Set up the system tray
    tray_thread = threading.Thread(target=setup_tray)
    tray_thread.start()

    # Set up the GUI to update every second
    root.after(1000, update_gui)

    # Start the Tkinter event loop
    root.mainloop()
