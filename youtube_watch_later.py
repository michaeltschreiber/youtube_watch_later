#!/usr/bin/env python3
"""
YouTube Playlist to Excel

This script extracts videos from a YouTube playlist by ID
and creates an Excel file with the following columns:
- Channel
- Video Title
- Video Description
- Link to Video
- Watched Status (checkbox)

This version uses device authentication flow, allowing the user to provide
a token from another device to authenticate.
"""

import os
import pickle
import pandas as pd
import argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

def get_authenticated_service():
    """
    Authenticate with YouTube API using device authentication flow
    Returns the YouTube API service
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use device auth flow instead of web server flow
            flow = Flow.from_client_secrets_file(
                'client_secret.json',
                scopes=SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            
            # Generate the authorization URL
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print(f"Please go to this URL to authorize the application:")
            print(auth_url)
            print()
            
            # Get the authorization code from the user
            code = input("Enter the authorization code: ")
            
            # Exchange the authorization code for credentials
            flow.fetch_token(code=code)
            creds = flow.credentials
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)

def get_playlist_info(youtube, playlist_id):
    """
    Get information about the playlist
    """
    try:
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        
        if not playlist_response.get('items'):
            return "Unknown playlist"
        
        return playlist_response['items'][0]['snippet']['title']
    except Exception as e:
        print(f"Error retrieving playlist info: {e}")
        return "Unknown playlist"

def get_playlist_videos(youtube, playlist_id):
    """
    Get all videos from a playlist
    Returns a list of video data
    """
    videos = []
    next_page_token = None
    
    while True:
        try:
            # Get playlist items (limited to 50 per request)
            playlist_response = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            # Process each video in the current page
            for item in playlist_response['items']:
                video_id = item['contentDetails']['videoId']
                
                try:
                    # Get additional video details
                    video_response = youtube.videos().list(
                        part='snippet',
                        id=video_id
                    ).execute()
                    
                    if not video_response['items']:
                        # Skip if video is not available (e.g., deleted or private)
                        continue
                        
                    video_data = video_response['items'][0]
                    
                    # Extract required information
                    video_info = {
                        'channel': video_data['snippet']['channelTitle'],
                        'title': video_data['snippet']['title'],
                        'description': video_data['snippet']['description'],
                        'link': f"https://www.youtube.com/watch?v={video_id}",
                        'watched': False  # Default to not watched
                    }
                    
                    videos.append(video_info)
                    
                except Exception as e:
                    print(f"Error processing video {video_id}: {e}")
                    continue
                
            # Check if there are more pages
            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break
                
        except Exception as e:
            print(f"Error fetching playlist items: {e}")
            break
    
    return videos

def create_excel_file(videos, playlist_name, output_file=None):
    """
    Create an Excel file with the video data
    """
    if not output_file:
        # Create a safe filename from the playlist name
        safe_name = ''.join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in playlist_name)
        output_file = f"{safe_name}_videos.xlsx"
    
    # Create DataFrame from video data
    df = pd.DataFrame(videos)
    
    # Create Excel writer
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    
    # Write data to Excel
    df.to_excel(writer, index=False, sheet_name='Playlist Videos')
    
    # Get the worksheet
    worksheet = writer.sheets['Playlist Videos']
    
    # Format the worksheet
    # Adjust column widths
    worksheet.column_dimensions['A'].width = 20  # Channel
    worksheet.column_dimensions['B'].width = 40  # Title
    worksheet.column_dimensions['C'].width = 50  # Description
    worksheet.column_dimensions['D'].width = 40  # Link
    worksheet.column_dimensions['E'].width = 15  # Watched
    
    # Save the Excel file
    writer.close()
    
    print(f"Excel file created: {output_file}")
    return output_file

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Extract YouTube playlist videos to Excel.')
    parser.add_argument('playlist_id', nargs='?', help='YouTube playlist ID (e.g., PLv5D27PeF1QwexfA46_kHG385hHdtjLyM)')
    parser.add_argument('-o', '--output', help='Output Excel file name')
    args = parser.parse_args()
    
    print("YouTube Playlist to Excel")
    print("---------------------------")
    
    # Check if client_secret.json exists
    if not os.path.exists('client_secret.json'):
        print("Error: client_secret.json not found.")
        print("Please download your OAuth 2.0 Client ID credentials from Google Cloud Console")
        print("and save it as 'client_secret.json' in the same directory as this script.")
        return
    
    try:
        # Authenticate and build the YouTube API service
        youtube = get_authenticated_service()
        
        # Get playlist ID from command line or prompt
        playlist_id = args.playlist_id
        if not playlist_id:
            playlist_id = input("Enter YouTube playlist ID: ")
        
        # Get playlist info
        playlist_name = get_playlist_info(youtube, playlist_id)
        print(f"Processing playlist: {playlist_name} (ID: {playlist_id})")
        
        # Get all videos from the playlist
        print("Fetching videos from playlist...")
        videos = get_playlist_videos(youtube, playlist_id)
        
        if not videos:
            print("No videos found in the playlist.")
            return
        
        print(f"Found {len(videos)} videos in the playlist.")
        
        # Create Excel file
        output_file = create_excel_file(videos, playlist_name, args.output)
        
        print()
        print(f"Successfully created Excel file: {output_file}")
        print("The Excel file contains the following columns:")
        print("- Channel")
        print("- Video Title")
        print("- Video Description")
        print("- Link to Video")
        print("- Watched Status (checkbox)")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
