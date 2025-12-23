# GestureNav
> **Touchless 3D Navigation for Blender**

![GestureNav Hero Image](assets/GestureNav_hero.png)

**GestureNav** is a professional tool that decouples computer vision from Blender's internal loop, allowing users to orbit, pan, and zoom the 3D viewport using hand gestures captured via a standard webcam.

By utilizing the "Puppeteer Pattern," GestureNav runs the heavy computer vision processing in a separate Python environment (Server) and broadcasts lightweight vector data to Blender (Client) via UDP. This ensures your 3D Viewport remains buttery smooth, even while tracking 21 hand landmarks in real-time.

---

## Key Features

* **Zero-Lag Performance:** The vision engine runs independently, ensuring no frame drops in Blender.
* **Intuitive Controls:**
    * **Orbit:** Make a **Fist** and move your hand to rotate around objects.
    * **Zoom:** **Pinch** your fingers to dolly in and out.
    * **Pan:** **Open Palm** to slide the view laterally (coming in v1.1).
* **Safety Clutch:** A "Listening Mode" toggle prevents accidental camera movement while you work.
* **Privacy First:** All processing is done locally on your machine. No images are ever saved or sent to the cloud.

---

## Documentation

We have detailed documentation available in the `docs/` folder to help you get started and understand the system architecture.

| Document | Description |
| :--- | :--- |
| **[Installation Guide](docs/INSTALL.md)** | Step-by-step setup for Python (Server) and Blender (Client). |
| **[User Manual](docs/USER_MANUAL.md)** | The "Gesture Dictionary" and best practices for lighting/positioning. |
| **[Architecture](docs/ARCHITECTURE.md)** | A deep dive into the UDP networking and decoupled design. |
| **[Roadmap](docs/ROADMAP.md)** | Future plans, including custom gesture mapping and key binds. |

---

## Quick Start

### Prerequisites
* **Blender:** Version 3.0 or higher.
* **Python:** Version 3.10 or 3.11 (installed on your system).
* **Webcam:** Any standard laptop or USB webcam.

### 1. Set up the Vision Server
Open your terminal in the project folder and install dependencies:
```
pip install -r requirements.txt
```

Start the vision server:
```
python server/main.py
```

*You should see a message: "Server listening on 127.0.0.1:5555"*

### 2. Install the Blender Client
1.  Zip the `client` folder (name it `GestureNav_Client.zip`).
2.  Open Blender and go to **Edit > Preferences > Add-ons**.
3.  Click **Install...** and select your zip file.
4.  Search for "GestureNav" and enable the checkbox.

### 3. Start Navigating
1.  In the Blender 3D Viewport, press **N** to open the Sidebar.
2.  Click the **GestureNav** tab.
3.  Click **Start Listener**.
4.  *Raise your hand and make a fist to test!*

---

# Directory Structure
```
GestureNav/
├── assets/                 # Images and branding resources
├── client/                 # Blender Add-on source code
├── server/                 # Python Computer Vision source code
├── docs/                   # Full project documentation
├── requirements.txt        # Python dependencies for the server
└── README.md               # You are here
```

---

# Contributing
Contributions are welcome! Please read the Roadmap to see what features are currently planned.

---

# License
This project is licensed under the GNU General Public License v3.0. Because this project integrates with Blender's API, it adheres to the open-source spirit of the Blender ecosystem.