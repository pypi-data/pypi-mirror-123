import subprocess
def kill_process(pid):
    subprocess.Popen("TASKKILL /F /PID {pid} /T".format(pid=pid))