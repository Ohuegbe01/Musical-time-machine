import requests
import spotipy
import pprint
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth


load_dotenv()
# Access environment variables
spoify_app_client_id = os.getenv("SPOIFY_APP_CLIENT_ID")
spotify_client_secret = os.getenv("SPOIFY_CLIENT_SECRET")



date = input("what year would you like to travel to? Type the date in this format YYYY-MM-DD:\n")
response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
y = response.text
soup = BeautifulSoup(y, "html.parser")
songs = soup.select("li ul li h3")
song_list = [_.getText().strip() for _ in songs]
print(song_list)

scope = "playlist-modify-private"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=spoify_app_client_id, client_secret=spotify_client_secret, redirect_uri='http://example.com', cache_path='../.cache'))

results = sp.current_user()['id']
# print(results)

# OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
# OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'
id = "68f132e16f3i8nb3uu2c8fv60"

# pl_id = f"spotify:track:'Touch My Body':{id}:year:2008"
# print(pl_id)
year = date.split("-")[0]
print(year)
song_uris = []
for _ in song_list:
    result = sp.search(q=f"track:{_} year:{year}", type="track")
    # pprint.pp(result)
    print(result)
    # pp = pprint.PrettyPrinter(width=41, compact=True)
    # pp.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{_} doesn't exist in Spotify. Skipped.")

json = {
    "name": f"{date} Billboard 100 Playlist",
    "description": "A taste of the BillBoard Top 100 Songs",
    "public": False
}

#
playlist = sp.user_playlist_create(user=id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)