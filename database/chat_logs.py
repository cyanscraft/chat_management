import requests

from utils.kakao_decrypt import KakaoDecrypt

decryptor = KakaoDecrypt()

def get_chat_logs(url:str, start_id:int, end_id:int, room_id:int):
    request_json = {"query": "SELECT c.id, c.chat_id, c.user_id, c.message, c.v, COALESCE(m.nickname, f.name) AS nickname, COALESCE(m.enc, f.enc) AS enc FROM chat_logs c LEFT JOIN open_chat_member m ON c.user_id = m.user_id LEFT JOIN friends f ON c.user_id = f.id WHERE c.id BETWEEN ? AND ? AND c.chat_id = ?;", "bind": [start_id, end_id, room_id]}
    headers = {'Accept': 'application/json'}
    query_result = requests.post(f"{url}/query", headers=headers, json=request_json).json()["data"]

    return query_result
