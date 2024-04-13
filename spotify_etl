import json, s3fs
import pandas as pd

df = pd.read_csv('spotify_songs.csv')

# Remove duplicates

# sort by track_popularity
df.sort_values("track_popularity", ascending=False, inplace=True)

# dropping rows with the same track_id
df.drop_duplicates(subset="track_id", keep='first', inplace=True)

df_final = df[['track_name', 'track_artist', 'track_popularity']].head(50)

spotify_top_50 = df_final.to_csv('spotify-top-50.csv', index=False)