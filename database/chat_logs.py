import requests

from utils.kakao_decrypt import KakaoDecrypt

decryptor = KakaoDecrypt()

def get_chat_logs(url:str, start_id:int, end_id:int, room_id:int):
    request_json = {"query": "SELECT c.id, c.chat_id, c.user_id, c.message, m.nickname, m.enc FROM chat_logs c JOIN open_chat_member m ON c.user_id = m.user_id WHERE c.id BETWEEN ? AND ? AND c.chat_id = ?;", "bind": [start_id, end_id, room_id]}
    headers = {'Accept': 'application/json'}
    query_result = requests.post(f"{url}/query", headers=headers, json=request_json).json()["data"]

    final_result = []
    for row in query_result:
        try:
            decrypted_message = decryptor.decrypt(
                int(row["user_id"]),
                int(row["enc"]),
                row["message"]
            )
            row["message"] = decrypted_message
        except Exception as e:
            print(f"복호화 실패: {e}")
            row["message"] = "[복호화 실패]"

        final_result.append(row)

    return query_result
