# **GestureNav Roadmap**
> **Product Vision**

## **Completed Milestones**

### **The Core (v1.0.0 - v1.3.0) [COMPLETED]**
* [x] **Architecture:** Decoupled "Puppeteer" Pattern (UDP Client-Server).
* [x] **Navigation:** Orbit (Virtual Joystick) and Zoom (Pinch).
* [x] **Safety:** Fist Lock and Listening Mode Clutch.
* [x] **Configuration:** Full Tuning Dashboard, Handedness Presets, Persistence.

---

### **The Polish Update (v1.5.0) [COMPLETED]**
*Focus: User Experience & Reliability*
* [x] **Graceful Shutdown:** Clean exit via 'Q', 'Esc', or Window Close.
* [x] **One-Click Launcher:** Auto-install dependencies and model.
* [x] **Robust Configuration:** Persistence and Handedness presets.

---

### **The Architecture Update (v1.6.0) [COMPLETED]**
*Focus: Scalability, Stability & Code Hygiene*
* [x] **Modular Architecture:** Split Server/Client into specialized packages.
* [x] **Infrastructure:** Dedicated `Tools/` directory and Clean `assets/`.
* [x] **Reliability:** Centralized configuration handling.

---

### **The Knowledge Base (v1.7.0) [COMPLETED]**
*Focus: Documentation & Governance*
* [x] **Technical Specs:** `ARCHITECTURE.md` and `PROTOCOL.md`.
* [x] **Governance:** `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
* [x] **History:** Professional `CHANGELOG.md`.

---

### **The DevOps Pipeline (v1.8.0) [COMPLETED]**
*Focus: Automation & Quality Assurance*
* [x] **The Gatekeeper (CI):** GitHub Actions for Linting (`flake8`) and Issue Templates.
* [x] **The Factory (CD):** Automated Packaging Script and Release Generation.

---

## **Active Development**

> *The developer is currently stuck in exams* 🥀💔

---

## **Future Horizon**

### **The "Cockpit" Update (v1.9.0)**
*Focus: Heads-Up Display (HUD) & Usability*

* [ ] **Virtual Joystick:** Draw GPU-based Joystick overlay directly in Blender Viewport.
* [ ] **Zoom Throttle:** Visual slider for zoom feedback.
* [ ] **Calibration Wizard:** A one-time setup tool to measure user hand size (Max Pinch/Palm Size) for perfect sensitivity.
* [ ] **Goal:** Remove the need for a second monitor or visible server window.


### **The "Virtuoso" Update (v2.0.0)**
*Focus: Advanced Control Mechanics*

* [ ] **Feature: Panning (Strafe).** "Peace Sign" (Victory) gesture to move view laterally.
* [ ] **Feature: View Snapping.** Rapid "Swipes" to snap to Front/Side/Top views.
* [ ] **Feature: Focus Selected.** "Double Pinch" (rapid pulse) to center view on object.
* [ ] **Core: Smart Smoothing.** Upgrade to Kalman Filters to eliminate micro-jitter while keeping latency low.

### **The "Platform" Update (v3.0.0)**
*Focus: Beyond Navigation*

* [ ] **Custom Gestures:** Map specific hand signs to custom Blender operators.
* [ ] **Direct Hand Rendering:** Draw full hand skeleton in 3D space using `gpu` module.
* [ ] **OS Expansion:** Investigation into Linux/MacOS support.