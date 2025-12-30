# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] (v1.7.0)
### Added
- **Docs:**
    - `docs/ARCHITECTURE.md`: Detailed system design and threading model.
    - `docs/PROTOCOL.md`: Specification for UDP Port 5005 and Orbit/Zoom/Lock states.
    - `CONTRIBUTING.md`: Governance and style guide (camelCase).
    - `CODE_OF_CONDUCT.md` and `SECURITY.md`.

## [v1.6.0] - 2025-12-28
### Added
- **System:** "The Puppet Master" Architecture (Decoupled Client-Server).
- **Server:** MediaPipe Hand Tracking with specialized "GestureDecider" logic.
- **Client:** Blender Modal Operator for non-blocking UI.
- **Feature:** Deadzone-based Orbit control.
- **Feature:** Pinch-to-Zoom.
- **Safety:** Fist detection lock.

### Changed
- Moved expensive computation out of Blender into a separate Python process.
- Switched to UDP for low-latency communication.
