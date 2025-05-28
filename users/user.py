import requests

def get_open_chat_member(userid:str, url):
    request_json = {"query": "SELECT * from open_chat_member WHERE user_id=?", "bind": [userid]}
    headers = {'Accept': 'application/json'}
    query_result = requests.post(f"{url}/query", headers=headers, json=request_json).json()["data"]
    return query_result[0]

