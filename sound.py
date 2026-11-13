import io
import time
import threading
from gtts import gTTS
import pygame

pygame.mixer.init()

_speech_token = 0
_is_speaking = False
_mixer_lock = threading.Lock()
_audio_cache = {}


def is_speaking():
    """현재 음성을 불러오거나 재생 중인지 반환"""
    return _is_speaking


def stop():
    """재생 중인 소리를 즉시 멈춤"""
    global _speech_token, _is_speaking
    _speech_token += 1
    _is_speaking = False
    with _mixer_lock:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except Exception:
            pass


def _get_mp3_bytes(text, lang):
    key = (lang, text)
    if key in _audio_cache:
        return _audio_cache[key]

    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang=lang, timeout=5)
    tts.write_to_fp(mp3_fp)
    data = mp3_fp.getvalue()
    _audio_cache[key] = data
    return data


def _speak_worker(token, items):
    global _is_speaking
    try:
        for text, lang in items:
            if token != _speech_token:
                return
            try:
                audio_bytes = _get_mp3_bytes(text, lang)

                if token != _speech_token:
                    return

                with _mixer_lock:
                    if token != _speech_token:
                        return
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(io.BytesIO(audio_bytes))
                    pygame.mixer.music.play()

                # 오디오 장치 오류로 무한 대기하지 않도록 최대 10초 제한
                play_start = time.time()
                while True:
                    if token != _speech_token:
                        with _mixer_lock:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.unload()
                        return

                    with _mixer_lock:
                        busy = pygame.mixer.music.get_busy()

                    if not busy or (time.time() - play_start > 10.0):
                        break
                    time.sleep(0.05)

                with _mixer_lock:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.unload()

            except Exception:
                pass
    finally:
        if token == _speech_token:
            _is_speaking = False


def speak(kanji, furigana, meaning, use_jp=True, use_ko=False):
    global _is_speaking
    stop()

    items = []
    if use_jp:
        jp_text = furigana if furigana else kanji
        items.append((jp_text, "ja"))

    if use_ko:
        ko_text = meaning.replace("·", ", ")
        items.append((ko_text, "ko"))

    if items:
        _is_speaking = True
        t = threading.Thread(
            target=_speak_worker, args=(_speech_token, items), daemon=True
        )
        t.start()
