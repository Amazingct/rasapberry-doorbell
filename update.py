import os
import time
user = "pi"
dir = "/home/{}".format(user)
wait = 15

# wait
time.sleep(wait)
# download
os.chdir(dir)
try:
    os.system("git clone https://github.com/Amazingct/rasapberry-doorbell")
except:
    os.system("sudo apt install git")

time.sleep(wait-5)
