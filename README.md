# iTunes Wrapped

This repository provides a Python-based tool for organizing and processing a personal music library exported from iTunes. It takes the raw JSON data from iTunes, formats it, and generates structured JSON outputs for easier access and integration with front-end applications.

## Features

- **Parsing and Formatting**: Converts the original iTunes library JSON into a more manageable and structured format.
- **Data Grouping and Sorting**: Organizes data based on various attributes such as play count, time played, album, artist, genre, and more.
- **Unique Identifiers**: Generates unique UUIDs for albums and genres to ensure consistency and reliability in data handling.
- **Custom Outputs**: Generates output files sorted by time played, play count, album, genre, and artist.
- **Flexible Integration**: Outputs are designed for easy integration with front-end applications, making it ideal for data visualization or music recommendation systems.

## Supported Data

The tool works with the following key attributes extracted from your iTunes library:

- **Track ID**
- **Name**
- **Artist**
- **Album Artist**
- **Album**
- **Genre**
- **Year**
- **Duration**
- **Play Count**
- **Time Played**

The data can be grouped by various attributes, including album, genre, and artist, to provide deeper insights into your music library.
