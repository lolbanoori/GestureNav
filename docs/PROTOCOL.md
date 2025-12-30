# **GestureNav Protocol (v1.7.0)**
> **API Specification**

This document defines the communication standard between the GestureNav Server (Vision) and any Client (Blender, Unity, Unreal, etc.).

---

## **1. Transport Layer**

*   **Protocol:** UDP (User Datagram Protocol)
*   **Default Port:** `5005`
*   **Direction:** Server -> Client (Fire-and-Forget)
*   **Encoding:** UTF-8 String (JSON formatted)

> [!NOTE]
> UDP is chosen for low latency. Dropped packets are preferable to delayed packets (Head-of-Line blocking) in real-time control.

---

## **2. Packet Structure**

The server streams a string based dictionary (JSON) representing the current hand state.

**Format:**
```json
{
  "state": "STATE_STRING",
  "data": {
    "v_x": FLOAT,
    "v_y": FLOAT,
    "val": FLOAT
  }
}
```

### **Fields**

| Field | Type | Range | Description |
| :--- | :--- | :--- | :--- |
| `state` | String | `ORBIT` \| `ZOOM` \| `LOCK` | The active control mode. |
| `v_x` | Float | `-1.0` to `1.0` | Horizontal Velocity (Left/Right). |
| `v_y` | Float | `-1.0` to `1.0` | Vertical Velocity (Up/Down). |
| `val` | Float | Any | Contextual value (e.g., Zoom magnitude). |

---

## **3. State Definitions**

The system operates as a state machine. The Client should switch behavior based on the `state` field.

### **A. ORBIT**
Standard navigation mode. The user is moving their hand to rotate the camera.
*   **Payload Example:**
    ```json
    { "state": "ORBIT", "data": { "v_x": 0.5, "v_y": -0.1, "val": 0.0 } }
    ```
*   **Client Action:** Rotate Viewport.

### **B. ZOOM**
The user performs a pinch gesture to zoom.
*   **Payload Example:**
    ```json
    { "state": "ZOOM", "data": { "v_x": 0.0, "v_y": 0.0, "val": 1.0 } }
    ```
*   **Client Action:** Dolly Camera.
*   `val`: `1.0` (Zoom In), `-1.0` (Zoom Out).

### **C. LOCK**
Safety mode. The user has formed a fist or the hand is lost.
*   **Payload Example:**
    ```json
    { "state": "LOCK", "data": { "v_x": 0.0, "v_y": 0.0, "val": 0.0 } }
    ```
*   **Client Action:** Ignore all input. Stop movement immediately.

---

## **4. Connection Flow (Handshake)**

**There is NO handshake.**

1.  Server starts and begins broadcasting to `localhost:5005`.
2.  Client starts listening on `localhost:5005`.
3.  Client picks up the stream immediately.

If the Server restarts, the Client simply continues listening. If the Client restarts, it catches the next packet.
