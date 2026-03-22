import sys
import os
import platform
import json
import urllib.request
import zipfile
import tarfile
import subprocess
import shutil

def get_latest_version():
    """Fetch latest release metadata from GitHub API."""
    api_url = "https://api.github.com/repos/Gentleman-Programming/engram/releases/latest"
    # Using a custom User-Agent to avoid potential blocks by GitHub API
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Memory-Orchestrator-Skill'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def download_and_extract(url, dest_dir):
    """Download and extract ZIP or TAR.GZ archive."""
    os.makedirs(dest_dir, exist_ok=True)
    suffix = ".zip" if url.endswith(".zip") else ".tar.gz"
    temp_file = os.path.join(dest_dir, f"engram_download{suffix}")
    
    print(f"📥 Downloading from {url}...")
    urllib.request.urlretrieve(url, temp_file)
    
    if suffix == ".zip":
        print("📦 Extracting ZIP...")
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
    else:
        print("📦 Extracting TAR.GZ...")
        with tarfile.open(temp_file, "r:gz") as tar_ref:
            tar_ref.extractall(dest_dir)
            
    os.remove(temp_file)

def get_engram_path():
    """Determine the path to the engram binary within the skill folder."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bin_dir = os.path.join(base_dir, "bin")
    exe_name = "engram.exe" if platform.system() == "Windows" else "engram"
    return os.path.join(bin_dir, exe_name)

def init():
    """Initialize memory: check and download binary if missing."""
    engram_path = get_engram_path()
    bin_dir = os.path.dirname(engram_path)
    
    if not os.path.exists(engram_path):
        print("🚀 Engram binary not found. Starting automatic acquisition for multiple platforms...")
        try:
            latest = get_latest_version()
            tag = latest["tag_name"]
            
            system = platform.system().lower()
            # Canonicalize OS names
            if system == "darwin": system = "darwin"
            elif system == "linux": system = "linux"
            elif system == "windows": system = "windows"
            
            machine = platform.machine().lower()
            # Canonicalize architectures
            if machine in ["amd64", "x86_64"]: arch = "amd64"
            elif machine in ["arm64", "aarch64"]: arch = "arm64"
            else: arch = machine
            
            # Format expected matches: engram_v1.9.9_linux_amd64.tar.gz
            # Since naming might vary slightly, we look for matches of system and arch
            asset = None
            for a in latest["assets"]:
                name = a["name"].lower()
                if system in name and arch in name:
                    asset = a
                    break
            
            if not asset:
                # Fallback search if arch varies (e.g. x86_64 vs amd64)
                print(f"⚠️ Precise match not found for {system}_{arch}. Searching for nearest...")
                for a in latest["assets"]:
                    if system in a["name"].lower():
                        asset = a
                        break
                        
            if asset:
                download_and_extract(asset["browser_download_url"], bin_dir)
                
                # Check if it was extracted correctly
                if not os.path.exists(engram_path):
                    # Search for the binary in case it was in a subfolder or named differently
                    exe_to_search = "engram.exe" if system == "windows" else "engram"
                    for root, _, files in os.walk(bin_dir):
                        for f in files:
                            if f == exe_to_search:
                                shutil.move(os.path.join(root, f), engram_path)
                                break
                
                # Ensure executable permissions on Unix-like systems
                if os.name != "nt" and os.path.exists(engram_path):
                    os.chmod(engram_path, 0o755)
                
                print(f"✅ Engram {tag} is ready at {engram_path}")
                # Print version to verify
                subprocess.run([engram_path, "version"], check=True)
            else:
                print(f"❌ Could not find a suitable asset for your system ({system} {arch}) in latest release.")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            sys.exit(1)
    else:
        print("✅ Engram is already available.")

def run_engram(*args):
    """Run an Engram command, initializing if necessary."""
    engram_path = get_engram_path()
    if not os.path.exists(engram_path):
        init()
    
    cmd = [engram_path] + list(args)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Engram command failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python memory.py <command> [args]")
        print("Commands: init, save_context, get_context, context, finalize_session, stats")
        sys.exit(1)
        
    cmd = sys.argv[1]
    
    if cmd == "init":
        init()
    elif cmd == "save_context":
        if len(sys.argv) < 4:
            print("Usage: python memory.py save_context <title> <message>")
            sys.exit(1)
        run_engram("save", sys.argv[2], sys.argv[3])
    elif cmd == "get_context":
        if len(sys.argv) < 3:
            print("Usage: python memory.py get_context <query>")
            sys.exit(1)
        run_engram("search", sys.argv[2])
    elif cmd == "context":
        run_engram("context")
    elif cmd == "finalize_session":
        if len(sys.argv) < 3:
            print("Usage: python memory.py finalize_session <summary>")
            sys.exit(1)
        run_engram("save", "Session Summary", sys.argv[2], "--topic", "session_summary")
    elif cmd == "stats":
        run_engram("stats")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
