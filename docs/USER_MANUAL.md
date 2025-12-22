# **GestureNav**
> **Touchless 3D Navigation for Blender**

<div align="center">
  <h1>User Manual & Gesture Guide</h1>
</div>

Welcome to a new way of interacting with Blender. GestureNav allows you to manipulate your 3D Viewport using only your hands. Because this tool relies on computer vision, "speaking" its language clearly is key to a smooth experience.

This guide will teach you the **Safety Clutch**, the **Gesture Dictionary**, and **Environmental Best Practices**.

---

## **1\. The "Clutch" Concept (Safety First)**

Imagine driving a car. You don't want the car to move every time you bump the steering wheel while parked. GestureNav works the same way.

* **The Problem:** Your webcam is always on. If you scratch your nose or reach for your coffee, the camera might think you are trying to rotate the view.  
* **The Solution:** The **"Listener"** (Clutch).  
* **Inactive State (Default):** The camera ignores you. You can move freely.  
* **Active State:** You must explicitly click **"Start Listener"** in the Blender side panel (or press the assigned hotkey).  
* **Rule of Thumb:** Only engage the Listener when you are ready to navigate. Disengage it when you return to modeling or sculpting with the mouse.

---

## **2\. The Gesture Dictionary**

GestureNav tracks your **Right Hand** by default. It distinguishes between three specific hand shapes to determine *what* you want to do.

### A. Orbit (Rotate View)
*The Metaphor: "Grabbing the World."*

Imagine the 3D object is floating in the air physically. To turn it, you would grab it and turn your wrist.

* **The Gesture:** **Closed Fist.**  
* **How to Perform:**  
  1. Close your fingers into a fist.  
  2. **Move your hand** (not just your wrist) in the air.  
  3. **Right/Left:** Rotates the view around the object.  
  4. **Up/Down:** Tilts the view over/under the object.

### B. Pan (Strafe/Move View)
*The Metaphor: "Pushing the Air."*

Imagine the 3D view is a sheet of paper on a desk. You want to slide the paper sideways without turning it.

* **The Gesture:** **Open Palm** (fingers spread, facing the camera).  
* **How to Perform:**  
  1. Open your hand flat, palm facing the screen.  
  2. **Move your hand** in any direction.  
  3. The view will slide laterally, tracking your hand movement perfectly.

### C. Zoom (Dolly In/Out)
*The Metaphor: "Stretching the Image."*

This works exactly like pinching a touch screen on a smartphone.

* **The Gesture:** **The Pinch** (Index finger and Thumb).  
* **How to Perform:**  
  1. Face your palm toward the camera.  
  2. **Pinch In:** Bring your thumb and index finger tip together to **Zoom In**.  
  3. **Spread Out:** Move your thumb and index finger apart to **Zoom Out**.

---

## **3\. Best Practices (Optimizing Performance)**

Computer vision is magical, but it is sensitive to the real world. Follow these three rules to prevent "jittery" movement.

### **Rule 1: Lighting is Everything**

Webcams adjust exposure automatically. If you have a bright window behind you (Backlighting), your face and hand will become dark silhouettes. The computer cannot see your fingers in the dark.

* **Bad:** Window behind you.  
* **Good:** Lamp in front of you (illuminating your hand).

### **Rule 2: The "Deadzone"**

GestureNav uses a virtual joystick logic.

* **Center of Camera Frame:** This is "Zero Velocity." If your hand is here, the camera stops moving.  
* **Edges of Camera Frame:** This is "Max Velocity."  
* **Tip:** If the camera is drifting, bring your hand back to the center of your chest/webcam view to stop it.

### **Rule 3: Keep it Clean**

Avoid "noisy" backgrounds if possible. If there are other people moving behind you, or if you have a poster of a hand on your wall, the AI might get confused.

* **Pro Tip:** Wear a sleeve color that contrasts with your skin tone. (e.g., Don't wear a beige shirt if you have beige skin; the camera might lose track of your wrist).  

---

## **Troubleshooting Quick-List**

* **View Spinning Uncontrollably?** → You are outside the "Deadzone." Center your hand.  
* **Zoom Jumping?** → Your lighting is too dim; the camera can't see your fingertips clearly.  
* **Nothing Happening?** → Check if the **"Status: Listening..."** is active in the Blender N-Panel.
