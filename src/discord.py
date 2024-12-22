import os
import requests
import urllib

CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("API_URL") + "/callback"
DISCORD_API_BASE_URL = "https://discord.com/api"

SCOPES = ["identify", "email"]


def login():
    # Redirect user to Discord OAuth2 authorization
    # encode redirect_uri
    redirect_uri = urllib.parse.quote(REDIRECT_URI)
    auth_url = f"{DISCORD_API_BASE_URL}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope={' '.join(SCOPES)}"
    return auth_url


def callback(code: str):
    # Get authorization code from the callback
    if not code:
        return "Authorization failed", 400

    # Exchange code for access token
    token_url = f"{DISCORD_API_BASE_URL}/oauth2/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=data, headers=headers)
    response.raise_for_status()
    token_data = response.json()

    return token_data["access_token"]


def get_user_info(token: str):
    # Get user info
    user_url = f"{DISCORD_API_BASE_URL}/users/@me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(user_url, headers=headers)
    response.raise_for_status()
    user_data = response.json()

    return user_data


def set_user_avatar(token: str, avatar: str):
    # Set user avatar
    avatar_url = f"{DISCORD_API_BASE_URL}/users/@me"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {"avatar": avatar}
    response = requests.patch(avatar_url, json=data, headers=headers)
    response.raise_for_status()
