import os, requests, json, re
import pandas as pd
from rich import print, print_json
from functions import get_secret, get_spotify_top_playlist_result, get_playlist_tracks_raw_data, transform_raw_playlist_data

secret = get_secret()

# def extract_raw_data():
spotify_global_top_50_playlist_id = get_spotify_top_playlist_result(secret)
spotify_global_top_50_raw_playlist_data = get_playlist_tracks_raw_data(spotify_global_top_50_playlist_id, secret)

print(spotify_global_top_50_raw_playlist_data)

# spotify_global_top_50 = None
# if spotify_global_top_50_raw_playlist_data:
#     spotify_global_top_50 = transform_raw_playlist_data(spotify_global_top_50_raw_playlist_data)

# df = pd.DataFrame(spotify_global_top_50)
# df.sort_values("popularity", ascending=False, inplace=True)
# df.reset_index(inplace=True, drop=True)
# df.to_csv('spotify_global_top_50.csv', index=False)