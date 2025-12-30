# **GestureNav Roadmap**
> **Product Vision**

## **Completed Milestones**

### **The Core (v1.0.0 - v1.3.0) [COMPLETED]**

* [x] **Architecture:** Decoupled "Puppeteer" Pattern (UDP Client-Server).
* [x] **Navigation:** Orbit (Virtual Joystick) and Zoom (Pinch).
* [x] **Safety:** Fist Lock and Listening Mode Clutch.
* [x] **Configuration:** (Accelerated from Phase 3)
    * [x] Full Tuning Dashboard.
    * [x] Handedness Presets.
    * [x] Save/Load Persistence.

---

### **The Polish Update (v1.5.0) [COMPLETED]**

*Focus: User Experience & Reliability*

* [x] **Graceful Shutdown:** Clean exit via 'Q', 'Esc', or Window Close.
* [x] **One-Click Launcher:** Auto-install dependencies and model.
* [x] **Robust Configuration:** Persistence and Handedness presets.

---

### **The Architecture Update (v1.6.0) [COMPLETED]**

*Focus: Scalability, Stability & Code Hygiene*

* [x] **Modular Architecture:**
    * [x] Server: Split into `vision`, `networking`, `config`.
    * [x] Client: Split into `ui`, `networking`, `config`.
* [x] **Infrastructure:**
    * [x] Dedicated `Tools/` directory for automation.
    * [x] Clean `assets/` organization.
* [x] **Reliability:**
    * [x] Centralized configuration handling.
    * [x] Standardized package layout.

---

### **The Knowledge Base (v1.7.0) [COMPLETED]**

*Focus: Documentation & Governance*

* [x] **Technical Specs:**
    * [x] `ARCHITECTURE.md`: Threading model and System Design.
    * [x] `PROTOCOL.md`: UDP Packet definitions for external integrations.
* [x] **Governance:**
    * [x] `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
    * [x] Professional `CHANGELOG.md` history.

---

### **The DevOps Pipeline (v1.8.0) [COMPLETED]**

*Focus: Automation & Quality Assurance*

* [x] **The Gatekeeper (CI):**
    * [x] GitHub Actions workflow for Python Linting (`flake8`).
    * [x] Issue and Pull Request Templates.
* [x] **The Factory (CD):**
    * [x] Automated Packaging Script (`Tools/build-scripts/package_addon.py`).
    * [x] Auto-release generation on Tag push.

---

## **Active Development**

> *The developer is currently stuck in exams* 🥀💔

---

## **Future Horizon**

### **The "Cockpit" Update (v1.9.0)**

*Focus: Heads-Up Display (HUD) & Usability*

* [ ] **Virtual Joystick:** Draw GPU-based Joystick overlay directly in Blender Viewport.
* [ ] **Zoom Throttle:** Visual slider for zoom feedback.
* [ ] **Inverted Control:** Option to invert zoom direction ("Pull" vs "Push").
* [ ] **Purpose:** Removes the need for a second monitor or visible server window.

---

### **The "Virtuoso" Update (v2.0)**

*Focus: Advanced Control Mechanics*

* [ ] **Feature: Panning (Strafe).** "Open Palm" gesture to move view laterally.
* [ ] **Feature: View Snapping.** "Swipes" to snap to Front/Side/Top views.
* [ ] **Feature: Focus Selected.** "Double Pinch" to center view.

---

### **Advanced Control (v3.0)**

*Focus: Beyond Navigation*

* [ ] **Custom Gestures:** Map specific hand signs (e.g., "Peace Sign") to custom operators.
* [ ] **Direct Hand Rendering:** Draw full hand skeleton in 3D space using `gpu` module.
* [ ] **Standalone Compilation:** Compile Server to `.exe` using Nuitka/PyInstaller.