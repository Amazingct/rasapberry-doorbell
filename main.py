sent_sms = 0
DOORBELL_PIN = 26
DOORBELL_SCREEN_ACTIVE_S = 200
JITSI_ID = "doorbellring12345"
RING_SFX_PATH = None
ENABLE_EMAIL = False

from twilio.rest import Client
import time
import os
import signal
import subprocess
import uuid
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
        account_sid = 'AC6bc78afd56470c418c040315901b6fd2'
        auth_token = 'f3c2672a0ca2ea2808d57dd63f428d3e'
        client = Client(account_sid, auth_token)
        client.messages.create(body="Doorbell: Join meeting using link: {}".format(link),from_='+15203896643', to='+2348051230116').sid


def ring_doorbell(pin):
    global sent_sms
    chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
    video_chat = VideoChat(chat_id)
    MediaPlayer("ring.mp3").play()
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
        while True:
            time.sleep(0.1)

    def _setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._doorbell_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self._doorbell_button_pin, GPIO.RISING, callback=ring_doorbell, bouncetime=2000)

    def _cleanup(self):
        GPIO.cleanup(self._doorbell_button_pin)
        show_screen()


doorbell = Doorbell(DOORBELL_PIN)
doorbell.run()
#ring_doorbell(1)


