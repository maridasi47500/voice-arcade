import os
import json
import pychromecast
import speech_recognition as sr
import pyttsx3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class VoiceArcadeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Welcome to Voice Arcade!')
        layout.add_widget(self.label)
        
        # Add buttons for each game (disabled)
        games = ["True or False", "Santa's Helper", "Would You Rather", "Daily Quiz", "Triviaz Hero", "Star Commander", "The Fake News Game", "The Number Games"]
        for game in games:
            btn = Button(text=game, disabled=True)
            layout.add_widget(btn)
        
        return layout

    def on_start(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.setup_chromecast()
        self.load_credentials()
        self.start_voice_recognition()

    def setup_chromecast(self):
        # Connect to Nest Mini
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Bureau"])
        if not chromecasts:
            self.label.text += "\nNo Chromecast devices found."
            return
        self.chromecast = chromecasts[0]
        self.chromecast.wait()
        
        # Access the correct attribute names
        if not hasattr(self.chromecast, 'device'):
            self.label.text += "\nChromecast device info not found."
        else:
            device_info = self.chromecast.device
            self.label.text += f"\nConnected to {device_info.friendly_name} at {device_info.host}"

    def load_credentials(self):
        credentials_path = '/home/mary/.config/google-oauthlib-tool/credentials.json'
        if os.path.exists('token.json'):
            self.credentials = Credentials.from_authorized_user_file('token.json')
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                credentials_path, ['https://www.googleapis.com/auth/assistant-sdk-prototype'])
            self.credentials = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.credentials.to_json())
        if self.credentials.expired and self.credentials.refresh_token:
            self.credentials.refresh(Request())
            
    def start_voice_recognition(self):
        with sr.Microphone() as source:
            self.label.text = "Say something..."
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                self.label.text = f"You said: {text}"
                self.respond_vocally(text)
            except sr.UnknownValueError:
                self.label.text = "Sorry, I did not understand that."
            except sr.RequestError:
                self.label.text = "Could not request results; check your network connection."

    def respond_vocally(self, text):
        self.chromecast.media_controller.play_media(
            f'http://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q={text}', 'audio/mp3')
        self.chromecast.media_controller.block_until_active()
        self.engine.say(f"You said: {text}")
        self.engine.runAndWait()

if __name__ == '__main__':
    VoiceArcadeApp().run()

