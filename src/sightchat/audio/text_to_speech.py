from __future__ import annotations


class TextToSpeech:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def speak(self, text: str) -> bool:
        if not self.enabled or not text.strip():
            return False
        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception:
            return False
