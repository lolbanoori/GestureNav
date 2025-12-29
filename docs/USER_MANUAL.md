# **GestureNav User Manual**
> **Mastering Touchless Navigation**

<div align="center">
  <h1>User Guide & Gesture Dictionary</h1>
</div>

Welcome to a new way of interacting with Blender. GestureNav allows you to manipulate your 3D Viewport using only your hands. Because this tool relies on computer vision, "speaking" its language clearly is key to a smooth experience.

This guide will teach you the **Safety Clutch**, the **Gesture Dictionary**, and how to use the **Configuration Dashboard**.

---

## **1. The "Clutch" Concept (Safety First)**

Imagine driving a car. You don't want the car to move every time you bump the steering wheel while parked. GestureNav works the same way.

* **Inactive State (Default):** The camera ignores you. You can move freely.  
* **Active State:** You must explicitly click **"Start Listener"** in the Blender side panel.  
* **Rule of Thumb:** Only engage the Listener when you are ready to navigate. Disengage it when you return to modeling or sculpting with the mouse.

---

## **2. The Gesture Dictionary**

GestureNav tracks your hand (Left or Right, configurable) to control the camera.

### A. Orbit (The Virtual Joystick)
*The Metaphor: "Leaning the Stick."*

GestureNav puts a "Deadzone Circle" in the center of your camera view.
*   **Stop:** Keep your hand inside the Green Circle.
*   **Orbit:** Move your hand **outside** the circle.
*   **Speed:** The further you reach, the faster the camera spins.

### B. Zoom (The Pinch)
*The Metaphor: "Stretching the View."*

*   **Zoom In:** Pinch your **Thumb and Index Finger** together.
*   **Zoom Out:** Spread your Thumb and Index Finger apart (wide "L" shape).
*   **Idle:** Keep your fingers in a neutral, relaxed position.

### C. Safety Locks
*The Metaphor: "The Emergency Brake."*

Sometimes you need to reposition your hand without moving the camera.
*   **Fist Lock (Zoom):** Make a tight **Fist**. This disables the Zoom engine. Use this to move your hand back to a comfortable position without accidentally zooming in/out.
*   **Open Hand Lock (Orbit):** (Optional) If enabled in settings, opening your hand flat will stop the Orbit rotation.

---

## **Quick Reference (Controls)**

| Gesture | Action | Visual Feedback (Server) |
| :--- | :--- | :--- |
| **Neutral Hand** | **Stop / Idle** | Hand tracked, Cursor in Green Circle. |
| **Move Hand** | **Orbit Camera** | Cursor leaves Green Circle. |
| **Pinch Fingers** | **Zoom In** | Text "ZOOM IN" (Red). |
| **Spread Fingers** | **Zoom Out** | Text "ZOOM OUT" (Blue). |
| **Make a Fist** | **Lock Zoom** | Text "FIST (ZOOM LOCKED)". |

---

## **3. The Configuration Dashboard**

Located in the Blender Sidebar (N-Panel) > **GestureNav** tab.

### Handedness
Click **"Right Hand"** or **"Left Hand"** to automatically move the Deadzone to the bottom corner of the screen, so your arm doesn't block your monitor.

### Tuning (Real-time)
*   **Deadzone Radius:** Drag the slider to change how large the "Stop Circle" is.
*   **Sensitivity:** Adjust how fast the camera responds to your movements.
*   **Zoom Triggers:** Adjust the "Pinch In" vs "Pinch Out" gap to fit your hand size.

### Persistence
*   **Save Settings:** Saves your current tuning to `~/.gesturenav_config.json`.
*   **Load Settings:** Loads your saved profile.
*   **Reset Defaults:** Reverts to the factory calibration.

---

## **4. Best Practices**

### **Rule 1: Lighting is Everything**
Webcams need light. If you are backlit (bright window behind you), your hand will be a silhouette.
*   **Good:** Lamp in front of you (illuminating your hand).
*   **Bad:** Dark room or window behind you.

### **Rule 2: The "Deadzone"**
If the camera is drifting, look at the server window. bring your hand back to the **Green Circle** to stop it.

---

## **Troubleshooting**

*   **View Spinning Uncontrollably?** → You are outside the "Deadzone." Center your hand.
*   **Zoom Jumping?** → Your lighting is too dim; the camera can't see your fingertips clearly.
*   **Can't Connect?** → Ensure you ran `start_server.bat` (or `python -m server.main`) **before** clicking start in Blender.
*   **Camera does not move?** → Ensure "Start Listener" is clicked in Blender AND the Python Server window is open.
*   **Crashes with `NameError`?** → Ensure you are running the latest version of the scripts.

---

**Author**: Zohair Banoori
**Version**: 1.6.0
