import requests
import base64

# 필수 정보
CLIENT_ID = '0b5da16ffd1b49c1b10a5766f642ac78'
CLIENT_SECRET = '51d4eaa6dc694103912d138ed833c71d'
REDIRECT_URI = 'http://localhost:3000/'
CODE = 'AQD8UDZN1lHaNIss0_myhjxPkPYBcOz1fJZGTy6fnQNYmmPrZ1-y49lQ4c5ERwGUU3oBs7wCH8jEYl1f44flzrmeDXgoZ3n38OkJKOpzHCXZu13bijL6eH-1iq4TvymtFwNu0yeqkxsPCLK5pv8CFjPl6Ems6AEdR55F4acsg7_Fn0U4bBUX4omJvOdgSEubyhBXhkQIK-sjDd3kgYbNKEKE6HSN3M3rlNLl1O5Ew6IPIBExRr6lGDC_xxdxmJgt4K-Hmq3tFfQKlZCkoA'
# Base64 인코딩된 인증 문자열
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

# POST 요청
response = requests.post(
    'https://accounts.spotify.com/api/token',
    data={
        'grant_type': 'authorization_code',
        'code': CODE,
        'redirect_uri': REDIRECT_URI,
    },
    headers={
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
)

# 결과 출력
if response.status_code == 200:
    token_data = response.json()
    print("access_token:", token_data['access_token'])
    print("refresh_token:", token_data['refresh_token'])
else:
    print("실패:", response.status_code, response.text)