# GestureNav
> **Touchless 3D Navigation for Blender**

![GestureNav Hero Image](assets/GestureNav_hero.png)

<div align="center">

  <a href="https://github.com/lolbanoori/GestureNav/releases/tag/v1.3.1">
    <img src="https://img.shields.io/badge/Download-v1.3.1-red?style=for-the-badge&logo=windows" alt="Download Release">
  </a>

  <a href="docs/INSTALL.md">
    <img src="https://img.shields.io/badge/Installation-Guide-blue?style=for-the-badge" alt="Get Started">
  </a>

  <a href="docs/USER_MANUAL.md">
    <img src="https://img.shields.io/badge/User-Manual-blue?style=for-the-badge" alt="Read Manual">
  </a>

</div>

**GestureNav** is a professional tool that decouples computer vision from Blender's internal loop, allowing users to orbit and zoom the 3D viewport using hand gestures captured via a standard webcam.

**v1.3 Update:** Now features a full **Configuration Dashboard** inside Blender, **Safety Locks**, and **Handedness Presets**!

---

## Key Features

*   **Zero-Lag Performance:** The vision engine runs independently on a separate thread/process.
*   **Intuitive Controls:**
    *   **Virtual Joystick Orbit:** Move your hand from the center to orbit. The further you reach, the faster it spins.
    *   **Zoom:** **Pinch** your fingers to zoom in, **Spread** to zoom out.
*   **Safety Locks:**
    *   **Fist Lock:** Make a fist to disable Zoom (useful for repositioning your hand).
    *   **Open Hand Lock:** Open your palm flat to disable Orbit (optional).
*   **Configuration Dashboard:**
    *   **Tuning:** Adjust sensitivity, deadzone size, and zoom thresholds in real-time.
    *   **Presets:** One-click setup for **Left-Handed** or **Right-Handed** users.
    *   **Persistence:** Save your profile to disk.

---

## Documentation

We have detailed documentation available in the `docs/` folder to help you get started and understand the system architecture.

| Document | Description |
| :--- | :--- |
| **[Installation Guide](docs/INSTALL.md)** | Step-by-step setup for Python (Server) and Blender (Client). |
| **[User Manual](docs/USER_MANUAL.md)** | The "Gesture Dictionary" and best practices for lighting/positioning. |
| **[Architecture](docs/ARCHITECTURE.md)** | A deep dive into the UDP networking and decoupled design. |
| **[Roadmap](docs/ROADMAP.md)** | Future plans, including custom gesture mapping and key binds

---

## Quick Start

### Prerequisites
*   **Blender:** Version 3.0 or higher.
*   **Python:** Version 3.10 or 3.11 (installed on your system).
*   **Webcam:** Any standard laptop or USB webcam.

### 1. Set up the Vision Server
Open your terminal in the project folder:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download MediaPipe Model
python server/download_model.py

# 3. Start the Server
python server/main.py
```
*You should see a webcam window appear.*

### 2. Install the Blender Client
1.  Open Blender.
2.  Go to **Scripting** workspace.
3.  Open `client/__init__.py`.
4.  Click **Run Script** (Play icon).
    *   *(Alternatively, zip the `client` folder and install as an Add-on)*.

### 3. Start Navigating
1.  In the 3D Viewport, press **N** to open the Sidebar.
2.  Click the **GestureNav** tab.
3.  Click **Start Listener**.
4.  **Test it:** Raise your hand using the "Virtual Joystick" method.

---

## Controls

| Gesture | Action | Visual Feedback (Server) |
| :--- | :--- | :--- |
| **Neutral Hand** | **Stop / Idle** | Cursor in Green Circle. |
| **Move Hand** | **Orbit Camera** | Cursor leaves Green Circle. |
| **Pinch Fingers** | **Zoom In** | Text "ZOOM IN" (Red). |
| **Spread Fingers** | **Zoom Out** | Text "ZOOM OUT" (Blue). |
| **Make a Fist** | **Lock Zoom** | Text "FIST (ZOOM LOCKED)". |

---

## Directory Structure
```
GestureNav/
├── assets/                  # Images and branding resources
├── client/                  # Blender Add-on source code
├── server/                  # Python Computer Vision source code
│   ├── main.py              # The Vision Engine
│   └── hand_landmarker.task # AI Model (downloaded)
├── docs/                    # Full project documentation
├── requirements.txt         # Python dependencies
└── README.md                # You are here
```

---

## Contributing
Contributions are welcome! Please read the Roadmap to see what features are currently planned.

---

## License
This project is licensed under the GNU General Public License v3.0. Because this project integrates with Blender's API, it adheres to the open-source spirit of the Blender ecosystem.