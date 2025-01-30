import os
from collections import defaultdict
from utils import (
    get_current_date,
    load_json,
    save_json,
    split_artists,
    file_path,
)
from fetcher import albums_dict, album_id, artist_id, songs_dict

dates = load_json("./data/dates.json")
oldest_date = min(dates["data"])
old_json_directory = f"./data/{oldest_date}"

CURRENT_DATE = get_current_date()
CURRENT_FOLDER = "./data/current"
output_folder = f"./data/{CURRENT_DATE}"
os.makedirs(output_folder, exist_ok=True)


def process_tracks(tracks):
    formatted_tracks = {"data": []}
    for track_id, track in tracks.items():
        formatted_tracks["data"].append(
            {
                "id": track["Track ID"],
                "name": track["Name"],
                "duration": track["Total Time"],
                "trackNumber": track["Track Number"],
                "artist": track["Artist"],
                "album": track["Album"],
                "albumArtist": track.get("Album Artist", track["Artist"]),
                "year": track["Year"],
                "genre": track["Genre"],
                "playCount": track.get("Play Count", 0),
                "timePlayed": track.get("Play Count", 0) * track["Total Time"],
                "positionsGained": 0,
            }
        )

    formatted_tracks["data"] = sorted(
        formatted_tracks["data"], key=lambda x: (-x["timePlayed"], x["name"])
    )

    old_formatted_tracks = load_json(
        file_path(
            f"Formatted_Biblioteca_{
        oldest_date}.json",
            old_json_directory,
        )
    )

    old_track_index_map = {
        track["id"]: idx for idx, track in enumerate(old_formatted_tracks["data"])
    }

    for idx, track in enumerate(formatted_tracks["data"]):
        old_index = old_track_index_map.get(track["id"], len(old_track_index_map) - 1)
        positions_gained = old_index - idx
        track["positionsGained"] = positions_gained

    return formatted_tracks


def process_albums(data):
    albums = defaultdict(
        lambda: {
            "id": 0,
            "name": "",
            "artist": "",
            "year": 0,
            "genre": "",
            "playCount": float("inf"),
            "timePlayed": 0,
            "tracks": [],
            "positionsGained": 0,
        }
    )

    for track in data:
        album_name = track["album"]
        album_artist = track["albumArtist"]
        album_year = track["year"]
        album_genre = track["genre"]
        play_count = track["playCount"]
        time_played = track["timePlayed"]
        album = albums[album_name]

        if album["name"] == "":
            album["name"] = album_name
            album["artist"] = album_artist
            album["year"] = album_year
            album["genre"] = album_genre

        album["playCount"] = min(album["playCount"], play_count)
        album["timePlayed"] += time_played
        album["tracks"].append(
            {
                "id": track["id"],
                "name": track["name"],
                "duration": track["duration"],
                "trackNumber": track["trackNumber"],
                "artist": track["artist"],
                "album": album_name,
                "albumArtist": track.get("albumArtist", track["artist"]),
                "year": album_year,
                "genre": album_genre,
                "playCount": play_count,
                "timePlayed": time_played,
                "positionsGained": 0,
            }
        )

    for album in albums.values():
        album["id"] = album_id(album["name"])
        album["tracks"] = sorted(album["tracks"], key=lambda x: x["trackNumber"])

    formatted_albums = {"data": list(albums.values())}

    formatted_albums["data"] = sorted(
        formatted_albums["data"], key=lambda x: x["timePlayed"], reverse=True
    )

    old_formatted_albums = load_json(
        file_path(
            f"Formatted_Biblioteca_byAlbum_{
        oldest_date}.json",
            old_json_directory,
        )
    )

    old_album_index_map = {
        album["id"]: idx for idx, album in enumerate(old_formatted_albums["data"])
    }

    for idx, album in enumerate(formatted_albums["data"]):
        old_index = old_album_index_map.get(album["id"], len(old_album_index_map) - 1)
        positions_gained = old_index - idx
        album["positionsGained"] = positions_gained

    save_json(
        formatted_albums,
        [
            file_path(
                f"Formatted_Biblioteca_byAlbum_{
              CURRENT_DATE}.json",
                output_folder,
            ),
            file_path("Formatted_Biblioteca_byAlbum.json", CURRENT_FOLDER),
        ],
    )


def process_artists(data):
    artists = defaultdict(
        lambda: {
            "id": 0,
            "name": "",
            "songs": [],
            "songsCount": 0,
            "timePlayed": 0,
            "positionsGained": 0,
        }
    )

    for track in data:
        artists_names = split_artists(track["artist"])
        for artist_name in artists_names:
            artist = artists[artist_name]

            if artist["name"] == "":
                artist["name"] = artist_name

            if track not in artist["songs"]:
                artist["songs"].append(track)

            artist["songsCount"] += 1
            artist["timePlayed"] += track["timePlayed"]

    for artist in artists.values():
        artist["id"] = artist_id(artist["name"])

    formatted_artists = {"data": list(artists.values())}

    formatted_artists["data"] = sorted(
        formatted_artists["data"], key=lambda x: x["timePlayed"], reverse=True
    )

    old_formatted_artists = load_json(
        file_path(
            f"Formatted_Biblioteca_byArtist_{
        oldest_date}.json",
            old_json_directory,
        )
    )

    old_artist_index_map = {
        artist["name"]: idx for idx, artist in enumerate(old_formatted_artists["data"])
    }

    for idx, artist in enumerate(formatted_artists["data"]):
        old_index = old_artist_index_map.get(
            artist["name"], len(old_artist_index_map) - 1
        )
        positions_gained = old_index - idx
        artist["positionsGained"] = positions_gained

    save_json(
        formatted_artists,
        [
            file_path(
                f"Formatted_Biblioteca_byArtist_{
              CURRENT_DATE}.json",
                output_folder,
            ),
            file_path("Formatted_Biblioteca_byArtist.json", CURRENT_FOLDER),
        ],
    )


def process_genres(data):
    genres = defaultdict(
        lambda: {
            "id": 0,
            "name": "",
            "albums": [],
            "artists": set(),
            "timePlayed": 0,
            "positionsGained": 0,
        }
    )

    album_dict = albums_dict()

    for index, track in enumerate(data):
        genre_name = track["genre"]
        genre = genres[genre_name]

        if genre["name"] == "":
            genre["name"] = genre_name

        album = album_dict.get(track["album"])
        if album and album not in genre["albums"]:
            genre["albums"].append(album)

        genre["id"] = index
        genre["artists"].add(track["artist"])
        genre["timePlayed"] += track["timePlayed"]

    for genre in genres.values():
        genre["artists"] = sorted(list(genre["artists"]))

    formatted_genres = {"data": list(genres.values())}

    formatted_genres["data"] = sorted(
        formatted_genres["data"], key=lambda x: x["timePlayed"], reverse=True
    )

    old_formatted_genres = load_json(
        file_path(
            f"Formatted_Biblioteca_byGenre_{
        oldest_date}.json",
            old_json_directory,
        )
    )

    old_genre_index_map = {
        genre["name"]: idx for idx, genre in enumerate(old_formatted_genres["data"])
    }

    for idx, genre in enumerate(formatted_genres["data"]):
        old_index = old_genre_index_map.get(genre["name"], len(old_genre_index_map) - 1)
        positions_gained = old_index - idx
        genre["positionsGained"] = positions_gained

    save_json(
        formatted_genres,
        [
            file_path(
                f"Formatted_Biblioteca_byGenre_{
              CURRENT_DATE}.json",
                output_folder,
            ),
            file_path("Formatted_Biblioteca_byGenre.json", CURRENT_FOLDER),
        ],
    )
