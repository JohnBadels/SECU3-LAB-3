import subprocess
import ctypes
import sys
import os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def save_hive(hive, output_path):
    try:
        command = ['reg', 'save', hive, output_path, '/y']
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Successfully saved {hive} to {output_path}")
        if result.stderr:
            print(f"Errors:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while saving {hive}: {e}")
        print(f"Output:\n{e.output}")
        print(f"Errors:\n{e.stderr}")

def main():
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    hives = {
        'HKLM\\SAM': os.path.join(script_dir, 'sam'),
        'HKLM\\SECURITY': os.path.join(script_dir, 'security'),
        'HKLM\\SOFTWARE': os.path.join(script_dir, 'software'),
        'HKLM\\SYSTEM': os.path.join(script_dir, 'system'),
        'HKU\\.DEFAULT': os.path.join(script_dir, 'default')
    }

    if is_admin():
        for hive, output_path in hives.items():
            save_hive(hive, output_path)
    else:
        # Re-run the script with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

if __name__ == "__main__":
    main()
