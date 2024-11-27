import pygame
from PIL import Image
import speech_recognition as sr
import requests
import base64
import os
import google.generativeai as genai
import playsound
import threading
import string
import webbrowser
from config.api_keys import GOOGLE_API_KEY, GOOGLE_TTS  # Import keys from config file
from config.keywords import appointment_kw, directions_kw, locations_kw  # Import keywords for appointment
# https://docs.google.com/forms/d/e/1FAIpQLScUxWD43CuS1yu5PWTZmwPMAYypFzMi96_qZfhrOBJDYKbBUQ/viewform?usp=sf_link
# Configure Google API
genai.configure(api_key=GOOGLE_API_KEY)

# Configuration for Gemini model
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 500,
}
model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=generation_config)

# Global variables
in_greeting_zone = False
stop_animation = threading.Event()  # Global flag to stop animation

# Utility Functions
def load_gif_frames(gif_path):
    """Load GIF frames safely."""
    gif = Image.open(gif_path)
    frames = []
    try:
        while True:
            frames.append(
                pygame.image.fromstring(
                    gif.convert("RGBA").tobytes(), gif.size, "RGBA"
                )
            )
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames


def google_tts_speak(text):
    """Use Google Text-to-Speech to generate speech."""
    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_TTS}"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "input": {"text": text},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Wavenet-F",
            "ssmlGender": "FEMALE"
        },
        "audioConfig": {"audioEncoding": "MP3"}
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    if 'audioContent' in response_data:
        file_path = os.path.abspath("output.mp3")
        with open(file_path, "wb") as out:
            out.write(base64.b64decode(response_data['audioContent']))
            print(f"Audio content saved as '{file_path}'")
    else:
        print("Error with TTS response:", response_data)


def play_audio(file_path):
    """Play audio file while ensuring the file exists."""
    if os.path.exists(file_path):
        playsound.playsound(file_path)
        os.remove(file_path)  # Remove the file after playing
    else:
        print(f"File {file_path} does not exist. Cannot play audio.")


# Animation Functions
def blink_animation(screen, blink_frames, neutral_face):
    """Perform blinking animation."""
    for frame in blink_frames:
        screen.blit(frame, (0, 0))
        pygame.display.flip()
        pygame.time.delay(200)
    screen.blit(neutral_face, (0, 0))


def talk_animation(screen, talk_frames, neutral_face):
    """Perform talking animation."""
    while not stop_animation.is_set():
        for frame in talk_frames:
            if stop_animation.is_set():
                break
            screen.blit(frame, (0, 0))
            pygame.display.flip()
            pygame.time.delay(150)
    screen.blit(neutral_face, (0, 0))
    pygame.display.flip()


def talk_with_animation(text, screen, talk_frames, neutral_face):
    """Handle talking and animation simultaneously."""
    global stop_animation
    file_path = os.path.abspath("output.mp3")
    google_tts_speak(text)

    if not os.path.exists(file_path):
        print("Audio file was not created. Skipping playback.")
        return

    stop_animation.clear()
    animation_thread = threading.Thread(target=talk_animation, args=(screen, talk_frames, neutral_face))
    audio_thread = threading.Thread(target=play_audio, args=(file_path,))

    animation_thread.start()
    audio_thread.start()

    audio_thread.join()
    stop_animation.set()
    animation_thread.join()


# Greeting Functions
def respond_greeting():
    """Generate the greeting response text."""
    return "Hi there! I'm Telebot3 the receptionist. Are you here for an appointment, or do you need directions?"

def greeting_zone(screen, talk_frames, neutral_face):
    """Simulate greeting zone detection."""
    global in_greeting_zone
    if not in_greeting_zone:
        in_greeting_zone = True
        print("Simulated: User detected in the greeting zone.")
        greeting_text = respond_greeting()
        talk_with_animation(greeting_text, screen, talk_frames, neutral_face)
        handle_user_response(screen, talk_frames, neutral_face)
        in_greeting_zone = False

# User Response Handling
def book_appointment(response):
    """Check if the user's response indicates a desire to make an appointment."""
    for keyword in appointment_kw:
        if keyword in response.lower():
            return True
    return False

def directions(response):
    """Check if the user's response indicates a desire to look for directions."""
    for keyword in directions_kw:
        return True
    return False

