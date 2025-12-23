# **GestureNav Installation Guide**
> **Setup & Troubleshooting**

<div align="center">
  <h1>Getting Started</h1>
</div>

**GestureNav** uses a **Split Architecture**:
1.  **The Server (External):** A Python script that watches your hand.
2.  **The Client (Internal):** The Blender Add-on that moves your camera.

**CRITICAL:** You must set up **both** parts.

---

## **Part 1: Setting up the Vision Server**

This runs outside of Blender to keep your 3D viewport fast.

### 1. Prerequisite: Python
You need Python **3.10** or **3.11** installed.
*   **Check version:** `python --version`
*   **Download:** [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies
Open your terminal in the `GestureNav/` folder:

```bash
# Install MediaPipe, OpenCV, NumPy
pip install -r requirements.txt
```

### 3. Download the AI Model
We need the specialized Hand Tracking model file from Google. Run this helper script:

```bash
python server/download_model.py
```
*   *This will download `hand_landmarker.task` into the `server/` folder.*

### 4. Test the Server
Run the main engine:

```bash
python server/main.py
```
*   Your webcam should turn on.
*   You should see a window with your video feed.
*   **Keep this window open** while using GestureNav.

---

## **Part 2: Setting up the Blender Client**

1.  **Open Blender** (3.0+).
2.  Go to the **Scripting** tab (top menu).
3.  Click **Open** and select `client/__init__.py`.
4.  Click **Run Script** (Play icon).
    *   *(Advanced Users: You can also zip the `client` folder and install it as a standard Add-on).*

---

## **Part 3: First Run**

1.  In the 3D Viewport, press **N** to open the Sidebar.
2.  Click the **GestureNav** tab.
3.  Click **Start Listener**.
4.  Raise your hand. You should see the Green Circle in the server window react!

---

## **Part 4: Troubleshooting**

### **Issue: "ModuleNotFoundError: No module named 'mediapipe'"**
This means you installed the libraries in a different Python environment than the one you are running.
*   **Fix:** Try `python -m pip install -r requirements.txt`.

### **Issue: "ERROR: Model file not found"**
You skipped **Step 3** in Part 1.
*   **Fix:** Run `python server/download_model.py` or manually download `hand_landmarker.task` and place it in the `server/` folder.

### **Issue: Blender isn't moving**
1.  Is the Server running? (Black terminal window open?)
2.  Did you click "Start Listener" in Blender?
3.  **Firewall:** Windows Defender might block the connection. Allow `python.exe` through the firewall.

### **Dual-PC Setup (Advanced)**
To run the server on a laptop and control a desktop:
1.  **Server:** Edit `main.py` -> Set `UDP_IP = "0.0.0.0"`.
2.  **Client:** Edit `__init__.py` -> Set IP to the Laptop's IP address (e.g., `192.168.1.50`).