import pychromecast
import speech_recognition as sr
import pyaudio

# Replace with your Nest Mini's IP address
CAST_IP = "192.168.1.100"

# Connect to Nest Mini via IP
try:
    chromecast = pychromecast.Chromecast(CAST_IP)
    chromecast.wait()
    device_info = chromecast.device
    if device_info:
        print(f"Connected to {device_info.friendly_name} at {device_info.host}")
except AttributeError as e:
    print(f"AttributeError: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

# Initialize recognizer
r = sr.Recognizer()

# Use the default microphone for audio input
try:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
except Exception as e:
    print(f"Failed to initialize microphone: {e}")

# Transcribe audio using Google Speech Recognition
try:
    print("You said: " + r.recognize_google(audio))
    # Respond using Nest Mini
    try:
        chromecast.media_controller.play_media(
            'http://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=Hello%20from%20Voice%20Arcade',
            'audio/mp3'
        )
        chromecast.media_controller.block_until_active()
    except Exception as e:
        print(f"Failed to play media on Chromecast: {e}")
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

