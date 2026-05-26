import subprocess, sys, pathlib
subprocess.check_call([sys.executable, str(pathlib.Path(__file__).with_name("download.py")), "--sample-only"])
