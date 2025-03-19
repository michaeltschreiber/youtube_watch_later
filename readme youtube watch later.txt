Step-by-Step Instructions to Create client_secret.json
1. Create a Google Cloud Project
Go to the Google Cloud Console
Click on the project dropdown at the top of the page
Click "NEW PROJECT"
Enter a name for your project (e.g., "YouTube Watch Later Extractor")
Click "CREATE"
Wait for the project to be created, then select it from the project dropdown
2. Enable the YouTube Data API v3
In the left sidebar, navigate to "APIs & Services" > "Library"
In the search bar, type "YouTube Data API v3"
Click on "YouTube Data API v3" in the search results
Click "ENABLE"
3. Configure the OAuth Consent Screen
In the left sidebar, navigate to "APIs & Services" > "OAuth consent screen"
Select "External" as the user type (unless you have a Google Workspace account)
Click "CREATE"
Fill in the required fields:
App name: "YouTube Watch Later Extractor"
User support email: Your email address
Developer contact information: Your email address
Click "SAVE AND CONTINUE"
On the "Scopes" page, click "ADD OR REMOVE SCOPES"
Search for "youtube.readonly" and select it
Click "UPDATE"
Click "SAVE AND CONTINUE"
On the "Test users" page, click "ADD USERS"
Add your Google email address
Click "SAVE AND CONTINUE"
Review the summary and click "BACK TO DASHBOARD"
4. Create OAuth 2.0 Client ID Credentials
In the left sidebar, navigate to "APIs & Services" > "Credentials"
Click "CREATE CREDENTIALS" at the top of the page
Select "OAuth client ID" from the dropdown
For "Application type", select "Desktop app"
Enter a name for your OAuth client (e.g., "YouTube Watch Later Desktop Client")
Click "CREATE"
A popup will appear with your client ID and client secret
Click "DOWNLOAD JSON"
Rename the downloaded file to client_secret.json
Now you have your client_secret.json file! Place this file in the same directory as the Python script I provided, and you'll be ready to run the script.
When you run the script, it will display an authorization URL. Open that URL in your browser, log in with your Google account, grant the requested permissions, and you'll receive an authorization code to paste back into the script.
Would you like me to provide the script and README files as attachments for easier download?