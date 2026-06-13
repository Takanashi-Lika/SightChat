from __future__ import annotations


class SpeechToText:
    def listen_once(self, language: str = "zh-CN") -> str:
        try:
            import speech_recognition as sr

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            return recognizer.recognize_google(audio, language=language)
        except Exception as exc:
            raise RuntimeError(f"语音识别失败：{exc}") from exc
