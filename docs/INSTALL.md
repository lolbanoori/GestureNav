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

### 1. Prerequisite: Python (Manual)
Since this is a Python program, you must have the interpreter installed.
*   **Download:** [python.org/downloads](https://www.python.org/downloads/)
*   **Version:** Python 3.10 or 3.11.
*   **Important:** Check or Tick **"Add Python to PATH"** during installation.

### 2. Start the Server (One-Click)
We have bundled a smart launcher that handles the rest.
1.  Open the `GestureNav` folder.
2.  Double-click `start_server.bat`.

**What it does automatically:**
*   Checks if Python is available.
*   Installs required libraries (`mediapipe`, `opencv-python`, etc).
*   Downloads the AI Model (`hand_landmarker.task`) if missing.
*   Launches the webcam window.

*(To close it safely later, simply click the **X** or press **Q**)*.

---

## **Part 2: Setting up the Blender Client**

### 1. Get the Add-on
*   **Option A (Recommended):** Download the latest `GestureNav_Client.zip` from [GitHub Releases](https://github.com/lolbanoori/GestureNav/releases).
*   **Option B (Manual):** Zip the `client` folder inside this repository and name it `GestureNav_Client.zip`.

### 2. Install in Blender
1.  Open Blender (3.0+).
2.  Simply **Drag and Drop** the zip file into the 3D Viewport.
3.  Click **OK** if prompted.

<br>

_Or you can:_
*1.  Go to **Edit > Preferences > Add-ons**.*
*2.  Click **Install...** (top right).*
*3.  Select your zip file.*
*4.  Check the box next to **GestureNav Client** to enable it.*

> **For Developers:** You can still link `client/__init__.py` in the Scripting Workspace for live editing.

---

## **Part 3: First Run**

1.  In the 3D Viewport, press **N** to open the Sidebar.
2.  Click the **GestureNav** tab.
3.  Click **Start Listener**.
4.  Raise your hand. You should see your **Hand Skeleton** being tracked and the cursor moving relative to the **Green Deadzone Circle**.

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