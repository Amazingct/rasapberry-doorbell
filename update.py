import os
import time
user = "pi/Documents"
dir = "/home/{}".format(user)
wait = 0

# wait
time.sleep(wait)
# download
os.chdir(dir)
try:
    os.system("git clone https://github.com/Amazingct/rasapberry-doorbell")
    os.system("mv rasapberry-doorbell /home/pi")
except:
    os.system("sudo apt install git")
    os.system("git clone https://github.com/Amazingct/rasapberry-doorbell")
    os.system("mv rasapberry-doorbell /home/pi")

time.sleep(5)
