import os, requests, json, s3fs, re
import pandas as pd
from dotenv import load_dotenv
from rich import print, print_json
from functions import get_spotify_top_playlist_result, get_playlist_tracks_raw_data, transform_raw_playlist_data

load_dotenv()
rapid_api_key = os.getenv("X_RAPID_API_KEY")

spotify_global_top_50_playlist_id = get_spotify_top_playlist_result('global top 50', rapid_api_key)
spotify_global_top_50_raw_playlist_data = get_playlist_tracks_raw_data(spotify_global_top_50_playlist_id, rapid_api_key)

spotify_global_top_50 = None
if spotify_global_top_50_raw_playlist_data:
    spotify_global_top_50 = transform_raw_playlist_data(spotify_global_top_50_raw_playlist_data)

df = pd.DataFrame(spotify_global_top_50)
df.sort_values("popularity", ascending=False, inplace=True)
df.reset_index(inplace=True, drop=True)
df.to_csv('spotify_global_top_50.csv', index=False)