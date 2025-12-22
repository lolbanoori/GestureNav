# **GestureNav**
> **Touchless 3D Navigation for Blender**

## **1\. Executive Summary**

A specialized tool allowing Blender users to orbit and zoom the 3D viewport using hand gestures captured via a laptop webcam. The system prioritizes viewport performance by decoupling heavy computer vision processing from Blender’s internal update loop.

---

## **2\. System Architecture: "The Puppeteer Pattern"**

We utilize a **Decoupled Client-Server** architecture over a local UDP network. This ensures that the heavy image processing (Server) never blocks the Blender UI thread (Client).

### The Server (Brain): 

A standalone Python process that runs OpenCV and MediaPipe. It calculates vector deltas and broadcasts them.

### The Client (Body): 

A lightweight Blender Add-on that listens to a specific port and applies transforms to the Viewport.

---

## **3\. Technology Stack**

	

| Component Category | Technology / Library | Specific Component | Target Version | Integration Status | Primary Function in System |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Operating System | Windows 10/11 | OS Environment | N/A | Finalized | Target Platform for Application Deployment |
| Backend/Server | Python (External) | Server Host | 3.10 or 3.11 | Finalized | Hosting the Vision Processing Engine |
| Vision Processing | mediapipe | Hand Tracking | Latest | Finalized | High-performance Real-time Hand Tracking |
| Vision Processing | opencv-python | Video Stream Handler | Latest | Finalized | Webcam Stream Capture and Processing |
| Core Utilities | numpy | Mathematical Operations | Latest | Finalized | Efficient Vector and Matrix Calculations |
| Frontend/Client | Blender Python API | 3D View Controller | 3.0+ | Finalized | Manipulating and Updating the 3D Scene View |
| Communication | socket (Std Lib) | Communication Protocol | N/A | Finalized | Local UDP Communication between Client and Server |

---

## **4\. Functional Logic (Single-Hand Control)**

### A. Trigger Mechanism

**Type:** Keyboard Toggle (e.g.,  Caps Lock  or custom hotkey).

**Behavior:** The system enters a "Listening" state only when triggered. It acts as a safety clutch to prevent accidental camera movement while working.

### B. Navigation Logic (The "Virtual Joystick")

We track a single hand to control two axes of movement:

#### Orbit (Rotate):

**Input:** Position of the Wrist Landmark (Index 0).

**Logic:** Defined by a "Deadzone" in the center of the camera frame.

**Action:**

* Hand moves Right → Orbit View Right (Yaw).  
* Hand moves Up → Orbit View Up (Pitch).

**Calculation:** Normalized vector distance from the image center *(0.5, 0.5)*.

#### Zoom (Dolly):

**Input:** Euclidean distance between Index Finger Tip (8) and Thumb Tip (4).

**Logic:**

* Pinch In (Tips touching) → Zoom In.  
* Open Hand → Stop Zoom/Zoom Out (depending on calibration).

**Smoothing:** Changes in zoom values are smoothed to prevent "stuttery" camera movement.

---

## **5\. Data Interface (UDP Protocol)**

Connection:  127.0.0.1  (Localhost) on Port  5555  .

**Packet Structure (JSON encoded bytes):** The Server sends this packet 30-60 times per second.

```
{
  "state": "active",       // Enum: "active", "idle", "lost\_tracking"
  "orbit\_x": 0.05,         // Float: \-1.0 to 1.0 (Horizontal speed)
  "orbit\_y": \-0.02,        // Float: \-1.0 to 1.0 (Vertical speed)
  "zoom\_delta": 0.0        // Float: Positive \= In, Negative \= Out
}
```

---

## **6\. Implementation Phases**

**Phase 1: Comms Skeleton** → Create the Blender Add-on listener to verify it can receive data without crashing the UI.

**Phase 2: Vision Engine** → Build the external Python script to detect hands and output raw coordinates to the console.

**Phase 3: Integration & Math** → Connect the two. Convert raw coordinates into the JSON packet and implement **Exponential Moving Average (EMA)** smoothing in Blender to remove jitter.

---

## **7\. Directory Structure**

```
GestureNav/
├── assets/                     
│   └── gesturenav_hero.png     
├── client/                     # Blender Add-on Code
├── server/                     # Python Computer Vision Code
├── docs/                       
│   ├── INSTALL.md              # Installation & Setup Guide
│   ├── USER_MANUAL.md          # User Manual & Gesture Guide
│   ├── ARCHITECTURE.md         # Technical Design Document
│   └── ROADMAP.md              # Product Roadmap
├── .gitignore                  
├── LICENSE                     
├── requirements.txt            # Python dependencies
└── README.md
```
