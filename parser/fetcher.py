import random
import time
import requests
from utils import load_json, save_json


def albums_dict():
    albums_input_file = "./data/current/Formatted_Biblioteca_byAlbum.json"
    album_data = load_json(albums_input_file)
    albums_dict = {album["name"]: album for album in album_data["data"]}

    return albums_dict


def album_id(album_name):
    albums_metadata_file = "./data/albumsMetadata.json"
    existing_data = load_json(albums_metadata_file)

    return next(
        (album["id"] for album in existing_data["data"] if album["name"] == album_name),
        None,
    )


def album_itunes(album_name, album_artist):
    url = "https://itunes.apple.com/search"
    params = {
        "term": album_name,
        "limit": 1,
        "entity": "album",
        "attributes": album_artist,
    }
    response = requests.get(url, params=params)
    return response.json()


def album_metadata():
    albums_input_file = "./data/current/Formatted_Biblioteca_byAlbum.json"
    albums_metadata_file = "./data/albumsMetadata.json"

    data = load_json(albums_input_file)

    existing_data = {}
    existing_data = load_json(albums_metadata_file)
    if not existing_data:
        existing_data = {"data": []}

    existing_album_names = {album["name"] for album in existing_data["data"]}

    new_albums = []

    for album in data["data"]:
        album_name = album["name"]
        album_artist = album["artist"]

        if not album_name or album_name in existing_album_names:
            continue

        result = album_itunes(album_name, album_artist)

        if result.get("resultCount", 0) > 0:
            album_id = result["results"][0].get("collectionId", "ID not found.")
            artwork_url = result["results"][0].get(
                "artworkUrl100", "Artwordk not found."
            )
            new_albums.append(
                {"name": album_name, "id": album_id, "image": artwork_url}
            )
        else:
            print(f"No results found for {album_name}.")

        time.sleep(random.uniform(2, 5))

    existing_data["data"].extend(new_albums)
    save_json(existing_data, [albums_metadata_file])

    return existing_data


def artist_id(artist_name):
    artists_metadata_file = "./data/artistsMetadata.json"
    existing_data = load_json(artists_metadata_file)

    return next(
        (
            artist["id"]
            for artist in existing_data["data"]
            if artist["name"] == artist_name
        ),
        None,
    )


def artist_itunes(artist_name):
    url = "https://itunes.apple.com/search"
    params = {
        "term": artist_name,
        "limit": 1,
        "entity": "musicArtist",
    }
    response = requests.get(url, params=params)
    return response.json()


def artist_metadata():
    artists_input_file = "./data/current/Formatted_Biblioteca_byArtist.json"
    artists_metadata_file = "./data/artistsMetadata.json"

    data = load_json(artists_input_file)

    existing_data = {}
    existing_data = load_json(artists_metadata_file)
    if not existing_data:
        existing_data = {"data": []}

    existing_artists_names = {artist["name"] for artist in existing_data["data"]}

    new_artists = []

    for artist in data["data"]:
        artist_name = artist["name"]

        if artist_name in existing_artists_names:
            continue

        result = artist_itunes(artist_name)

        if result.get("resultCount", 0) > 0:
            artist_id = result["results"][0].get("artistId", "ID not found.")
            artwork_url = result["results"][0].get(
                "artistLinkUrl", "ArtistLinkUrl not found."
            )
            new_artists.append(
                {"name": artist_name, "id": artist_id, "parse_image": artwork_url}
            )
        else:
            print(f"No results found for {artist_name}.")

        time.sleep(random.uniform(2, 5))

    existing_data["data"].extend(new_artists)
    save_json(existing_data, [artists_metadata_file])

    return existing_data


def songs_dict():
    songs_input_file = "./data/current/Formatted_Biblioteca.json"
    songs_data = load_json(songs_input_file)
    songs_dict = {album["name"]: album for album in songs_data["data"]}

    return songs_dict
