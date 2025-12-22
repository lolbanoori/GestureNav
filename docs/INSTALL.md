# **GestureNav**
> **Touchless 3D Navigation for Blender**

<div align="center">
  <h1>Installation & Setup Guide</h1>
</div>

**Welcome to GestureNav.** Before you begin, it is important to understand that GestureNav works differently than standard Blender add-ons. It uses a **Split Architecture**:

1. **The Server (External):** A Python script running in a terminal window that watches your hand.  
2. **The Client (Internal):** The Blender Add-on that moves your camera.

**CRITICAL:** You must set up **both** parts for the system to work.

---

## **Part 1: Setting up the Vision Server (The "Brain")**

This component runs outside of Blender. It uses Google MediaPipe to track your hands and broadcasts the data.

### 1\. Prerequisite: Python

You need a standard installation of Python installed on your computer.

* **Recommended Version:** Python **3.10** or **3.11**.  
  * *Note: Python 3.12+ is not yet fully stable with some computer vision libraries.*  
* **Check your version:** Open your Command Prompt (cmd) or Terminal and type:
```
python \--version
```

* **Download:** If you don't have it, download it from [python.org](https://www.python.org/downloads/).  
  * *Windows Users:* Ensure you check the box **"Add Python to PATH"** during installation.

### 2\. Install Dependencies

Open your terminal, navigate to the ```GestureNav/``` folder, and run the following command to install the necessary libraries (MediaPipe, OpenCV, NumPy):
```
pip install \-r requirements.txt
```

* *If you see an error saying ```pip``` is not recognized, try ```python \-m pip install \-r requirements.txt```* 

### 3\. Test the Server

Before opening Blender, let's make sure the camera works.

1. Navigate to the ```server/``` folder in your terminal.  
2. Run the script:
```
python main.py
```

3. If successful, your webcam light should turn on, and you should see text indicating: ```*Server listening on 127.0.0.1:5555*```

---

## **Part 2: Setting up the Blender Client (The "Body")**

Now we need to teach Blender how to listen to the Server.

1. **Zip the Client Folder:**  
   * Go to your ```GestureNav``` directory.  
   * Right-click the ```client``` folder and choose **Send to \> Compressed (zipped) folder**.  
   * Name it  GestureNav\_Client.zip .  
2. **Install in Blender:**  
   * Open Blender (Version 3.0 or higher).  
   * Go to **Edit \> Preferences**.  
   * Click on the **Add-ons** tab.  
   * Click **Install...** (top right).
   * Select your ```GestureNav\_Client.zip``` file.  
3. **Activate:**  
   * Search for "GestureNav" in the list.  
   * Check the box to enable **3D View: GestureNav Client**.

---

## **Part 3: Configuration & Networking**

### **Default Setup (Localhost)**

By default, GestureNav is configured to run on a single machine.

* **IP:** ```127.0.0.1``` (This means "this computer")  
* **Port:** ```5555```

### **Dual-PC Setup (Advanced)**

If you want to run the Vision Server on a laptop (to save resources) and control Blender on a powerful workstation:

1. **Find the Server's IP:**  
   * On the computer running the webcam (Server), open Command Prompt.  
   * Type ```ipconfig``` (Windows) or ```ifconfig``` (Mac/Linux).  
   * Look for **IPv4 Address**. It usually looks like ```192.168.1.XX```  
2. **Configure the Script:**  
   * Open ```server/main.py```. Change ```UDP\_IP \= "127.0.0.1"```  to ```"0.0.0.0"``` (this allows it to broadcast).  
   * Open ```client/operator\_listen.py```. Change ```UDP\_IP``` to the Server's IPv4 address found in step 1.

---

## **Part 4: Troubleshooting**

### **Issue: "I am moving my hand, but Blender isn't moving."**

**Solution 1: The Safety Clutch** Ensure you have clicked **"Start Listener"** in the GestureNav side panel (N-Panel) in Blender.

**Solution 2: Firewall Blocking (Most Common)** Since GestureNav uses UDP (Network Packets), Windows Defender or 3rd party antiviruses might block the connection, thinking it's a virus trying to access the internet.

#### How to fix Windows Firewall:

1. Press the Windows Key and type **"Allow an app through Windows Firewall"**.  
2. Click **Change Settings** (Requires Admin).  
3. Look for ```python.exe``` (or ```python```).  
4. Ensure both **Private** and **Public** checkboxes are ticked.  
5. Click OK.


### **Issue: "ModuleNotFoundError: No module named 'mediapipe'"**

This means the dependencies were installed in a different Python environment than the one you are running.

* **Fix:** Ensure you are running the server using the same python executable you used for pip. Try ```python \-m pip install mediapipe``` directly.

### **Issue: Lag or Jitter**

* **Fix:** Ensure good lighting. MediaPipe struggles in dark rooms, causing the "skeleton" to jitter, which shakes the camera