import os
import subprocess
import sys


def run_command(command):
    """Helper function to run a shell command and return its output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()


def process_file(filename):
    if filename.endswith('.pat'):
        pat_file = filename
        base_name = os.path.splitext(filename)[0]
    else:
        base_name = os.path.splitext(filename)[0]
        pat_file = f"{base_name}.pat"
        split_files = []

        print(f"Running pcf.exe {filename}")
        run_command(f".\\pcf.exe {filename}")

    print(f"Running sigmake_unlimit.exe {pat_file} {base_name}.sig")
    run_command(f".\\sigmake_unlimit.exe {pat_file} {base_name}.sig")
    
    exc_file = f"{base_name}.exc"
    if os.path.exists(exc_file):
        with open(exc_file, 'r') as exc:
            exc_lines = exc.readlines()
        with open(exc_file, 'w') as exc:
            length = len(exc_lines)-4
            for i, line in enumerate(exc_lines[4:len(exc_lines)], start=4):
                if  (i + 2) <= length and line == '\n' and i != len(exc_lines) - 1 and exc_lines[i + 2] != '\n':
                # if exc file not work sucessfully, try this
                # if line == '\n' and i != len(exc_lines) - 1 and exc_lines[i + 2] != '\n':
                    exc_lines[i + 1] = '+' + exc_lines[i + 1]
                exc.writelines(exc_lines[i])
        
    print(f"Re-running sigmake.exe {pat_file } {base_name}.sig")
    run_command(f".\\sigmake_unlimit.exe {pat_file} {base_name}.sig")  

    if os.path.exists(exc_file):
        with open(exc_file, 'r') as exc:
            exc_lines = exc.readlines()
        with open(exc_file, 'w') as exc:
            if exc_lines[length-1] != '\n':
                exc.writelines(exc_lines[:length] + exc_lines[length+4:])
            else:
                os._exit(0)

        print(f"Re-running sigmake.exe {pat_file } {base_name}.sig")
        run_command(f".\\sigmake_unlimit.exe {pat_file} {base_name}.sig")  
        
    print(f"Cleaning up temporary files...")
    os.remove(exc_file)
    os.remove(pat_file)
    

filename=sys.argv[1]
# usage: python.exe (file.lib or file.pat) name.sig
process_file(filename)
