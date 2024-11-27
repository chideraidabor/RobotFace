import pygame
from PIL import Image
import speech_recognition as sr
import pyttsx3
import time
import google.generativeai as genai
import os
import PIL.Image
import json
genai.configure(api_key = "AIzaSyB8l5GIUfbI2IWdUvgwI1FGHPAxGifLYz8")
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

### Function Calling
############# LLM Function Defination #############
def power_disco_ball(power: bool) -> bool:
    """Powers the spinning disco ball."""
    print(f"Disco ball is {'spinning!' if power else 'stopped.'}")
    return True


def start_music(energetic: bool, loud: bool, bpm: int) -> str:
    """Play some music matching the specified parameters.

    Args:
      energetic: Whether the music is energetic or not.
      loud: Whether the music is loud or not.
      bpm: The beats per minute of the music.

    Returns: The name of the song being played.
    """
    print(f"Starting music! {energetic=} {loud=}, {bpm=}")
    return "Never gonna give you up."


def dim_lights(brightness: float) -> bool:
    """Dim the lights.

    Args:
      brightness: The brightness of the lights, 0.0 is off, 1.0 is full.
    """
    print(f"Lights are now set to {brightness:.0%}")
    return True
############# LLM Function Defination #############

############# Python Function Call #############
def python_power_disco_ball(power):
    print("power_disco_ball: This is a function from actual python function call")
    print(power)
    print("----------------")

def python_start_music(energetic, loud, bpm):
    print("start_music: This is a function from actual python function call")
    print(energetic, loud, bpm)
    print("----------------")

def python_dim_lights(brightness):
    print("dim_lights: This is a function from actual python function call")
    print(brightness)
    print("----------------")
############# Python Function Call #############

house_fns = [power_disco_ball, start_music, dim_lights]

function_handler_dict = {
    "power_disco_ball": python_power_disco_ball,
    "start_music": python_start_music,
    "dim_lights": python_dim_lights
}



model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=house_fns)

chat = model.start_chat()
response = chat.send_message("Turn this place into a party!")

function_responses = {}
for part in response.parts:
    if fn := part.function_call:
        args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
        function_responses[fn.name] = function_handler_dict[fn.name](**fn.args)
        print(f"{fn.name}({args}) ==> {function_responses[fn.name]}")
### Function Calling




# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content("Write a story about a magic backpack.")
# print(response.text)



# sample_file = PIL.Image.open('panda.jpeg')
# sample_file_1 = PIL.Image.open('firefighter.jpeg')

# Choose a Gemini model.
# model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# prompt = "Write an advertising jingle showing how the product in the first image could solve the problems shown in the second two images."

# response = model.generate_content([prompt, sample_file, sample_file_1])

# print(response.text)

# model = genai.GenerativeModel("gemini-1.5-pro-latest")
# prompt = """List a few popular cookie recipes in JSON format.

# Use this JSON schema:

# Recipe = {'recipe_name': str, 'ingredients': list[str]}
# Return: list[Recipe]"""
# result = model.generate_content(prompt)
# print(result.text.json)
# json_data = json.loads()

# import typing_extensions as typing

# class Recipe(typing.TypedDict):
#     recipe_name: str
#     ingredients: list[str]

# model = genai.GenerativeModel("gemini-1.5-pro-latest")
# result = model.generate_content(
#     "List a few popular cookie recipes.",
#     generation_config=genai.GenerationConfig(
#         response_mime_type="application/json", response_schema=list[Recipe]
#     ),
# )
# output = result.text
# print(output)
# print("---------------------------------------------")

# print(output[0])


# def set_light_values(brightness, color_temp):
#     """Set the brightness and color temperature of a room light. (mock API).

#     Args:
#         brightness: Light level from 0 to 100. Zero is off and 100 is full brightness
#         color_temp: Color temperature of the light fixture, which can be `daylight`, `cool` or `warm`.

#     Returns:
#         A dictionary containing the set brightness and color temperature.
#     """
#     return {
#         "brightness": brightness,
#         "colorTemperature": color_temp
#     }

# model = genai.GenerativeModel(model_name='gemini-1.5-flash',
#                               tools=[set_light_values])
# chat = model.start_chat()
# response = chat.send_message('Dim the lights so the room feels cozy and warm.')
# print(response.text)

# def power_disco_ball(power: bool) -> bool:
#     """Powers the spinning disco ball."""
#     print(f"Disco ball is {'spinning!' if power else 'stopped.'}")
#     return True


# def start_music(energetic: bool, loud: bool, bpm: int) -> str:
#     """Play some music matching the specified parameters.

#     Args:
#       energetic: Whether the music is energetic or not.
#       loud: Whether the music is loud or not.
#       bpm: The beats per minute of the music.

#     Returns: The name of the song being played.
#     """
#     print(f"Starting music! {energetic=} {loud=}, {bpm=}")
#     return "Never gonna give you up."


# def dim_lights(brightness: float) -> bool:
#     """Dim the lights.

#     Args:
#       brightness: The brightness of the lights, 0.0 is off, 1.0 is full.
#     """
#     print(f"Lights are now set to {brightness:.0%}")
#     return True

# # Set the model up with tools.
# house_fns = [power_disco_ball, start_music, dim_lights]

# model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=house_fns)

# # Call the API.
# chat = model.start_chat()
# response = chat.send_message("Turn this place into a party!")

# # Print out each of the function calls requested from this single call.
# for part in response.parts:
#     if fn := part.function_call:
#         args = ", ".join(f"{key}={val}" for key, val in fn.args.items())
#         print(f"{fn.name}({args})")