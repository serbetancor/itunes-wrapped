interface BaseEntity {
  id: number
  name: string
  timePlayed: number
  positionsGained: number
  image?: string
}

export interface Song extends BaseEntity {
  duration: number
  trackNumber: number
  artist: string
  album: string
  albumArtist: string
  year: number
  genre: string
  playCount: number
}

export interface Album extends BaseEntity {
  artist: string
  year: number
  genre: string
  playCount: number
  tracks: Song[]
}

export interface Artist extends BaseEntity {
  songs: Song[]
  songsCount: number
}

export interface Genre extends BaseEntity {
  albums: Album[]
  artists: string[]
}
