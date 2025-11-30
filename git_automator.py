import time
import subprocess
import os
import json
from datetime import datetime
import sys

# Config
REPO_ROOT = os.getcwd()
LOG_FILE = "VERSION_LOG.md"
VERSION_FILE = ".version_tracker.json"

def run(cmd):
    try:
        # print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def get_track(filename):
    # Normalize path separators
    filename = filename.replace('\\', '/')
    parts = filename.split('/')
    if len(parts) > 1:
        # e.g. "notebooks/01.ipynb" -> "track/notebooks"
        return f"track/{parts[0]}"
    # Root files
    return "track/root"

def load_versions():
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_versions(data):
    with open(VERSION_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def update_log(track, version, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"| {track} | {version} | {message} | {timestamp} |\n"
    
    with open(LOG_FILE, 'a') as f:
        f.write(entry)

def main():
    print("GitOps Automation Started...")
    print("Monitoring for changes...")
    
    # Initial Pull to sync
    run("git pull --rebase origin main")

    while True:
        try:
            status = run("git status --porcelain")
            if status:
                lines = status.split('\n')
                # Process only the first change to ensure atomic handling, then loop again
                for line in lines:
                    if not line.strip(): continue
                    
                    parts = line.strip().split(maxsplit=1)
                    if len(parts) < 2: continue
                    
                    # parts[0] is status (M, ??, etc), parts[1] is filename
                    # Handle quoted filenames
                    filename = parts[1].strip('"')
                    
                    # Ignore metadata files to prevent loops
                    if filename in [LOG_FILE, VERSION_FILE, "git_automator.py"]:
                        continue
                        
                    print(f"Detected change in: {filename}")
                    
                    versions = load_versions()
                    track = get_track(filename)
                    
                    # Update Version
                    if track not in versions:
                        versions[track] = {"major": 1, "minor": 0}
                    else:
                        versions[track]["minor"] += 1
                    
                    v_major = versions[track]["major"]
                    v_minor = versions[track]["minor"]
                    version_str = f"v{v_major}.{v_minor}"
                    branch_name = f"{track}/{version_str}"
                    
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    msg = f"auto:{timestamp} — {filename}"
                    
                    # 1. Add the file
                    run(f'git add "{filename}"')
                    
                    # 2. Commit
                    run(f'git commit -m "{msg}"')
                    
                    # 3. Create/Update Branch for this version
                    run(f"git branch -f {branch_name}")
                    
                    # 4. Update Log & Tracker
                    update_log(track, version_str, msg)
                    save_versions(versions)
                    
                    run(f'git add "{LOG_FILE}" "{VERSION_FILE}"')
                    run(f'git commit -m "docs: update version log for {version_str}"')
                    
                    # 5. Push
                    print(f"Pushing {branch_name} and main...")
                    run("git push origin main")
                    run(f"git push -f origin {branch_name}")
                    
                    # Break after processing one file to re-evaluate status
                    break
            
            time.sleep(2)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error in loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
