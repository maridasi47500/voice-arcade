import pychromecast
import speech_recognition as sr
import pyaudio

# Remplacez par l'adresse IP de votre Nest Mini
CAST_IP = "192.168.1.100"

# Connectez-vous au Nest Mini via IP
chromecast = pychromecast.Chromecast(CAST_IP)
chromecast.wait()

# Vérifiez la connexion
cast_info = chromecast.device
if cast_info and hasattr(cast_info, 'cast_type'):
    print(f"Connecté à {cast_info.friendly_name} à {cast_info.host}")

# Initialiser le reconnaisseur
r = sr.Recognizer()

# Utiliser le microphone par défaut pour l'entrée audio
with sr.Microphone() as source:
    print("Dites quelque chose !")
    audio = r.listen(source)

# Transcrire l'audio en utilisant la reconnaissance vocale de Google
try:
    print("Vous avez dit : " + r.recognize_google(audio))
    # Répondre en utilisant le Nest Mini
    chromecast.media_controller.play_media(
        'http://translate.google.com/translate_tts?ie=UTF-8&tl=en&client=tw-ob&q=Bonjour%20de%20Voice%20Arcade',
        'audio/mp3'
    )
    chromecast.media_controller.block_until_active()
except sr.UnknownValueError:
    print("Google Speech Recognition ne pouvait pas comprendre l'audio")
except sr.RequestError as e:
    print(f"Impossible de demander des résultats au service de reconnaissance vocale de Google ; {e}")
except Exception as e:
    print(f"Une erreur inattendue s'est produite : {e}")

