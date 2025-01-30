import os
import xml.etree.ElementTree as ET
from utils import get_current_date, load_json, save_json, add_date, file_path
from processor import process_albums, process_artists, process_genres, process_tracks
from fetcher import fetch_new_covers

CURRENT_DATE = get_current_date()
CURRENT_FOLDER = "./data/current"
output_folder = f"./data/{CURRENT_DATE}"
os.makedirs(output_folder, exist_ok=True)


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
            elif value_elem.tag == "false":
                value = False
            else:
                value = value_elem.text

            track[key] = value

        tracks[track_id] = track

    return tracks


def update_covers():
    covers = fetch_new_covers()
    cover_dict = {cover["name"]: cover["image"] for cover in covers.get("data", [])}

    album_file = "./data/current/Formatted_Biblioteca_byAlbum.json"
    albums = load_json(album_file)

    for album in albums.get("data", []):
        album_name = album.get("name")
        if album_name in cover_dict:
            album["image"] = cover_dict[album_name]

    save_json(
        albums,
        [
            file_path(
                f"Formatted_Biblioteca_byAlbum_{
              CURRENT_DATE}.json",
                output_folder,
            ),
            file_path("Formatted_Biblioteca_byAlbum.json", CURRENT_FOLDER),
        ],
    )

    tracks_file = "./data/current/Formatted_Biblioteca.json"
    tracks = load_json(tracks_file)

    for track in tracks.get("data", []):
        album_name = track.get("album")
        if album_name in cover_dict:
            track["image"] = cover_dict[album_name]

    save_json(
        tracks,
        [
            file_path(
                f"Formatted_Biblioteca_{
              CURRENT_DATE}.json",
                output_folder,
            ),
            file_path("Formatted_Biblioteca.json", CURRENT_FOLDER),
        ],
    )


def main():
    xml_file = "./libraries/Biblioteca.xml"
    new_xml_file = f"./libraries/Biblioteca_{CURRENT_DATE}.xml"
    add_date(CURRENT_DATE)

    tracks = parse_xml(xml_file, new_xml_file)
    save_json(
        tracks,
        [
            file_path("Biblioteca.json", CURRENT_FOLDER),
            file_path(f"Biblioteca_{CURRENT_DATE}.json", output_folder),
        ],
    )

    formatted_tracks = process_tracks(tracks)
    save_json(
        formatted_tracks,
        [
            file_path("Formatted_Biblioteca.json", CURRENT_FOLDER),
            file_path(f"Formatted_Biblioteca_{CURRENT_DATE}.json", output_folder),
        ],
    )

    process_albums(formatted_tracks["data"])
    process_artists(formatted_tracks["data"])
    process_genres(formatted_tracks["data"])

    update_covers()


if __name__ == "__main__":
    main()
