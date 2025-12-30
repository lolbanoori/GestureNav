# Contributing to GestureNav

Thank you for your interest in improving GestureNav! We welcome contributions from the community.

## Quick Start (Development Environment)

To set up your environment for development:

### 1. The Server (Python)
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/lolbanoori/GestureNav.git
    cd GestureNav
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download the Model:**
    ```bash
    python server/download_model.py
    ```
4.  **Run the Server:**
    ```bash
    python server/main.py
    ```

### 2. The Client (Blender)
**Recommended for Devs (Symlink/Edit-in-Place):**
Instead of zipping and installing every time:
1.  Open Blender.
2.  Go to the **Scripting** tab.
3.  Open `client/__init__.py`.
4.  Run the script (Alt+P) to register the addon temporarily.

**For Testing Packaging:**
1.  Zip the `client/` folder.
2.  Install via **Edit > Preferences > Add-ons**.

---

## Style Guide

We adhere to strict coding standards to keep the codebase clean.

### Python Code
*   **Naming:** Use `snake_case` for variables and functions (e.g., `calculate_velocity`, `gesture_state`).
*   **Classes:** Use `PascalCase` (e.g., `HandTracker`, `GestureSender`).
*   **Formatting:** Follow PEP 8. Use 4 spaces for indentation.
*   **Linting:** We use `flake8` to enforce style. Run `flake8 .` before pushing.
*   **Strings:** Use double quotes `"` unless the string contains double quotes.

### Documentation
*   **Tone:** Professional and concise.
*   **Emojis:** Do **NOT** use emojis in official technical documentation (`docs/`). Keep them in `README.md` or this guide only.
*   **Markdown:** Use standard Markdown headers (`#`, `##`, `###`).

---

## Pull Request Process

1.  **Issue Link:** Every Pull Request (PR) must be linked to an existing Issue. If one doesn't exist, create it first.
    *   Use the **Bug Report** or **Feature Request** templates provided.
2.  **Descriptive Title:** Use a title that explains *what* changed (e.g., "Fix UDP timeout on server shutdown" not "Fix bug").
3.  **Scope:** Keep PRs small and focused. One feature/bugfix per PR.
4.  **Pass Tests & Linting:** 
    *   **CI Checks:** Ensure the automated GitHub Action passes (it checks `flake8` syntax).
    *   **Server:** Verify `python server/main.py` starts and tracks hands.
    *   **Client:** Verify the addon loads in Blender without console errors.

We reserve the right to close PRs that do not follow these guidelines.
