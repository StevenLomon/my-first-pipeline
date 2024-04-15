import boto3.session
import requests, re, json, boto3
from botocore.exceptions import ClientError

def get_secret():
    secret_name = "rapid_api/api_key"
    region_name = "eu-north-1"

    # Create a Secrests Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    
    secret = get_secret_value_response['SecretString']
    return secret


def get_spotify_top_playlist_result(api_key) -> str:
    url = "https://spotify23.p.rapidapi.com/search/"

    querystring = {"q":"global top 50","type":"playlists","offset":"0","limit":"1"}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    # print(f"First API call response status code: {response.status_code}")

    # playlist_id = None
    # if response.status_code == 200:
    #     data = response.json()
    #     playlist_uri = data.get('playlists', {}).get('items', [{}])[0].get('data', {}).get('uri', None)
    #     playlist_id = re.search(r'playlist:(\S+)', playlist_uri).group(1)
    
    # return playlist_id

def get_playlist_tracks_raw_data(playlist_id:str, api_key) -> json:
    url = "https://spotify23.p.rapidapi.com/playlist_tracks/"

    querystring = {"id":playlist_id,"offset":"0","limit":"50"}

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json() if response.status_code == 200 else None

def transform_raw_playlist_data(raw_data:json) -> list[dict]:
    song_list = []

    items = raw_data.get('items', [{}])
    for item in items:
        track = item.get('track', {})
        song = {'id': track.get('id', None),
                'title': track.get('name', None),
                'artist': track.get('artists', [{}])[0].get('name', None),
                'popularity': track.get('popularity', None)}
        song_list.append(song)
    
    return song_list