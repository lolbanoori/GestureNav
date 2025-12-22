# **GestureNav**
> **Touchless 3D Navigation for Blender**

## **Phase 1: The Core (MVP \- v1.0)** 

*Focus: Stability & Basic Navigation*

* **Architecture:** Validated "Puppeteer" Pattern (UDP Client-Server).  
* **Features:**  
  * Orbit (Fist \+ Move).  
  * Zoom (Pinch In/Out).  
  * "Clutch" Toggle (Keyboard hotkey to enable/disable listening).  
* **UX:** Basic center-screen deadzone to prevent drift.

---

## **Phase 2: The "Virtuoso" Update (v1.1)** 

*Focus: Completing the Navigation Suite*

* **Feature: Panning (Strafe).** Implementation of the "Open Palm" gesture to move the view laterally.  
* **Feature: View Snapping.** Implementation of high-velocity "Swipes" to snap to Front/Side/Top views.  
* **Feature: Focus Selected.** "Double Pinch" gesture to trigger  Numpad .  (Center view on object).

---

## **Phase 3: User Customization (v1.5)** 

*Focus: Accessibility & Comfort*

* **Settings UI:** A panel in Blender to adjust:  
  * **Sensitivity Curves:** Linear vs. Exponential (for finer control at slow speeds).  
  * **Invert Axis:** For users who prefer "Flight Sim" controls (Up \= Down).  
  * **Smoothing Factor:** Slider to trade off latency vs. smoothness.

---

## **Phase 4: Advanced Control (v2.0)** 

*Focus: Beyond Navigation*

* **Custom Gestures:** Ability to map a specific hand sign (e.g., "Peace Sign") to a specific Blender Operator (e.g.,  Undo  ,  Render  , or  Toggle X-Ray  ).  
* **Multi-Modal Feedback:** Visual overlay in the 3D viewport showing the user's hand state (e.g., a small red dot when "Fist" is detected) so they know how the system is interpreting their hand.
