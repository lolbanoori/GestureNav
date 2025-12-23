# **GestureNav Architecture**
> **Technical Design Document (v1.3)**

## **1. Executive Summary**

A specialized tool allowing Blender users to orbit and zoom the 3D viewport using hand gestures captured via a laptop webcam. The system prioritizes viewport performance by decoupling heavy computer vision processing from Blender’s internal update loop.

---

## **2. System Pattern: "The Puppet Master"**

We utilize a **Decoupled Client-Server** architecture over a local UDP network. This ensures that the heavy image processing (Server) never blocks the Blender UI thread (Client).

### The Server (Brain): 
A standalone Python process that runs OpenCV and MediaPipe. 
*   **Thread 1 (Main):** Captures video, tracks hands using MediaPipe Tasks, calculates vector deltas, and broadcasts navigation data to Port 5555.
*   **Thread 2 (Config Listener):** Listens on Port 5556 for tuning updates from the Client.

### The Client (Body): 
A lightweight Blender Add-on.
*   **Operator:** Runs a modal timer to listen to Port 5555 and applies transforms to the Viewport.
*   **UI Panel:** Sends configuration JSON packets to Port 5556 whenever a slider is moved.

---

## **3. Data Interface (Bidirectional UDP)**

### Downstream: Navigation Data
**Server -> Client (Port 5555)**
*Frequency: 30-60Hz*

Packet Structure:
```json
{
  "state": "active",       // "active" or "idle"
  "x": 0.5,                // Float: -1.0 to 1.0 (Orbit X Speed)
  "y": -0.2,               // Float: -1.0 to 1.0 (Orbit Y Speed)
  "zoom": 1                // Integer: 1 (In), -1 (Out), 0 (None)
}
```

### Upstream: Configuration Data
**Client -> Server (Port 5556)**
*Frequency: On Change*

Packet Structure:
```json
{
  "deadzone_radius": 0.12,
  "deadzone_offset_x": 0.75, // 0.25 for Left Hand
  "zoom_thresh_in": 0.05,
  "orbit_sens_server": 3.0,
  "use_fist_safety": true
  // ... other props
}
```

---

## **4. Functional Logic**

### A. Orbit (Virtual Joystick) and Deadzone
We calculate the distance of the **Wrist** from a "Deadzone Center" (configurable).
*   **Inside Deadzone:** No movement.
*   **Outside Deadzone:** Movement speed increases linearly (clamped by Max Speed).

### B. Zoom (Discrete Trigger)
We calculate the distance between **Thumb** and **Index** tips.
*   **Distance < Threshold_In:** Zoom In.
*   **Distance > Threshold_Out:** Zoom Out.
*   **Between:** Idle (Hysteresis loop prevents jitter).

### C. Safety Locks
1.  **Fist Lock:**
    *   Logic: Checks average distance of Middle, Ring, and Pinky tips to Wrist.
    *   If small (< 0.25), input is flagged as a "Fist".
    *   Result: Zoom Orbit is ignored (Safety).
2.  **Open Hand Lock:**
    *   Logic: Checks if fingers are fully extended.
    *   Result: Orbit is stopped (optional).

---

## **5. Technology Stack**

| Component | Technology | Role |
| :---- | :---- | :---- |
| **Server** | Python 3.10+ | Host Process |
| **Vision** | MediaPipe Tasks | High-performance Hand Tracking |
| **Video** | OpenCV | Webcam Capture & Visualization |
| **Client** | Blender Python API | Add-on & Viewport Control |
| **Comms** | UDP Sockets | IPC (Inter-Process Communication) |
| **Persistence** | JSON | Saving user profiles to `~/.gesturenav_config.json` |

---

## **6. Directory Structure**

```
GestureNav/
├── assets/                     # Branding
├── client/                     # Blender Add-on
│   ├── __init__.py             # UI, Props, and Lifecycle
│   └── operator_listen.py      # Modal Operator & Navigation Logic
├── server/                     # Vision Server
│   ├── main.py                 # Entry Point (Threads & Logic)
│   └── hand_landmarker.task    # Model File
├── docs/                       
│   ├── INSTALL.md              # Installation & Setup Guide
│   ├── USER_MANUAL.md          # User Manual & Gesture Guide
│   ├── ARCHITECTURE.md         # Technical Design Document
│   └── ROADMAP.md              # Product Roadmap
├── .gitignore                  
├── LICENSE                     
├── requirements.txt            # Python dependencies
└── README.md                   # Overview
```