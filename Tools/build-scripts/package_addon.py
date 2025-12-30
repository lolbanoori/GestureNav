import os
import zipfile
import re
import sys

def get_version():
    """Extracts version from client/__init__.py"""
    init_path = os.path.join("client", "__init__.py")
    with open(init_path, "r") as f:
        content = f.read()
    # Find version tuple, e.g., "version": (1, 8, 0)
    match = re.search(r'"version":\s*\((\d+),\s*(\d+),\s*(\d+)\)', content)
    if match:
        return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    raise ValueError("Could not find version in client/__init__.py")

def package_addon():
    version = get_version()
    zip_name = f"GestureNav_client_v{version}.zip"
    source_dir = "client"

    print(f"Packaging {zip_name}...")

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Exclude pycache to keep zip clean
            dirs[:] = [d for d in dirs if d not in ['__pycache__']]
            
            for file in files:
                if file.endswith('.pyc') or file == '.DS_Store':
                    continue
                
                file_path = os.path.join(root, file)
                # Maintain folder structure inside zip
                arcname = os.path.relpath(file_path, start=os.path.dirname(source_dir))
                zipf.write(file_path, arcname)

    print(f"Successfully created {zip_name}")

    # Write variables to GitHub Actions environment
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"VERSION={version}\n")
            f.write(f"FILENAME={zip_name}\n")

if __name__ == "__main__":
    package_addon()
