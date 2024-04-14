import os, requests, json, s3fs, re
import pandas as pd

# df = pd.read_csv('spotify_songs.csv')

# # Remove duplicates

# # sort by track_popularity
# df.sort_values("track_popularity", ascending=False, inplace=True)

# # dropping rows with the same track_id
# df.drop_duplicates(subset="track_id", keep='first', inplace=True)

# df_final = df[['track_name', 'track_artist', 'track_popularity']].head(50)

# spotify_top_50 = df_final.to_csv('spotify-top-50.csv', index=False)

X_RAPID_API_KEY = 

def get_spotify_top_playlist_result(query:str) -> str:
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q":query,"type":"playlists","offset":"0","limit":"10","numberOfTopResults":"5"}

    headers = {
        "X-RapidAPI-Key": "614be38f4bmshf29cb3db90ab80dp12c424jsn4c4279b56ddf",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        playlist_uri = data.get('playlists', {}).get('items')[0].get('data').get('uri')
        playlist_id = re.search(r'playlist:(\S+)', playlist_uri).group(1)
    
    return playlist_id

spotify_global_top_50_playlist_id = get_spotify_top_playlist_result('global top 50')

def get_playlist_tracks(playlist_id:str) -> dict:
    url = "https://spotify23.p.rapidapi.com/playlist_tracks/"

    querystring = {"id":playlist_id,"offset":"0","limit":"50"}

    headers = {
        "X-RapidAPI-Key": "614be38f4bmshf29cb3db90ab80dp12c424jsn4c4279b56ddf",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)