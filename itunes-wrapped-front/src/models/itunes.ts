interface BaseEntity {
  id: string
  name: string
  timePlayed: number
  positionsGained: number
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
  albums: string[]
  songsCount: number
}

export interface Genre extends BaseEntity {
  albums: string[]
  artists: string[]
}
