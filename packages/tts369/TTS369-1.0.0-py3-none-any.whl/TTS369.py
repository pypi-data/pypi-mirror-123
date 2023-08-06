import pyttsx3


class TTS:
    def __init__(self, message):
        self.message = message

    def say(self):
        pyttsx3.speak(self.message)
