import requests
import spotipy
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
import time

client_id = "your_spotify_client_id"
client_secret = "your_spotify_client_secret_key"

def index(request):
  return render(request, 'frontend/index.html')

@api_view(['GET','POST'])
def link(req):
  if req.method == "POST":
    try:
      data = req.body.decode('utf-8')
      response = requests.get(str(data))
      soup = BeautifulSoup(response.content, "html.parser")
      song_titles = soup.find_all("div", class_="songs-list-row__song-name")
      rows = soup.find_all("div", class_="songs-list-row")
      playlist_title = soup.find("h1", id="page-container__first-linked-element").text.split("\n")[1:-1][0][1:]
    except:
      return render(req, "frontend/index.html", status=400)
      
    songs = []
    for i, song in enumerate(rows):
      title = song_titles[i].text
      if "(" in title:
        title = title[:title.index("(")]
      elif "[" in title:
        title = title[:title.index("[")]
      artist = song.find("div", "songs-list__col songs-list__col--artist typography-body").find("div").find("a").text
      album = song.find("div", "songs-list__col songs-list__col--album typography-body").find("div").find("span").find("a").text
      if "(" in album:
        album = album[:album.index("(")]
      songs.append({"title": title, "artist":artist, "album":album})
    
    sp = spotipy.Spotify(
      auth_manager=spotipy.SpotifyOAuth(
          scope="playlist-modify-private",
          redirect_uri="http://example.com",
          client_id=client_id,
          client_secret=client_secret,
          show_dialog=True,
          cache_path="token.txt"
      ))
    user_id = sp.current_user()["id"]
    
    uris = []
    for song in songs:
      if "Single" in song["album"]:
        result = sp.search(q=f"track:{song['title']} artist:{song['artist']}", type="track")
      else:
        result = sp.search(q=f"track:{song['title']} artist:{song['artist']} album:{song['album']}", type="track")
      try:
        uri = result["tracks"]["items"][0]["uri"]
        uris.append(uri)
        print("Song added:", song["title"])
      except IndexError:
        print(song["title"], "not on spotify")
        
    playlist = sp.user_playlist_create(user=user_id, name=playlist_title, public=False)
    sp.playlist_add_items(playlist_id=playlist["id"], items=uris)
  return render(req, "frontend/index.html")