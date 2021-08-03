
DOORBELL_PIN = 26
DOORBELL_SCREEN_ACTIVE_S = 60
JITSI_ID = "Home-Doorbell"
RING_SFX_PATH = None

import time
import os
import signal
import subprocess
import uuid



try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19, GPIO.OUT)
    GPIO.output(19, 1)

except RuntimeError:
    print("Error importing RPi.GPIO. This is probably because you need superuser. Try running again with 'sudo'.")


def show_screen():
    # os.system("tvservice -p")
    # os.system("xset dpms force on")
    pass

def hide_screen():
    # os.system("tvservice -o")
    pass


def send_notification(chat_url):
    message = "Someone at the door, use link to view video {}".format(chat_url)
    # send notification here


def ring_doorbell(pin):
    SoundEffect(RING_SFX_PATH).play()
    chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
    video_chat = VideoChat(chat_id)
    send_notification(video_chat.get_chat_url())
    show_screen()
    video_chat.start()
    time.sleep(DOORBELL_SCREEN_ACTIVE_S)
    video_chat.end()
    hide_screen()


class SoundEffect:
    def __init__(self, filepath):
        self.filepath = filepath

    def play(self):
        if self.filepath:
            subprocess.Popen(["aplay", self.filepath])


class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None

    def get_chat_url(self):
        return "http://meet.jit.si/%s" % self.chat_id

    def start(self):
        if not self._process and self.chat_id:
            self._process = subprocess.Popen(["chromium-browser", "-kiosk", self.get_chat_url()])
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


if __name__ == "__main__":
    doorbell = Doorbell(DOORBELL_PIN)
    doorbell.run()
