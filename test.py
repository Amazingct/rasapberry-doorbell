JITSI_ID = "Home-Doorbell"
import time
import os
import signal
import subprocess
import uuid


def ring_doorbell():
    chat_id = JITSI_ID if JITSI_ID else str(uuid.uuid4())
    video_chat = VideoChat(chat_id)
    video_chat.start()
    time.sleep(60)
    video_chat.end()

class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None

    def get_chat_url(self):
        return "http://meet.jit.si/%s" % self.chat_id

    def start(self):
        if not self._process and self.chat_id:
            self._process = subprocess.Popen(["firefox", "-kiosk", self.get_chat_url()])
        else:
            print("Can't start video chat -- already started or missing chat id")

    def end(self):
        if self._process:
            os.kill(self._process.pid, signal.SIGTERM)

try:
    print("Starting Doorbell...")
    print("Waiting for doorbell rings...")
    ring_doorbell()


except KeyboardInterrupt:
    print("Safely shutting down...")





