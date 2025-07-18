import subprocess
import sys
import os

def build():
    target_name = "ConsultingToolkit"
    cmd = [
        "pyinstaller",
        "--clean",
        "--onefile",
        "--name", target_name,
        "run.py",
    ]

    if sys.platform.startswith("darwin"):
        # macOS: create app bundle
        cmd.extend(["--windowed"])  # hide terminal
    elif sys.platform.startswith("win"):
        # Windows: standard exe
        cmd.extend(["--noconsole"])
    subprocess.check_call(cmd)

    dist_path = os.path.join("dist", target_name + (".app" if sys.platform.startswith("darwin") else ".exe"))
    print(f"Build complete: {dist_path}")

if __name__ == "__main__":
    build()
