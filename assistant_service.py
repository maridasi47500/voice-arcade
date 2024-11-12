


import os
import json
import pyaudio
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_assistant_sdk.api_v1alpha2 import EmbeddedAssistantClient
from google_assistant_sdk.api_v1alpha2 import embedded_assistant_pb2

# Path to your credentials
credentials_path = '/home/mary/.config/google-oauthlib-tool/credentials.json'

# Load credentials
def load_credentials(credentials_path):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            from google_auth_oauthlib.flow import InstalledAppFlow
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                ['https://www.googleapis.com/auth/assistant-sdk-prototype']
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Connect to Google Assistant Service
credentials = load_credentials(credentials_path)
assistant = EmbeddedAssistantClient(credentials=credentials)

def assistant_request(text_query):
    audio = pyaudio.PyAudio()
    request = embedded_assistant_pb2.AssistRequest(
        config=embedded_assistant_pb2.AssistConfig(
            audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                encoding=embedded_assistant_pb2.AudioOutConfig.LINEAR16,
                sample_rate_hertz=16000
            ),
            text_query=text_query,
            device_config=embedded_assistant_pb2.DeviceConfig(
                device_id='2KGSPJ',
                device_model_id='H2C'
            )
        )
    )

    response = assistant.assist(request)
    for event in response:
        if event.speech_results:
            print('Transcript: ', event.speech_results[0].transcript)
            with open("recognized_text.txt", "a") as file:
                file.write(event.speech_results[0].transcript + "\n")
            print(f'Repeating: {event.speech_results[0].transcript}')
        if event.dialog_state_out.supplemental_display_text:
            print('Response: ', event.dialog_state_out.supplemental_display_text)
        if event.audio_out.audio_data:
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, output=True)
            stream.write(event.audio_out.audio_data)
            stream.stop_stream()
            stream.close()
    audio.terminate()

# Example usage:
assistant_request("What's the weather like today?")

