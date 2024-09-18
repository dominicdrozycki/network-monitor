# Network Monitoring Tool

![Python Version](https://img.shields.io/badge/Python-3.x-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A simple Python-based network monitoring tool that tracks upload and download speeds in real time using a graphical user interface (GUI).

---

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Features
- Real-time network upload and download speed tracking
- Simple and clean GUI built with `tkinter`
- Optional logging of network activity to a file
- Customizable thresholds for alerts

---

## Requirements
- Python 3.x
- `psutil` (for network monitoring)
- `tkinter` (for GUI)

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/dominicdrozycki/network-monitor.git
    ```
2. Navigate to the project directory:
    ```bash
    cd network-monitor/src
    ```
3. Install the required dependencies:
    ```bash
    pip install -r ../requirements.txt
    ```

---

## Usage

To run the network monitoring tool, use the following command:
```bash
python main.py
