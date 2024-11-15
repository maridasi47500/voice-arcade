import pychromecast
import speech_recognition as sr

CAST_IP = "192.168.1.10"

try:
    chromecast = pychromecast.Chromecast(CAST_IP)
    chromecast.wait()
    device_info = chromecast.device
    print(f"Connected to {device_info.friendly_name} at {device_info.host}")
except Exception as e:
    print(f"An error occurred: {e}")

r = sr.Recognizer()
try:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        print("Audio captured successfully")

    print("You said: " + r.recognize_google(audio))
    chromecast.media_controller.play_media(
        'http://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=Hello%20from%20Voice%20Arcade',
        'audio/mp3'
    )
    chromecast.media_controller.block_until_active()
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
except Exception as e:
    print(f"An error occurred: {e}")

