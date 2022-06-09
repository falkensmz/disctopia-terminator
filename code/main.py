import os
import sys
import subprocess as sp
from shutil import rmtree

header = """
    ____  _           __              _                 
   / __ \(_)_________/ /_____  ____  (_)___ _           
  / / / / / ___/ ___/ __/ __ \/ __ \/ / __ `/           
 / /_/ / (__  ) /__/ /_/ /_/ / /_/ / / /_/ /            
/_____/_/____/\___/\__/\____/ .___/_/\__,_/             
  ______                   /_/            __            
 /_  __/__  _________ ___  (_)___  ____ _/ /_____  _____
  / / / _ \/ ___/ __ `__ \/ / __ \/ __ `/ __/ __ \/ ___/
 / / /  __/ /  / / / / / / / / / / /_/ / /_/ /_/ / /    
/_/  \___/_/  /_/ /_/ /_/_/_/ /_/\__,_/\__/\____/_/     
                                                        
                                                                                                                                                                                    
Version: 1.0.0                                                                               
"""

def check_registry():
    print("[+] Checking for registry key...")
    key = r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run\update'
    result = sp.Popen(f"reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
    out, err = result.communicate()
    result.wait()
    if err:
        return False
    else:
        return True

def check_config():
    print("[+] Checking for config file...")
    USERNAME = os.environ.get("USERNAME")
    if os.path.exists(fr'C:\Users\{USERNAME}\.config'):
        return True
    else:
        return False

def check_peristence():
    print("[+] Checking for persistence...\n")
    if os.path.exists(os.environ["appdata"] + "\\Windows-Updater.exe"):
        return True
    else:
        return False

def check_processes():
    print(f"[+] Checking for processes...")
    result = sp.Popen(f"tasklist", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
    out, err = result.communicate()
    result.wait()
    if "Windows-Updater.exe" in out:
        return True
    else:
        return False

print(header)

registry = check_registry()
config = check_config()
processes = check_processes()
persistence = check_peristence()

if registry or config or processes or persistence:
    print("[!] Disctopia-C2 has been detected on the system.\n")
    choice = input("[?] Do you want to permanently delete Disctopia-c2 from the system? (Y/N): ")
    if choice == "Y":
        print("\n[+] Deleting Disctopia-C2 from the system...")

        USERNAME = os.environ.get("USERNAME")

        if registry:
            try:
                sp.call('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /f', shell=True)
            except Exception as e:
                print(f"An error has occured : {e}")

        if config:
            try:
                rmtree(fr'C:\Users\{USERNAME}\.config')
            except Exception as e:
                print(f"An error has occured : {e}")

        if persistence:
            try:
                os.remove(os.environ["appdata"] + "\\Windows-Updater.exe")
            except Exception as e:
                print(f"An error has occured : {e}")

        if processes:
            try:
                sp.Popen(f"taskkill /IM Windows-Updater.exe ", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
            except Exception as e:
                print(f"An error has occured : {e}")

        print("\n[!] Threat has been neutralized successfully.")
        print("[+] Thank you for using disctopia-terminator\n")
        input("[ENTER] to exit")
        sys.exit()

    elif choice == "N":
        print("[+] Thank you for using disctopia-terminator\n")
        input("[ENTER] to exit")
        sys.exit()
    else:
        print("[!] Invalid input\n", 'red')
        input("[ENTER] to exit")
        sys.exit()
else:
    print("[!] Disctopia-C2 has not been detected on the system.")
    print("Thank you for using disctopia-terminator\n")
    input("[ENTER] to exit")
    sys.exit()