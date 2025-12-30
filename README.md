# GestureNav
> Touchless 3D Navigation for Blender using computer vision and hand gestures.

![GestureNav Hero](assets/branding/GestureNav_hero.png)

<a href="https://github.com/lolbanoori/GestureNav/releases/tag/v1.8.0">
  <img src="https://img.shields.io/badge/Download-v1.8.0-red?style=for-the-badge&logo=windows" alt="Download Release">
</a>
<a href="docs/INSTALL.md">
  <img src="https://img.shields.io/badge/Installation-Guide-blue?style=for-the-badge" alt="Get Started">
</a>
<a href="docs/USER_MANUAL.md">
  <img src="https://img.shields.io/badge/User-Manual-blue?style=for-the-badge" alt="Read Manual">
</a>

**GestureNav** is a professional tool that decouples computer vision from Blender's internal loop, allowing users to orbit and zoom the 3D viewport using hand gestures captured via a standard webcam.

**v1.8.0 Update:** Now features a **DevOps Pipeline** with automated CI/CD checks, standardized Issue Templates, and automated Release generation!

---

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Structure](#structure)
- [API](#api)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

---

## Background

Traditional specialized hardware for 3D navigation (like 3D mice) is expensive. GestureNav provides a cost-effective, touchless alternative by leveraging standard webcams and modern MediaPipe hand tracking. Our unique decoupled architecture ensures that the heavy computer vision processing never slows down the Blender viewport.

---

## Install

For a detailed step-by-step guide, please see our **[Installation Guide](docs/INSTALL.md)**.

### Prerequisites

*   **Blender:** Version 3.0 or higher.
*   **Python:** Version 3.10 or 3.11 (installed on your system).
*   **Webcam:** Any standard laptop or USB webcam.

### Server Setup

**Double-click `start_server.bat`!**

*   It will automatically install requirements and download the AI model for you.
*   You should see a webcam window appear.
*   *(Linux/Mac users: Run `pip install -r requirements.txt` then `python -m server.main`)*

### Client Setup

1.  **Zip** the `client` folder (Name it `GestureNav_Client.zip`) or download the release.
2.  **Drag and Drop** the zip file into Blender (or install via **Edit > Preferences > Add-ons**).
3.  Enable the **GestureNav Client** add-on.

---

## Usage

For comprehensive usage instructions, "Gesture Dictionary", and best practices, see the **[User Manual](docs/USER_MANUAL.md)**.

### Quick Start

1.  In the 3D Viewport, press **N** to open the Sidebar.
2.  Click the **GestureNav** tab.
3.  Click **Start Listener**.
4.  **Test it:** Raise your hand using the "Virtual Joystick" method.

### Controls

| Gesture | Action | Visual Feedback (Server) |
| :--- | :--- | :--- |
| **Neutral Hand** | **Stop / Idle** | Cursor in Green Circle. |
| **Move Hand** | **Orbit Camera** | Cursor leaves Green Circle. |
| **Pinch Fingers** | **Zoom In** | Text "ZOOM IN" (Red). |
| **Spread Fingers** | **Zoom Out** | Text "ZOOM OUT" (Blue). |
| **Make a Fist** | **Lock Zoom** | Text "FIST (ZOOM LOCKED)". |

---

## Structure

```
GestureNav/
├── assets/                  # Branding & Screenshots
├── client/                  # Blender Add-on (Modular)
├── server/                  # Vision Server (Modular)
├── Tools/                   # Build Scripts & Automation
├── docs/                    # Full project documentation
├── start_server.bat         # One-Click Launcher
└── README.md                # You are here
```

---

## API

For detailed technical specifications, please refer to:

*   **[Architecture](docs/ARCHITECTURE.md)** - System design and threading model.
*   **[Protocol](docs/PROTOCOL.md)** - UDP packet structure and state definitions.

---

## Contributing

Contributions are welcome!
Please check out the [Roadmap](docs/ROADMAP.md) and see our [Contributing Guide](CONTRIBUTING.md) for details on how to propose bug fixes and improvements.

Please note that this project is released with a **[Code of Conduct](CODE_OF_CONDUCT.md)**. By participating in this project you agree to abide by its terms.

---

## Security

Please consult [SECURITY.md](SECURITY.md) for our security policy and vulnerability reporting.

---

## License

GNU General Public License v3.0 © [Zohair Banoori](https://github.com/lolbanoori)