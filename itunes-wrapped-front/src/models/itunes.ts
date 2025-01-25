export interface Song {
  id: string
  name: string
  duration: number
  trackNumber: number
  artist: string
  album: string
  albumArtist: string
  year: number
  genre: string
  playCount: number
  timePlayed: number
}

export interface Album {
  id: string
  name: string
  artist: string
  year: number
  genre: string
  playCount: number
  timePlayed: number
  tracks: Song[]
}

export interface Artist {
  id: string
  name: string
  albums: string[]
  songsCount: number
  timePlayed: number
}

export interface Genre {
  id: string
  name: string
  albums: string[]
  artists: string[]
  timePlayed: number
}
