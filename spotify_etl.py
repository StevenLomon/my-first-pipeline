import os, requests, json, s3fs, re
import pandas as pd
from dotenv import load_dotenv
from rich import print, print_json

# df = pd.read_csv('spotify_songs.csv')

# # Remove duplicates

# # sort by track_popularity
# df.sort_values("track_popularity", ascending=False, inplace=True)

# # dropping rows with the same track_id
# df.drop_duplicates(subset="track_id", keep='first', inplace=True)

# df_final = df[['track_name', 'track_artist', 'track_popularity']].head(50)

# spotify_top_50 = df_final.to_csv('spotify-top-50.csv', index=False)

load_dotenv()
rapid_api_key = os.getenv("X_RAPID_API_KEY")

def get_spotify_top_playlist_result(query:str, api_key) -> str:
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q":query,"type":"playlists","offset":"0","limit":"10","numberOfTopResults":"5"}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        playlist_uri = data.get('playlists', {}).get('items', [{}])[0].get('data', {}).get('uri', None)
        playlist_id = re.search(r'playlist:(\S+)', playlist_uri).group(1)
    
    return playlist_id

spotify_global_top_50_playlist_id = get_spotify_top_playlist_result('global top 50', rapid_api_key)

def get_playlist_tracks(playlist_id:str, api_key) -> list[dict]:
    url = "https://spotify23.p.rapidapi.com/playlist_tracks/"

    querystring = {"id":playlist_id,"offset":"0","limit":"50"}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    song_list = []
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [{}])
        for item in items:
            track = item.get('track', {})
            song = {'id': track.get('id', None),
                    'title': track.get('name', None),
                    'artist': track.get('artists', [{}])[0].get('name', None),
                    'popularity': track.get('popularity', None)}
            song_list.append(song)
    
    return song_list

spotify_global_top_50 = get_playlist_tracks(spotify_global_top_50_playlist_id, rapid_api_key)
df = pd.DataFrame(spotify_global_top_50)
df.sort_values("popularity", ascending=False, inplace=True)
df.reset_index(inplace=True, drop=True)
df.to_csv('spotify_global_top_50.csv', index=False)