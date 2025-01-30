import random
import time
import requests
from utils import load_json, save_json


def fetch_album_data(album_name, album_artist):
    url = "https://itunes.apple.com/search"
    params = {
        "term": album_name,
        "limit": 1,
        "entity": "album",
        "attributes": album_artist,
    }
    response = requests.get(url, params=params)
    return response.json()


def fetch_new_covers():
    cover_input_file = "./data/current/Formatted_Biblioteca_byAlbum.json"
    cover_output_file = "./data/covers.json"

    data = load_json(cover_input_file)

    existing_data = {}
    existing_data = load_json(cover_output_file)
    if not existing_data:
        existing_data = {"data": []}

    existing_album_names = {album["name"] for album in existing_data["data"]}

    new_albums = []

    for album in data["data"]:
        album_name = album["name"]
        album_artist = album["artist"]

        if not album_name or album_name in existing_album_names:
            continue

        result = fetch_album_data(album_name, album_artist)

        if result.get("resultCount", 0) > 0:
            artwork_url = result["results"][0].get("artworkUrl100", "Not found")
            new_albums.append({"name": album_name, "image": artwork_url})
        else:
            print(f"No results found for {album_name}.")

        time.sleep(random.uniform(2, 5))

    existing_data["data"].extend(new_albums)
    save_json(existing_data, [cover_output_file])

    return existing_data
