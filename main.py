#/usr/bin/python3
sent_sms = 0
DOORBELL_PIN = 26
DOORBELL_SCREEN_ACTIVE_S = 120
JITSI_ID = "doorbellring12345"
RING_SFX_PATH = None
ENABLE_EMAIL = False
import tkinter
window = tkinter.Tk()
window.title("GUI")
label = tkinter.Label(window, text = "DOORBELL< WELCOME").pack()
from twilio.rest import Client
import time
import os
import signal
import subprocess
from vlc import MediaPlayer

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, 1)
except :
    print("Error importing RPi.GPIO. This is probably because you need superuser. Try running again with 'sudo'.")


def show_screen():
    pass

def hide_screen():
    pass

def send_sms(link):
    global sent_sms
    if sent_sms == 0:
        account_sid = 'AC7cab1dd6c21df2e084f59bd0c10e9d84'
        auth_token = '4056b5a5fe68586d03a0cc22ed1b022b'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            messaging_service_sid='MG636d6da0db1c920d83f1eb29d4729a66',
            body="Doorbell: Join meeting using link: {}".format(link),
            to='+2348168864021'
        )



def ring_doorbell(pin):
    global sent_sms
    chat_id = JITSI_ID
    video_chat = VideoChat(chat_id)
    MediaPlayer("/home/pi/rasapberry-doorbell/ring.mp3").play()
    send_sms(video_chat.get_chat_url())
    show_screen()
    video_chat.start()
    sent_sms = 1
    time.sleep(DOORBELL_SCREEN_ACTIVE_S)
    video_chat.end()
    sent_sms = 0
    hide_screen()


class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None

    def get_chat_url(self):
        return "http://meet.jit.si/%s" % self.chat_id

    def start(self):
        if not self._process and self.chat_id:
            self._process = subprocess.Popen(["chromium-browser","-kiosk", self.get_chat_url()])
        else:
            print("Can't start video chat -- already started or missing chat id")

    def end(self):
        if self._process:
            os.kill(self._process.pid, signal.SIGTERM)


class Doorbell:
    def __init__(self, doorbell_button_pin):
        self._doorbell_button_pin = doorbell_button_pin

    def run(self):
        try:

            print("Starting Doorbell...")
            hide_screen()
            self._setup_gpio()
            print("Waiting for doorbell rings...")
            self._wait_forever()

        except KeyboardInterrupt:
            print("Safely shutting down...")

        finally:
            self._cleanup()

    def _wait_forever(self):
            window.mainloop()
            time.sleep(0.1)

    def _setup_gpio(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._doorbell_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(self._doorbell_button_pin, GPIO.RISING, callback=ring_doorbell, bouncetime=2000)
        except:
            pass

    def _cleanup(self):
        try:
            GPIO.cleanup(self._doorbell_button_pin)
            show_screen()
        except:
            pass

doorbell = Doorbell(DOORBELL_PIN)
doorbell.run()




