from turtle import Screen
import requests
import bs4
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# _______________ POP UP WITH QUESTION _______________ #
screen = Screen()
screen.setup(width=600, height=250)
screen.bgcolor("navajo white")
chosen_date = screen.textinput(title="Let's travel!",
                            prompt=f"Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

# _______________ MAKING REQUESTS TO BILLBOARD _______________ #
top_songs_endpoint = f"https://www.billboard.com/charts/hot-100/{chosen_date}"
response = requests.get(url=top_songs_endpoint)


# _______________ MAKING A LIST WITH 100 SONG NAMES _______________ #
soup = bs4.BeautifulSoup(response.text, "html.parser")
songs_list = [song.text.replace("\t", "") for song in soup.select("div.o-chart-results-list-row-container li h3")]
song_names_list = [song.replace("\n", "") for song in songs_list]


# _______________ AUTHENTICATION TO SPOTIFY _______________ #
spotify_client_id = "xxx"
spotify_client_secret = "xxx"
redirect_URI = "http://example.com/"
SCOPE = "xxx"

auth = SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret,
                    redirect_uri=redirect_URI, scope=SCOPE)
token = auth.get_access_token()["access_token"]
client = spotipy.Spotify(auth=token)


# _______________ SEARCHING TRACKS URI ON SPOTIFY _______________ #
tracks_uri_list = []
year = chosen_date.split("-")[0]
for song in song_names_list:
    try:
        tracks_uri_list.append(client.search(q=f"track:{song} year:{year}", limit=1, type="track")
                               ["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"Song {song} doesn't exist in Spotify")


# _______________ CREATING A NEW PLAYLIST _______________ #
user_id = client.current_user()["id"]
playlist = client.user_playlist_create(user=user_id, name=f"The hot 100 songs in {chosen_date}", public=False)

playlist_id = playlist["id"]
add_tracks = client.playlist_add_items(playlist_id=playlist_id, items=tracks_uri_list)
