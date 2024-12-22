from dotenv import load_dotenv

load_dotenv()

import mediapipe as mp
import cv2
from hattify import hattify
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import discord


IMAGE_FILE = "assets/cat in currents.png"
# IMAGE_FILE = "assets/penguin.png"
# IMAGE_FILE = "assets/man.png"
# IMAGE_FILE = "assets/cat.jpg"
# IMAGE_FILE = "assets/lena30.jpg"


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/login")
def login():
    return RedirectResponse(discord.login())


@app.get("/test")
def read_item():
    image = mp.Image.create_from_file(IMAGE_FILE)

    rgb_annotated_image = hattify(image)

    # Write to file
    cv2.imwrite("output.jpg", rgb_annotated_image)


@app.get("/callback")
def callback(code: str):
    token = discord.callback(code)
    user_data = discord.get_user_info(token)
    discord.set_user_avatar(token, "assets/christmas-hat.png")
    return user_data
