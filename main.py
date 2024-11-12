from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import speech_recognition as sr

class VoiceArcadeApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        
        welcome_label = Label(
            text="Welcome to Voice Arcade!",
            font_size='24sp',
            color=(1,1,1,1),
            size_hint_y=0.2
        )
        root.add_widget(welcome_label)
        
        game_buttons = BoxLayout(
            orientation='vertical',
            size_hint_y=0.8
        )
        root.add_widget(game_buttons)
        
        games = ["True or False", "Santa's Helper", "Would You Rather", "Daily Quiz", "Triviaz Hero", "Star Commander", "The Fake News Game", "The Number Games"]

        self.buttons = {}
        for game in games:
            btn = Button(text=game, size_hint_y=None, height='48dp')
            btn.bind(on_release=self.on_button_release)
            game_buttons.add_widget(btn)
            self.buttons[game.lower()] = btn

        self.recognizer = sr.Recognizer()
        self.listen_for_commands()
        return root

    def on_button_release(self, instance):
        print(f"You selected: {instance.text}")

    def listen_for_commands(self):
        try:
            with sr.Microphone() as source:
                print("Say the name of the game you want to select!")
                audio = self.recognizer.listen(source)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                if command in self.buttons:
                    self.buttons[command].trigger_action(duration=0.1)
                else:
                    print("Command not recognized. Please try again.")
        except sr.UnknownValueError:
            print("Google Web Speech could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech service; {e}")

if __name__ == '__main__':
    VoiceArcadeApp().run()

