# **GestureNav Roadmap**
> **Product Vision**

## **Phase 1: The Core (v1.0 - v1.3) [COMPLETED]**

*   [x] **Architecture:** Decoupled "Puppeteer" Pattern (UDP Client-Server).
*   [x] **Navigation:** Orbit (Virtual Joystick) and Zoom (Pinch).
*   [x] **Safety:** Fist Lock and Listening Mode Clutch.
*   [x] **Configuration:** (Accelerated from Phase 3)
    *   [x] Full Tuning Dashboard.
    *   [x] Handedness Presets.
    *   [x] Save/Load Persistence.

---

## **Phase 2: The Polish Update (v1.5) [COMPLETED]**

*Focus: User Experience & Reliability*

*   [x] **Graceful Shutdown:** Clean exit via 'Q', 'Esc', or Window Close.
*   [x] **One-Click Launcher:** Auto-install dependencies and model.
*   [x] **Robust Configuration:** Persistence and Handedness presets.

---

## **Phase 3: The Refactor (v1.6.0) [COMPLETED]**

*Focus: Scalability, Stability & Code Hygiene*

*   [x] **Modular Architecture:**
    *   [x] Server: Split into `vision`, `networking`, `config`.
    *   [x] Client: Split into `ui`, `networking`, `config`.
*   [x] **Infrastructure:**
    *   [x] Dedicated `Tools/` directory for automation.
    *   [x] Clean `assets/` organization.
*   [x] **Reliability:**
    *   [x] Fix circular imports via `python -m server.main`.
    *   [x] Consistent configuration defaults.

---

## **Phase 4: The "Virtuoso" Update (v2.0)**

*Focus: Advanced Control*

*   [ ] **Feature: Panning (Strafe).** "Open Palm" gesture to move view laterally.
*   [ ] **Feature: View Snapping.** "Swipes" to snap to Front/Side/Top views.
*   [ ] **Feature: Focus Selected.** "Double Pinch" to center view.

---

## **Phase 5: Advanced Control (v3.0)**

*Focus: Beyond Navigation*

*   [ ] **Custom Gestures:** Map specific hand signs (e.g., "Peace Sign") to operators.
*   [ ] **Visual Overlay:** Draw the hand skeleton directly inside the Blender 3D Viewport (using GPU module) instead of a separate window.
