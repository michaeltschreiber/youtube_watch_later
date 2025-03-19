# YouTube Watch Later to Excel (Device Authentication Version)

This Python script extracts videos from your YouTube Watch Later playlist and creates an Excel file with the following columns:
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

```bash
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2 pandas openpyxl
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
4. Enter a name for your OAuth client (e.g., "YouTube Watch Later Extractor")
5. Click "Create"
6. Download the JSON file by clicking the download button
7. Rename the downloaded file to `client_secret.json` and place it in the same directory as the script

## Usage

1. Place the `youtube_watch_later.py` script and your `client_secret.json` file in the same directory
2. Run the script:
   ```bash
   python youtube_watch_later.py
   ```
3. The script will display an authorization URL
4. Open the URL in your browser, log in to your Google account, and grant permission to access your YouTube data
5. You will receive an authorization code - copy this code
6. Paste the authorization code into the script prompt
7. The script will extract your Watch Later playlist and create an Excel file named `youtube_watch_later.xlsx` in the same directory

## Notes

- This version uses device authentication flow, which allows you to authenticate on a different device than the one running the script
- The authentication token is stored in a file named `token.pickle` for future use
- If you want to use a different Google account, delete the `token.pickle` file and run the script again
- The Watch Later playlist is a special playlist in YouTube that requires specific handling

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
