import pychromecast
import speech_recognition as sr
import wave
r = sr.Recognizer()

CAST_IP = "192.168.1.10"

# Discover Chromecasts on the network
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Bureau"])

if len(chromecasts) == 0:
    print("No Chromecasts found")
    exit(1)

chromecast = chromecasts[0]
chromecast.wait()

device_info = chromecast.cast_info

# Debug: Print the type and value of device_info
print(f"Type of device_info: {type(device_info)}")
print(f"Value of device_info: {device_info}")

if hasattr(device_info, 'cast_type'):
    print(f"Connected to {device_info.friendly_name} at {device_info.host}")
else:
    print("The device_info object does not have a cast_type attribute.")

try:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        print("Audio captured successfully")

        # Save the audio to a file
        with open("captured_audio.wav", "wb") as file:
            file.write(audio.get_wav_data())

    try:
        recognized_text = r.recognize_google(audio)
        print("You said: " + recognized_text)

        # Write recognized text to a file
        with open("recognized_text.txt", "a") as file:
            file.write(recognized_text + "\n")
        
        chromecast.media_controller.play_media(
            f'http://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={recognized_text}',
            'audio/mp3'
        )
        chromecast.media_controller.block_until_active()
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        with open("recognized_text.txt", "a") as file:
            file.write("Could not understand audio\n")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        with open("recognized_text.txt", "a") as file:
            file.write(f"RequestError: {e}\n")
except Exception as e:
    print(f"An error occurred: {e}")

#Move to Nest Mini Later
#We can explore using the Nest Mini as a microphone through Google Assistant or other integrations later, but for now, let’s ensure your setup works with the internal mic.

#Does this help get things on track? 🎶✨ Ready for more tech adventures? 😊
