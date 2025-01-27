import os
import json
import uuid
from collections import defaultdict
from datetime import datetime
import xml.etree.ElementTree as ET


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def file_path(filename, output_folder):
    return os.path.join(output_folder, filename)


def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_json(data, file_paths):
    for path in file_paths:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


def generate_uuid():
    return str(uuid.uuid4())


def add_date(date):
    json_file = "dates.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            data = json.load(f)
    else:
        data = {"data": []}

    if date not in data["data"]:
        data["data"].append(date)

        with open(json_file, "w") as f:
            json.dump(data, f, indent=2)


def parse_xml(xml_file, new_xml_file):
    if os.path.exists(xml_file):
        os.rename(xml_file, new_xml_file)
    else:
        raise FileNotFoundError(f"File not found: {xml_file}")

    tree = ET.parse(new_xml_file)
    root = tree.getroot()
    library_dict = root.find("dict")

    tracks_dict = None
    keys = list(library_dict)

    for i in range(len(keys)):
        if keys[i].tag == "key" and keys[i].text == "Tracks":
            tracks_dict = keys[i + 1]
            break

    if tracks_dict is None or tracks_dict.tag != "dict":
        raise ValueError("Tracks dictionary not found in XML")

    tracks = {}
    track_elements = list(tracks_dict)
    for i in range(0, len(track_elements), 2):
        track_id = track_elements[i].text
        track_data = track_elements[i + 1]

        track = {}
        keys = list(track_data)

        for j in range(0, len(keys), 2):
            key = keys[j].text
            value_elem = keys[j + 1]

            # Convert values based on type
            if value_elem.tag == "integer":
                value = int(value_elem.text)
            elif value_elem.tag == "true":
                value = True
            elif value_elem.tag == 'false':
                value = False
            else:
                value = value_elem.text

            track[key] = value

        tracks[track_id] = track

    return tracks


