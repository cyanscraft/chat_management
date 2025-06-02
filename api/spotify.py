import os

import requests
import time
import base64

from dotenv import load_dotenv

load_dotenv()  # .env 파일을 읽어서 환경변수로 등록함

# === Spotify App Credentials ===
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:3000'
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH")

# === Access Token 상태 ===
access_token = 'BQCr7s2cGRmhQPbmwGPuImjiMGXgblLaXFNuWREHjpKajgyyLwXxble7MxMjulDgBygTzRt8T6afpvEO_VWnPtl9A83ApNFREJOdA54HLRbfTc4R2bZQYQxJRmujEjk2bpN7Nfl3ICi0QwqQgNxNHGm-dojMr3I3SNHF74_0Kj4zT1HLYiUiTreYhpzGSgurH8FgDyD3P9nv_H1H9T-JpXCyT3yMX2VZV_FI5bJE4Md4FU_lmtapmg'
access_token_expires_at = 0


def get_access_token():
    global access_token, access_token_expires_at

    if access_token and time.time() < access_token_expires_at:
        return access_token

    print('[!] Access token expired or not available. Refreshing...')

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN,
        },
        headers={
            'Authorization': f'Basic {b64_auth_str}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to refresh token: {response.text}")

    token_data = response.json()
    access_token = token_data['access_token']
    expires_in = token_data.get('expires_in', 3600)
    access_token_expires_at = time.time() + expires_in - 10  # 여유 10초

    return access_token


def search_track(query, limit=1):
    token = get_access_token()

    response = requests.get(
        'https://api.spotify.com/v1/search',
        headers={
            'Authorization': f'Bearer {token}',
        },
        params={
            'q': query,
            'type': 'track',
            'limit': limit,
        }
    )

    if response.status_code != 200:
        raise Exception(f"Search failed: {response.text}")

    results = response.json()
    return results.get('tracks', {}).get('items', [])

def get_current_device():
    token = get_access_token()

    response = requests.get(
        'https://api.spotify.com/v1/me/player',
        headers={
            'Authorization': f'Bearer {token}',
        }
    )
    if response.status_code == 204:
        return 204
    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Search failed: {response.text}")

    results = response.json()
    return results

def get_current_track():
    token = get_access_token()

    response = requests.get(
        'https://api.spotify.com/v1/me/player/currently-playing?market=KR',
        headers={
            'Authorization': f'Bearer {token}',
        }
    )

    if response.status_code == 204:
        return 204
    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Search failed: {response.text}")

    results = response.json()
    return results

def spotify_next():
    token = get_access_token()
    device = get_current_device()
    device_id = device['device']['id']

    response = requests.post(
        f'https://api.spotify.com/v1/me/player/next?device_id={device_id}',
        headers={
            'Authorization': f'Bearer {token}',
        }
    )
    time.sleep(0.5)
    return get_current_track()
def spotify_prev():
    token = get_access_token()
    device = get_current_device()
    device_id = device['device']['id']

    response = requests.post(
        f'https://api.spotify.com/v1/me/player/previous?device_id={device_id}',
        headers={
            'Authorization': f'Bearer {token}',
        }
    )
    time.sleep(0.5)
    return get_current_track()
def spotify_pause():
    token = get_access_token()
    device = get_current_device()
    device_id = device['device']['id']

    response = requests.put(
        f'https://api.spotify.com/v1/me/player/pause?device_id={device_id}',
        headers={
            'Authorization': f'Bearer {token}',
        }
    )

    return response
def spotify_play():
    token = get_access_token()
    device = get_current_device()
    device_id = device['device']['id']

    response = requests.put(
        f'https://api.spotify.com/v1/me/player/play?device_id={device_id}',
        headers={
            'Authorization': f'Bearer {token}',
        }
    )

    return response

def spotify_playlist():
    ...


# === 테스트 ===
if __name__ == '__main__':
    keyword = input("검색할 노래 제목: ")
    results = search_track(keyword)
    for i, track in enumerate(results):
        print(f"{i + 1}. {track['name']} - {track['artists'][0]['name']}")
        print(f"   URL: {track['external_urls']['spotify']}")

