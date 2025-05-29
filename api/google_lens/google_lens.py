import requests
import re
from bs4 import BeautifulSoup

def get_lens_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36"
    }
    url = "https://images.google.com"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        html = response.text

        # kOPI 추출
        kopi_match = re.search(r'kOPI\s*:\s*(\d+)', html)
        kopi = kopi_match.group(1) if kopi_match else "없음"

        # Yllh3e 추출
        yllh3e_match = re.search(r'"Yllh3e":"([^"]+)"', html)
        yllh3e = yllh3e_match.group(1) if yllh3e_match else "없음"

        # data-ved 추출 (BeautifulSoup 사용)
        soup = BeautifulSoup(html, "html.parser")
        data_ved = "없음"
        print(soup)
        for c_wiz in soup.find_all("c-wiz"):
            data_ved_val = c_wiz.get("data-ved")
            if data_ved_val:
                data_ved = data_ved_val
                break

        return kopi, yllh3e, data_ved
    else:
        return None, None, None

# 사용 예시
kopi, yllh3e, data_ved = get_lens_data()
print("kOPI:", kopi)
print("Yllh3e:", yllh3e)
print("data-ved:", data_ved)
