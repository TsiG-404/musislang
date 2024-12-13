import subprocess
import os

def open_cmd_and_run(script_name):
    # Construct the full command to open cmd and run the Python script
    command = f'start cmd /k "python {script_name}"'
    # Execute the command
    subprocess.run(command, shell=True)

def main():
    scripts = ["app.py", "lyrics.py", "kara.py"]

    for script in scripts:
        if not os.path.exists(script):
            print(f"Warning: {script} does not exist in the current directory.")

    # Open Command Prompt windows for each script
    for script in scripts:
        open_cmd_and_run(script)

if __name__ == "__main__":
    main()
