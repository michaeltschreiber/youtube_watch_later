# YouTube Playlist to Excel

This Python script extracts videos from any YouTube playlist by ID and creates an Excel file with the following columns:

- Channel
- Video Title
- Video Description
- Link to Video
- Watched Status (checkbox)

## Prerequisites

- Python 3.6 or higher
- Google account with access to YouTube
- Google Cloud Platform project with YouTube Data API v3 enabled

## Setup Instructions

### 1. Install Required Python Packages

You can install all required packages using the included requirements.txt file:

```bash
pip install -r requirements.txt
```

### 2. Set Up Google Cloud Project and Enable YouTube Data API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. In the sidebar, navigate to "APIs & Services" > "Library"
4. Search for "YouTube Data API v3" and enable it

### 3. Create OAuth 2.0 Credentials

1. In the Google Cloud Console, navigate to "APIs & Services" > "Credentials"
2. Click "Create Credentials" and select "OAuth client ID"
3. Select "Desktop app" as the application type
4. Enter a name for your OAuth client (e.g., "YouTube Playlist Extractor")
5. Click "Create"
6. Download the JSON file by clicking the download button
7. Rename the downloaded file to `client_secret.json` and place it in the same directory as the script

## Usage

The script supports the following command-line options:

```bash
python youtube_watch_later.py [playlist_id] [-o OUTPUT_FILE]
```

Where:
- `playlist_id`: Optional YouTube playlist ID (if not provided, you will be prompted)
- `-o OUTPUT_FILE` or `--output OUTPUT_FILE`: Optional custom output filename

### Examples

#### Basic Usage (Will Prompt for Playlist ID)
```bash
python youtube_watch_later.py
```

#### Provide Playlist ID Directly
```bash
python youtube_watch_later.py PLv5D27PeF1QwexfA46_kHG385hHdtjLyM
```

#### Specify Custom Output Filename
```bash
python youtube_watch_later.py PLv5D27PeF1QwexfA46_kHG385hHdtjLyM -o my_videos.xlsx
```

### Authentication Process

1. Place the `youtube_watch_later.py` script and your `client_secret.json` file in the same directory
2. Run the script with your desired options
3. The script will display an authorization URL
4. Open the URL in your browser, log in to your Google account, and grant permission to access your YouTube data
5. You will receive an authorization code - copy this code
6. Paste the authorization code into the script prompt
7. The script will extract the playlist videos and create an Excel file (named based on the playlist name or using your custom filename)

## Notes

- This script uses device authentication flow, which allows you to authenticate on a different device than the one running the script
- The authentication token is stored in a file named `token.pickle` for future use
- If you want to use a different Google account, delete the `token.pickle` file and run the script again
- To get a playlist ID, open the playlist in YouTube and look at the URL. The ID is the value after `list=` (e.g., `PLv5D27PeF1QwexfA46_kHG385hHdtjLyM`)

## Troubleshooting

### "Error: client_secret.json not found"
- Make sure you've downloaded the OAuth credentials JSON file from Google Cloud Console
- Rename it to `client_secret.json` and place it in the same directory as the script

### "Invalid client secret file"
- Make sure you've downloaded the correct type of credentials (OAuth client ID for Desktop app)

### "Access Not Configured"
- Make sure you've enabled the YouTube Data API v3 in your Google Cloud project

### "Quota Exceeded"
- The YouTube Data API has usage quotas. If you exceed them, you'll need to wait until they reset or request a quota increase