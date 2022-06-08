    from tempfile import TemporaryFile
    import discord_webhook
    import os
    import sys
    import subprocess as sp
    from shutil import rmtree

    def check_registry():
        key = r'HKCU\Software\Microsoft\Windows\CurrentVersion\Run\update'
        result = sp.Popen(f"reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
        out, err = result.communicate()
        result.wait()
        if err:
            return False
        else:
            return True

    def check_config():
        USERNAME = os.environ.get("USERNAME")
        if os.path.exists(fr'C:\Users\{USERNAME}\.config'):
            return True
        else:
            return False

    def check_peristence():
        if os.path.exists(os.environ["appdata"] + "\\Windows-Updater.exe"):
            return True
        else:
            return False

    def check_processes():
        result = sp.Popen(f"tasklist", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
        out, err = result.communicate()
        result.wait()
        if "Windows-Updater.exe" in out:
            return True
        else:
            return False

    registry = check_registry()
    config = check_config()
    processes = check_processes()
    persistence = check_peristence()

    if check_registry() or check_config() or check_processes() or check_peristence():
        print("Disctopia-C2 was detected on the system.")
        choice = input("Do you want to permanently delete Disctopia-c2 from the system? (Y/N): ")
        if choice == "Y" or "y" or "YES" or "yes":

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

            print("Threat has been neutralized successfully.")
            sys.exit()

        else:
            print("Thank you for using disctopia-terminator")
            print("Exiting ...")
            sys.exit()
