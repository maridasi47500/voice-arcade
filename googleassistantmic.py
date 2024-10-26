import pychromecast
import speech_recognition as sr
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

CAST_IP = "192.168.1.10"  # Replace with your Nest Mini's IP address
credentials = '/path/to/your/credentials.json'

def process_event(event):
    if event.type == EventType.ON_END_OF_UTTERANCE:
        print('End of utterance detected.')
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        text = event.args['text']
        print(f'You said: {text}')
        with open("recognized_text.txt", "a") as file:
            file.write(text + "\n")
        chromecast.media_controller.play_media(
            f'http://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={text}',
            'audio/mp3'
        )
        chromecast.media_controller.block_until_active()
    elif event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT:
        print('Conversation timed out.')

try:
    chromecast = pychromecast.Chromecast(CAST_IP)
    chromecast.wait()
    device_info = chromecast.device
    print(f"Connected to {device_info.friendly_name} at {device_info.host}")
except Exception as e:
    print(f"An error occurred: {e}")

assistant = Assistant(credentials)
for event in assistant.start():
    process_event(event)

