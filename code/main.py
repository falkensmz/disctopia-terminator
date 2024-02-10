import os
import sys
import subprocess
from shutil import rmtree

header = """
______           _              _         _                      _             _             
|  _  \         | |            (_)       | |                    (_)           | |            
| | | |_   _ ___| |_ ___  _ __  _  __ _  | |_ ___ _ __ _ __ ___  _ _ __   __ _| |_ ___  _ __ 
| | | | | | / __| __/ _ \| '_ \| |/ _` | | __/ _ \ '__| '_ ` _ \| | '_ \ / _` | __/ _ \| '__|
| |/ /| |_| \__ \ || (_) | |_) | | (_| | | ||  __/ |  | | | | | | | | | | (_| | || (_) | |   
|___/  \__, |___/\__\___/| .__/|_|\__,_|  \__\___|_|  |_| |_| |_|_|_| |_|\__,_|\__\___/|_|   
        __/ |            | |                                                                 
       |___/             |_|                                                                 
"""

def run_command(command):
    """Executes a shell command and returns its output and error."""
    result = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, text=True)
    return result.stdout, result.stderr

def check_registry():
    print("[+] Checking for registry key...")
    out, err = run_command("reg query HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update")
    return not err

def check_config():
    print("[+] Checking for config file...")
    config_path = os.path.join(os.environ.get("USERPROFILE"), ".config")
    return os.path.exists(config_path)

def check_persistence():
    print("[+] Checking for persistence...\n")
    updater_path = os.path.join(os.environ.get("APPDATA"), "Windows-Updater.exe")
    return os.path.exists(updater_path)

def check_processes():
    print("[+] Checking for processes...")
    out, err = run_command("tasklist")
    return "Windows-Updater.exe" in out

print(header)

checks = [check_registry(), check_config(), check_persistence(), check_processes()]

if any(checks):
    print("[!] Disctopia-C2 has been detected on the system.\n")
    if input("[?] Do you want to permanently delete Disctopia-C2 from the system? (Y/N): ").upper() == "Y":
        print("\n[+] Deleting Disctopia-C2 from the system...")
        if checks[0]:  # Registry
            subprocess.call('reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v update /f', shell=True)

        if checks[1]:  # Config
            rmtree(os.path.join(os.environ.get("USERPROFILE"), ".config"))

        if checks[2]:  # Persistence
            os.remove(os.path.join(os.environ.get("APPDATA"), "Windows-Updater.exe"))

        if checks[3]:  # Processes
            subprocess.run("taskkill /IM Windows-Updater.exe /F", shell=True)

        print("\n[!] Threat has been neutralized successfully.")
    else:
        print("[+] Exiting without changes.")
else:
    print("[!] Disctopia-C2 has not been detected on the system.")

print("Thank you for using disctopia-terminator\n")
input("[ENTER] to exit")
sys.exit()
