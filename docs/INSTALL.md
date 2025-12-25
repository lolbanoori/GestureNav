# **GestureNav Installation Guide**
> **Setup & Troubleshooting**

<div align="center">
  <h1>Getting Started</h1>
</div>

**GestureNav** uses a **Split Architecture**:
1.  **The Server (External):** A program that watches your hand.
2.  **The Client (Internal):** The Blender Add-on that moves your camera.

**CRITICAL:** You must set up **both** parts.

---

## **Part 1: Setting up the Vision Server**

This runs outside of Blender to keep your 3D viewport fast.

### 1. Prerequisite: Python
You need Python **3.10** or **3.11** installed.
*   **Check version:** `python --version`
*   **Download:** [python.org](https://www.python.org/downloads/)
    *   *Note: Check "Add Python to PATH" during installation.*

### 2. Start the Server (One-Click Setup)
Since you are on Windows, we have a smart launcher for you!

1.  **Double-click** `start_server.bat` in the GestureNav folder.
2.  It will automatically:
    *   Check for Python.
    *   **Install necessary libraries** (MediaPipe, OpenCV, etc.) if missing.
    *   **Download the AI Model** if missing.
    *   Start the Vision Engine.

*   *Note: If you are on Linux/Mac, or prefer manual control, run `pip install -r requirements.txt` and `python server/main.py` manually.*

---

## **Part 2: Setting up the Blender Client**

We install this just like any other Blender Add-on.

### 1. Prepare the File
1.  Zip the `client` folder (Right-click `client` -> Send to -> Compressed (zipped) folder).
2.  Rename it to `GestureNav_Client.zip`.

### 2. Install in Blender
1.  Open Blender (3.0+).
2.  Go to **Edit > Preferences**.
3.  Click the **Add-ons** tab.
4.  Click **Install...** (top right).
5.  Select your `GestureNav_Client.zip`.
6.  Check the box next to **GestureNav Client** to enable it.
*Or you can simply drag and drop the `GestureNav_Client.zip` file into Blender.*

> **For Developers:**
> You can also open `client/__init__.py` in the **Scripting Workspace** and click Run Script to load it temporarily for editing.

---

## **Part 3: First Run**

1.  In the 3D Viewport, press **N** to open the Sidebar.
2.  Click the **GestureNav** tab.
3.  Click **Start Listener**.
4.  Raise your hand. You should see the Green Circle in the server window react!

---

## **Part 4: Troubleshooting**

### **Issue: "ModuleNotFoundError: No module named 'mediapipe'"**
This means you installed the libraries in a different Python environment than the one `start_server.bat` is using.
*   **Fix:** Try `python -m pip install -r requirements.txt`.

### **Issue: "ERROR: Model file not found"**
You skipped **Step 3** in Part 1.
*   **Fix:** Run `python server/download_model.py`.

### **Issue: Blender isn't moving**
1.  Is the Server running? (Black window open?)
2.  Did you click "Start Listener" in Blender?
3.  **Firewall:** Windows Defender might block the connection. Allow `python.exe` through the firewall.

### **Dual-PC Setup (Advanced)**
To run the server on a laptop and control a desktop:
1.  **Server:** Edit `main.py` -> Set `UDP_IP = "0.0.0.0"`.
2.  **Client:** Edit `__init__.py` -> Set IP to the Laptop's IP address (e.g., `192.168.1.50`).