# Voice Arcade

Voice Arcade is a Python application built with Kivy, utilizing speech recognition to create a voice-activated gaming experience. The application interacts with a Nest Mini via Chromecast to provide a unique hands-free gaming experience.

## Features

- Voice-activated commands to start different games
- Integration with Nest Mini for audio output
- A variety of built-in games:
  - True or False
  - Santa's Helper
  - Would You Rather
  - Daily Quiz
  - Triviaz Hero
  - Star Commander
  - The Fake News Game
  - The Number Games

## Requirements

- Python 3.x
- Kivy
- SpeechRecognition
- pyttsx3
- google-api-python-client
- pychromecast
- requests

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/voice-arcade.git
    cd voice-arcade
    ```

2. Create a virtual environment:
    ```sh
    python -m venv voice_arcade_env
    source voice_arcade_env/bin/activate  # Sur Windows, utilisez `voice_arcade_env\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Update the IP address in the `setup_chromecast` method in `voice_arcade.py` to match your Nest Mini:
    ```python
    self.chromecast = pychromecast.Chromecast("192.168.1.100")  # Remplacer par l'IP de ton Nest Mini
    ```

## Usage

1. Run the application:
    ```sh
    python voice_arcade.py
    ```

2. Use voice commands to start games. The supported games are:
    - True or False
    - Santa's Helper
    - Would You Rather
    - Daily Quiz
    - Triviaz Hero
    - Star Commander
    - The Fake News Game
    - The Number Games

# Nest Mini Voice Recognition and Control Script

This script allows you to use your Nest Mini as both a microphone and speaker over WiFi for voice recognition and playback using Google Assistant and PyChromecast.

## Prerequisites

- Python 3.x
- Google Cloud Project with Google Assistant API and Cloud Speech-to-Text API enabled
- OAuth 2.0 credentials from Google Cloud
- Nest Mini connected to the same WiFi network

## Setup Instructions

### 1. Google Cloud Project Setup

1. Create a new project on [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Assistant API** and **Cloud Speech-to-Text API**.

### 2. OAuth Credentials

1. Set up OAuth 2.0 credentials for your project.
2. Download the JSON file for your credentials.
Run the following command to authenticate with your OAuth 2.0 credentials:

sh

Copié
```sh
google-oauthlib-tool --client-secrets /path/to/your/credentials.json --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save --headless --device-code
```


### 3. Install Necessary Python Libraries

```sh
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-assistant-sdk[samples] google-cloud-speech pychromecast speechrecognition
```


First, activate your Python virtual environment:

```sh
source ~/voice_arcade_env/bin/activate

# voice-arcade
