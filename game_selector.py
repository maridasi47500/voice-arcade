import pychromecast
import speech_recognition as sr
import pyttsx3
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class VoiceArcadeApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Welcome to Voice Arcade!')
        layout.add_widget(self.label)

        # Ajouter des boutons pour chaque jeu (désactivés)
        games = ["True or False", "Santa's Helper", "Would You Rather", "Daily Quiz", "Triviaz Hero", "Star Commander", "The Fake News Game", "The Number Games"]
        for game in games:
            btn = Button(text=game, disabled=True)
            layout.add_widget(btn)
        
        return layout

    def on_start(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.setup_chromecast()
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
    

    def start_voice_recognition(self):
        with sr.Microphone() as source:
            self.label.text = "Say something..."
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                self.label.text = f"You said: {text}"
                self.respond_to_command(text)
            except sr.UnknownValueError:
                self.label.text = "Sorry, I didn't catch that."
        
        # Restart listening for voice commands
        self.start_voice_recognition()

    def respond_to_command(self, command):
        if command.lower() in ["true or false", "santa's helper", "would you rather", "daily quiz", "triviaz hero", "star commander", "the fake news game", "the number games"]:
            self.label.text = f"Starting game: {command}"
            self.engine.say(f"Starting game {command}")
            self.engine.runAndWait()
            self.chromecast.media_controller.play_media('http://path_to_audio_file', 'audio/mp3')
            self.chromecast.media_controller.block_until_active()
            # Confirmation vocale que le jeu a été lancé
            self.engine.say(f"The game {command} has started.")
            self.engine.runAndWait()

        else:
            self.engine.say("Unknown game command")
            self.engine.runAndWait()
        
if __name__ == '__main__':
    VoiceArcadeApp().run()

