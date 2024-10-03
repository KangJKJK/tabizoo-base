import requests
import time

from smart_airdrop_claimer import base
from core.headers import headers
from core.info import get_info


def spin_info(data, proxies=None):
    url = "https://api.tabibot.com/api/spin/v1/info"

    try:
        response = requests.post(
            url=url, headers=headers(data=data), proxies=proxies, timeout=20
        )
        data = response.json()
        energy = data["data"]["energy"]["energy"]
        return energy
    except:
        return None


def play_spin(data, multiplier, proxies=None):
    url = "https://api.tabibot.com/api/spin/v1/play"
    payload = {"multiplier": multiplier}

    try:
        response = requests.post(
            url=url,
            headers=headers(data=data),
            json=payload,
            proxies=proxies,
            timeout=20,
        )
        data = response.json()
        prize = data["data"]["prize"]
        return prize
    except:
        return None


def process_spin(data, multiplier, proxies=None):
    while True:
        # 스핀 정보 가져오기
        energy = spin_info(data=data, proxies=proxies)
        if energy is not None:
            if energy > 0:
                final_multiplier = min(multiplier, energy)
                # 스핀 실행
                prize = play_spin(
                    data=data, multiplier=final_multiplier, proxies=proxies
                )
                if prize:
                    prize_type = prize["prize_type"]
                    amount = prize["amount"]
                    multiplier = prize["multiplier"]
                    if amount > 0:
                        base.log(
                            f"{base.white}자동 스핀: {base.green}성공 | {amount*multiplier} {prize_type} 추가됨"
                        )
                    else:
                        base.log(
                            f"{base.white}자동 스핀: {base.green}성공 | {base.red}{amount*multiplier} {prize_type}"
                        )
                    # 정보 업데이트
                    get_info(data=data, proxies=proxies)
                    time.sleep(1)
                else:
                    base.log(f"{base.white}자동 스핀: {base.red}실패")
                    break
            else:
                base.log(f"{base.white}자동 스핀: {base.red}스핀할 에너지가 없습니다")
                break
        else:
            base.log(f"{base.white}자동 스핀: {base.red}에너지 데이터를 찾을 수 없습니다")
            break
