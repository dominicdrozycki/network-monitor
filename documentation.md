## **Documentation for Network Monitoring Tool**

---

### **Table of Contents**
1. [Overview](#1-overview)
2. [Project Structure](#2-project-structure)
3. [Features](#3-features)
4. [How It Works](#4-how-it-works)
5. [Customization Options](#5-customization-options)
6. [Graphical User Interface (GUI)](#6-graphical-user-interface-gui)
7. [Logging Functionality](#7-logging-functionality)
8. [System Tray Integration](#8-system-tray-integration)
9. [Contributing Guidelines](#9-contributing-guidelines)
10. [Known Issues and Future Improvements](#10-known-issues-and-future-improvements)

---

### **1. Overview**
The **Network Monitoring Tool** is a Python application designed to track real-time upload and download speeds on the user's network interface. It features a graphical user interface (GUI) created using `tkinter` and supports system tray integration with `pystray`.

---

### **2. Project Structure**
- **src/**: Contains the core source code (`main.py`).
- **README.md**: Provides an introduction, installation instructions, and usage details.
- **requirements.txt**: Specifies the dependencies for the project.
- **LICENSE**: License details for the project.

---

### **3. Features**
- Monitor real-time network upload and download speeds.
- User-defined upload/download thresholds with alerts.
- Simple GUI with real-time updates.
- Logging of network speeds to a file.
- Graphical representation of network speeds using `matplotlib`.
- Minimize the app to the system tray.

---

### **4. How It Works**
The application uses Python’s `psutil` library to fetch network statistics from the system. It periodically checks the amount of data sent and received by the network interface, calculates the speeds, and displays the data in the GUI.

---

### **5. Customization Options**
You can customize the tool by modifying the following options:
- **Upload and Download Thresholds**: Set custom thresholds to get alerts when speeds exceed the limit.
- **Logging**: Enable or disable logging through the checkbox in the GUI. When enabled, network speeds are logged to a file.

---

### **6. Graphical User Interface (GUI)**
The GUI provides real-time feedback on network performance. The key components are:
- **Speed Labels**: Display upload/download speeds in kilobytes per second.
- **Threshold Input**: Fields for users to input custom speed thresholds.
- **Interface Selection**: Dropdown menu for selecting the network interface to monitor.
- **Logging Checkbox**: Option to enable or disable logging.
- **Real-Time Graph**: Graphical plot of network speeds using `matplotlib`.

---

### **7. Logging Functionality**
If logging is enabled, the network speeds are written to `network.log`. The format of the log entries is:
[Timestamp] Upload: [Speed] KB/s, Download: [Speed] KB/s

You can modify the logging behavior in the `main.py` file by changing the logging level or file format.

---

### **8. System Tray Integration**
The application can be minimized to the system tray using the `pystray` library. When minimized, the app runs in the background and can be restored by clicking on the tray icon.

Tray options include:
- **Show**: Restores the application window.
- **Quit**: Exits the application.

---

### **9. Contributing Guidelines**
Contributions are welcome. Here's how you can help improve the tool:
- Report bugs or issues.
- Suggest new features.
- Fork the repository and create a pull request with your improvements.

---

### **10. Known Issues and Future Improvements**
- **Graph Refresh Rate**: The graph updates every second, which may result in performance lag on slower systems. Optimizations can be made to adjust the refresh rate dynamically.
- **Multi-Interface Monitoring**: Currently, the tool monitors only one network interface at a time. Future improvements could include multi-interface monitoring.
- **Dark Mode**: The GUI could be enhanced with a dark mode feature.

