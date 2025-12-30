# GestureNav
> **Touchless 3D Navigation for Blender**

![GestureNav Hero](assets/branding/GestureNav_hero.png)

<div align="center">

  <a href="https://github.com/lolbanoori/GestureNav/releases/tag/v1.8.0">
    <img src="https://img.shields.io/badge/Download-v1.8.0-red?style=for-the-badge&logo=windows" alt="Download Release">
  </a>

  <a href="docs/INSTALL.md">
    <img src="https://img.shields.io/badge/Installation-Guide-blue?style=for-the-badge" alt="Get Started">
  </a>

  <a href="docs/USER_MANUAL.md">
    <img src="https://img.shields.io/badge/User-Manual-blue?style=for-the-badge" alt="Read Manual">
  </a>

</div>


**GestureNav** is a professional tool that decouples computer vision from Blender's internal loop, allowing users to orbit and zoom the 3D viewport using hand gestures captured via a standard webcam.

**v1.8.0 Update:** Now features a **DevOps Pipeline** with automated CI/CD checks, standardized Issue Templates, and automated Release generation!

---

## Key Features

*   **Zero-Lag Performance:** The vision engine runs independently on a separate thread/process.
*   **Intuitive Controls:**
    *   **Virtual Joystick Orbit:** Move your hand from the center to orbit. The further you reach, the faster it spins.
    *   **Zoom:** **Pinch** your fingers to zoom in, **Spread** to zoom out.
*   **Safety & UX:**
    *   **Graceful Shutdown:** Close the server cleanly with **'Q'**, **'Esc'**, or the Window **'X'**.
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
**Double-click `start_server.bat`!**

*   It will automatically install requirements and download the AI model for you.
*   *You should see a webcam window appear.*

*(Linux/Mac users: Run `pip install -r requirements.txt` then `python -m server.main`)*

### 2. Install the Blender Client
1.  **Zip** the `client` folder (Name it `GestureNav_Client.zip`).
2.  **Drag and Drop** the zip file into Blender (or install via **Edit > Preferences > Add-ons**).
3.  Enable the **GestureNav Client** add-on.

> *Developers: You can still load `client/__init__.py` in the Scripting Workspace for testing.*

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
├── assets/                  # Branding & Screenshots
├── client/                  # Blender Add-on (Modular)
│   ├── __init__.py          # Registry
│   ├── config.py            # Settings & Properties
│   ├── networking.py        # UDP Logic
│   └── ui.py                # Interface Panel
├── server/                  # Vision Server (Modular)
│   ├── config/              # Settings & Constants
│   ├── networking/          # UDP Server Class
│   ├── vision/              # MediaPipe Hand Tracking
│   └── main.py              # Orchestrator
├── Tools/                   # Build Scripts & Automation
├── docs/                    # Full project documentation
├── start_server.bat         # One-Click Launcher
├── requirements.txt         # Python dependencies
└── README.md                # You are here
```

---

## Contributing
Contributions are welcome! Please read the Roadmap to see what features are currently planned.

---

## License
This project is licensed under the GNU General Public License v3.0. Because this project integrates with Blender's API, it adheres to the open-source spirit of the Blender ecosystem.