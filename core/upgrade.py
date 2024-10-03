import requests

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info


def upgrade(data, proxies=None):
    url = "https://api.tabibot.com/api/user/v1/level-up"

    try:
        response = requests.post(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        status = data["code"]
        return status
    except:
        return None


def process_upgrade(data, proxies=None):
    # 업그레이드 상태 확인
    upgrade_status = upgrade(data=data, proxies=proxies)
    if upgrade_status == 200:
        base.log(f"{base.white}자동 업그레이드: {base.green}성공")
        get_info(data=data, proxies=proxies)
    elif upgrade_status == 400:
        base.log(f"{base.white}자동 업그레이드: {base.red}코인이 부족합니다")
    else:
        base.log(f"{base.white}자동 업그레이드: {base.red}알 수 없는 상태")
