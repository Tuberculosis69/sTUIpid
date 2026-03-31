import requests
from config import API_KEY, STEAM_ID

BASE_URL = "http://api.steampowered.com"

# This is all vibed, screw backend
def  get_owned_games():
    """
    Fetch the full game library for the configured Steam account.
    Returns a list of game objects with appid, name, and playtime info.
    """
    url = f"{BASE_URL}/IPlayerService/GetOwnedGames/v0001/"
    params = {
        "key": API_KEY,
        "steamid": STEAM_ID,
        "include_appinfo": True,
        "include_played_free_games": True,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("response", {}).get("games", [])
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Unexpected error fetching library: {e}")

    return []


def get_recent_games():
    """
    Fetch games played in the last 2 weeks.
    Returns a list of game objects with playtime_2weeks field.
    """
    url = f"{BASE_URL}/IPlayerService/GetRecentlyPlayedGames/v0001/"
    params = {
        "key": API_KEY,
        "steamid": STEAM_ID,
        "include_played_free_games": True,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("response", {}).get("games", [])
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Unexpected error fetching recent games: {e}")

    return []


def get_player_summary():
    """
    Fetch basic profile info for the configured Steam account.
    Returns a dict with personaname, avatarurl, profileurl etc.
    """
    url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        "key": API_KEY,
        "steamids": STEAM_ID,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        players = data.get("response", {}).get("players", [])
        return players[0] if players else {}
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Unexpected error fetching player summary: {e}")

    return {}

def save_img(appid, hash):
    url = f"http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg"
    params = {}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        with open(f"images/{appid}.jpg", "wb") as f:
            f.write(response.content)
        print(f"(LOG) Saved images/{appid}.jpg")
    except requests.exceptions.ConnectionError:
        print("Error: No internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Unexpected error fetching player summary: {e}")
        