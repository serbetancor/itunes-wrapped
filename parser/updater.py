import os
from utils import load_json, save_json, file_path, get_current_date
from fetcher import album_metadata, artist_metadata
from scraper import artists_scraper

CURRENT_DATE = get_current_date()
CURRENT_FOLDER = "./data/current"
output_folder = f"./data/{CURRENT_DATE}"
os.makedirs(output_folder, exist_ok=True)


def update_album_covers():
    albumsMetadata = album_metadata()
    cover_dict = {
        cover["name"]: cover["image"] for cover in albumsMetadata.get("data", [])
    }

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


def update_artists_images():
    artists_metadata = artist_metadata()

    artists_no_name = []

    for artist in artists_metadata["data"][:]:
        if "image" not in artist:
            artists_no_name.append(artist)
            artists_metadata["data"].remove(artist)

    if len(artists_no_name):
        updated_images = artists_scraper(artists_no_name)
        artists_metadata["data"].extend(updated_images)

        save_json(artists_metadata, ["./data/artistsMetadata.json"])

    artist_file = "./data/current/Formatted_Biblioteca_byArtist.json"
    artists = load_json(artist_file)

    artists_metadata_dict = {
        cover["id"]: cover["image"] for cover in artists_metadata["data"]
    }

    for artist in artists.get("data", []):
        artist_id = artist["id"]
        if artist_id in artists_metadata_dict:
            artist["image"] = artists_metadata_dict[artist_id]

    save_json(
        artists,
        [
            file_path(
                f"Formatted_Biblioteca_byArtist_{
              CURRENT_DATE}.json",
                output_folder,
            ),
            file_path("Formatted_Biblioteca_byArtist.json", CURRENT_FOLDER),
        ],
    )
