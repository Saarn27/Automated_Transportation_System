import os
import subprocess
from datetime import datetime

SRC = "main.py"
EXE = os.path.join("dist", "main.exe")
LOG = "build_and_run.log"

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{datetime.now()} - {msg}\n")

def mtime(path):
    return os.path.getmtime(path) if os.path.exists(path) else 0

if mtime(SRC) > mtime(EXE):
    log("main.py changed -> rebuilding exe...")
    subprocess.run(["py", "-m", "PyInstaller", "--onefile", SRC], check=True)
else:
    log("No changes -> exe is up to date.")

if os.path.exists(EXE):
    log(f"Running {EXE} ...")
    subprocess.run([EXE], check=True)
else:
    log("ERROR: exe not found, build failed?")