def location(location):
    """Generate a location-specific response."""
    location_map = {
        "conference room": "The conference room is located on the second floor, third door on your right.",
        "cafeteria": "The cafeteria is located on the first floor, down the hall by Starbucks.",
        "lobby": "Oh! The lobby is right here! Behind me is the front desk, and behind you is the seating area.",
        "reception": "The reception area is right here! Behind me is the front desk, and behind you is the seating area.",
        "restroom": "The restroom is down the hall, to the left.",
        "bathroom": "The bathroom is down the hall, to the left.",
        "meeting": "the meeting Room is on the second floor, last door down the hall.",
    }
    # Return the matching response or a default message if the location is not found
    return location_map.get(location, f"I'm sorry, but '{location}' is not located in this building.")

def handle_user_response(screen, talk_frames, neutral_face):
    """Handle the user's response after greeting."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening for user response...")
            audio = recognizer.listen(source, timeout=5)
            user_response = recognizer.recognize_google(audio).lower().strip()
            print(f"User said: {user_response}")
            
            response_text = ""

            # Check if the user wants to book an appointment
            if book_appointment(user_response):
                talk_with_animation("Okay! You're here for an appointment. Please fill out the form on the screen and let me know when youre done.", screen, talk_frames, neutral_face)
                form_url = "https://docs.google.com/forms/d/e/1FAIpQLScUxWD43CuS1yu5PWTZmwPMAYypFzMi96_qZfhrOBJDYKbBUQ/viewform?usp=sf_link"  # Replace with your form URL
                webbrowser.open(form_url)

                    # Wait for user confirmation
                while True:
                    talk_with_animation("Please say 'I'm done' when you've finished the form.", screen, talk_frames, neutral_face)
                    audio = recognizer.listen(source, timeout=10)  # Wait for a response
                    response = recognizer.recognize_google(audio).lower().strip()

                    if response == "i'm done":
                        talk_with_animation("Thank you! Someone will attend to you shortly. you can wait in the lobby behind you", screen, talk_frames, neutral_face)
                        break

            # Check if the user is asking for directions
            elif directions(user_response):
                print("Direction intent detected.")

                # Ask the user for the specific location
                talk_with_animation("Where would you like to go?", screen, talk_frames, neutral_face)

                print("Listening for location...")
                location_audio = recognizer.listen(source, timeout=5)
                location_response = recognizer.recognize_google(location_audio).lower().strip()
                print(f"User specified location: {location_response}")

                # Match the location
                matched_location = False
                new_location = ""
                for loc in locations_kw:
                    print(loc)
                    if loc in location_response:
                        matched_location = True
                        new_location = loc
                        break

                if matched_location:
                    # Provide location-specific response
                    response_text = location(new_location)
                    print(f"Matched location: {new_location}")
                else:
                    # Inform the user the specific location is not found
                    response_text = f"I'm sorry, but '{new_location}' is not available in this building."
                    print(response_text)

            # Default fallback if no intent is detected
            else:
                response_text = "I'm here to help if you need anything else."
            
            # Speak and animate response
            talk_with_animation(response_text, screen, talk_frames, neutral_face)
        except sr.UnknownValueError:
            print("Could not understand the audio input. Please try again.")
            talk_with_animation("Sorry, I didn't catch that. Could you repeat?", screen, talk_frames, neutral_face)
        except sr.WaitTimeoutError:
            print("No input detected.")
            talk_with_animation("I didn't hear you. Could you please repeat that?", screen, talk_frames, neutral_face)
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            talk_with_animation("There seems to be an issue with the speech service. Please try again later.", screen, talk_frames, neutral_face)
        except Exception as e:
            print(f"Unexpected error: {e}")
            talk_with_animation("An unexpected error occurred. Please try again later.", screen, talk_frames, neutral_face)


# Main Function
def main():

    pygame.init()
    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    # Load assets
    neutral_face = pygame.image.load("Gif/neutral.png")
    blink_frames = load_gif_frames("Gif/Blinking.gif")
    talk_frames = load_gif_frames("Gif/Talking.gif")

    screen.blit(neutral_face, (0, 0))
    pygame.display.flip()

    print("Press SPACEBAR to simulate user entering the greeting zone.")

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Trigger greeting on spacebar press
                    greeting_zone(screen, talk_frames, neutral_face)

        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
