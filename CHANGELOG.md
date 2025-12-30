# Changelog

> All notable changes to the **GestureNav** project will be documented in this file.

## [Unreleased]
*Development in progress for v1.8.0.*

### Added
- **CI Pipeline:** Automated GitHub Action (`ci.yml`) to enforce code quality on every push.
- **Linter Rules:** Added `.flake8` configuration to standardize Python code style (max-line-length: 120).
- **Issue Templates:** Standardized `bug_report.md` and `feature_request.md` forms to improve user reporting.
- **PR Template:** Added checklist for contributors to ensure quality before merging.

---

## [1.7.0] - 2025-12-30
### Added
- **Architecture:** Created `docs/ARCHITECTURE.md` with High-Level Diagram, Threading Model, and Coordinate System.
- **Protocol:** Created `docs/PROTOCOL.md` defining Transport (UDP 5005), Packet Structure, and States (ORBIT, ZOOM, LOCK).
- **Contribution Guide:** Created `CONTRIBUTING.md` with Quick Start, Style Guide, and Make PR sections.
- **Legal & Safety:** Added `CODE_OF_CONDUCT.md` (Contributor Covenant) and `SECURITY.md` (Vulnerability Reporting).
- **Changelog:** Created `CHANGELOG.md` to track project history.

---

## [1.6.0] - 2025-12-29
### Changed
- **Architectural Refactor:** Complete decoupling of the Server (Vision Engine) and Client (Blender Add-on).
- **Server:** Split monolithic `main.py` into specialized packages: `server.vision`, `server.networking`, and `server.config`.
- **Client:** Reorganized Blender Add-on into a modular MVC pattern (`client.ui`, `client.networking`, `client.config`).
- **Assets:** Moved branding and screenshots to the `assets/` directory for better project hygiene.

### Fixed
- Improved UDP socket handling to prevent "Address already in use" errors on quick restarts.

---

## [1.5.0] - 2024-12-15
### Added
- **Sensitivity Controls:** Added sliders in the N-Panel to adjust Orbit and Zoom sensitivity in real-time.
- **Handedness Support:** Added toggle for Left/Right hand preference.
- **Visual Feedback:** Server window now draws the "Deadzone" circle and hand landmarks overlay.

### Changed
- Improved gesture recognition threshold to reduce false positives during rapid movement.

---

## [1.3.1] - 2024-11-01
### Added
- **Initial Release:** Core GestureNav functionality.
- **Orbit Mode:** Open palm gesture to rotate the 3D viewport.
- **Zoom Mode:** Pinch gesture to zoom in/out.
- **Lock Mode:** Closed fist gesture to pause navigation.
- Basic UDP communication between Python Server and Blender Client.