def process_tracks(tracks,  oldest_date, old_json_directory, current_date, output_folder, current_folder):
    formatted_tracks = {"data": []}
    for track_id, track in tracks.items():
        formatted_tracks["data"].append({
            "id": str(track["Track ID"]),
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
            "positionsGained": 0
        })

    formatted_tracks["data"] = sorted(
        formatted_tracks["data"], key=lambda x: (-x["timePlayed"], x["name"]))

    old_formatted_tracks = load_json(file_path(f'Formatted_Biblioteca_{
        oldest_date}.json', old_json_directory))

    old_track_index_map = {track['id']: idx for idx,
                           track in enumerate(old_formatted_tracks["data"])}

    for idx, track in enumerate(formatted_tracks["data"]):
        old_index = old_track_index_map.get(
            track['id'],  len(old_track_index_map) - 1)
        positions_gained = old_index - idx
        track['positionsGained'] = positions_gained

    return formatted_tracks


def process_albums(data, oldest_date, old_json_directory, current_date, output_folder, current_folder):
    albums = defaultdict(lambda: {
        "id": generate_uuid(),
        "name": "",
        "artist": "",
        "year": 0,
        "genre": "",
        "playCount": float('inf'),
        "timePlayed": 0,
        "tracks": [],
        "positionsGained": 0
    })

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
        album["tracks"].append({
            "id": str(track["id"]),
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
            "positionsGained": 0
        })

    for album in albums.values():
        album["tracks"] = sorted(
            album["tracks"], key=lambda x: x["trackNumber"])

    formatted_albums = {
        "data": list(albums.values())
    }

    formatted_albums["data"] = sorted(
        formatted_albums["data"], key=lambda x: x["timePlayed"], reverse=True)

    old_formatted_albums = load_json(file_path(f'Formatted_Biblioteca_byAlbum_{
        oldest_date}.json', old_json_directory))

    old_album_index_map = {album['name']: idx for idx,
                           album in enumerate(old_formatted_albums["data"])}

    for idx, album in enumerate(formatted_albums["data"]):
        old_index = old_album_index_map.get(
            album['name'], len(old_album_index_map) - 1)
        positions_gained = old_index - idx
        album['positionsGained'] = positions_gained

    save_json(formatted_albums, [file_path(
        f'Formatted_Biblioteca_byAlbum_{current_date}.json', output_folder), file_path(
        f'Formatted_Biblioteca_byAlbum.json', current_folder)])


def process_genres(data, oldest_date, old_json_directory, current_date, output_folder, current_folder):
    genres = defaultdict(lambda: {
        "id": generate_uuid(),
        "name": "",
        "albums": set(),
        "artists": set(),
        "timePlayed": 0,
        "positionsGained": 0
    })

    for track in data:
        genre_name = track["genre"]
        genre = genres[genre_name]

        if genre["name"] == "":
            genre["name"] = genre_name

        genre["albums"].add(track["album"])
        genre["artists"].add(track["artist"])
        genre["timePlayed"] += track["timePlayed"]

    for genre in genres.values():
        genre["albums"] = sorted(list(genre["albums"]))
        genre["artists"] = sorted(list(genre["artists"]))

    formatted_genres = {
        "data": list(genres.values())
    }

    formatted_genres["data"] = sorted(
        formatted_genres["data"], key=lambda x: x["timePlayed"], reverse=True)

    old_formatted_genres = load_json(file_path(f'Formatted_Biblioteca_byGenre_{
        oldest_date}.json', old_json_directory))

    old_genre_index_map = {genre['name']: idx for idx,
                           genre in enumerate(old_formatted_genres["data"])}

    for idx, genre in enumerate(formatted_genres["data"]):
        old_index = old_genre_index_map.get(
            genre['name'], len(old_genre_index_map) - 1)
        positions_gained = old_index - idx
        genre['positionsGained'] = positions_gained

    save_json(formatted_genres, [file_path(
        f'Formatted_Biblioteca_byGenre_{current_date}.json', output_folder), file_path(
        f'Formatted_Biblioteca_byGenre.json', current_folder)])


def process_artists(data, oldest_date, old_json_directory, current_date, output_folder, current_folder):
    artists = defaultdict(lambda: {
        "id": generate_uuid(),
        "name": "",
        "albums": [],
        "songsCount": 0,
        "timePlayed": 0,
        "positionsGained": 0
    })

    for track in data:
        artist_name = track["artist"]
        artist = artists[artist_name]

        if artist["name"] == "":
            artist["name"] = artist_name

        if track["album"] not in artist["albums"]:
            artist["albums"].append(track["album"])

        artist["songsCount"] += 1
        artist["timePlayed"] += track["timePlayed"]

    for artist in artists.values():
        artist["albums"] = sorted(artist["albums"])

    formatted_artists = {
        "data": list(artists.values())
    }

    formatted_artists["data"] = sorted(
        formatted_artists["data"], key=lambda x: x["timePlayed"], reverse=True)

    old_formatted_artists = load_json(file_path(f'Formatted_Biblioteca_byArtist_{
        oldest_date}.json', old_json_directory))

    old_artist_index_map = {artist['name']: idx for idx,
                            artist in enumerate(old_formatted_artists["data"])}

    for idx, artist in enumerate(formatted_artists["data"]):
        old_index = old_artist_index_map.get(
            artist['name'], len(old_artist_index_map) - 1)
        positions_gained = old_index - idx
        artist['positionsGained'] = positions_gained

    save_json(formatted_artists, [file_path(
        f'Formatted_Biblioteca_byArtist_{current_date}.json', output_folder), file_path(
        f'Formatted_Biblioteca_byArtist.json', current_folder)])


def main():
    current_date = get_current_date()
    output_folder = f"./{current_date}"
    current_folder = "./current"
    os.makedirs(output_folder, exist_ok=True)

    dates = load_json('dates.json')
    oldest_date = min(dates["data"])
    old_json_directory = f"./{oldest_date}"

    xml_file = "Biblioteca.xml"
    new_xml_file = f"Biblioteca_{current_date}.xml"
    add_date(current_date)

    tracks = parse_xml(xml_file, new_xml_file)
    save_json(tracks, [file_path(
        f'Biblioteca.json', current_folder), file_path(
        f'Biblioteca_{current_date}.json', output_folder)])

    formatted_tracks = process_tracks(
        tracks,  oldest_date, old_json_directory, current_date, output_folder, current_folder)
    save_json(formatted_tracks, [file_path(
        f'Formatted_Biblioteca.json', current_folder), file_path(
        f'Formatted_Biblioteca_{current_date}.json', output_folder)])

    group_fields = ['albums', 'genres', 'artists']

    for field in group_fields:
        globals()[f'process_{field}'](
            formatted_tracks["data"], oldest_date, old_json_directory, current_date, output_folder, current_folder)


if __name__ == "__main__":
    main()
