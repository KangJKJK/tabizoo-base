import sys

sys.dont_write_bytecode = True

from smart_airdrop_claimer import base
from core.info import get_info
from core.task import process_check_in, process_do_project_task, process_do_normal_task
from core.mine import process_claim
from core.spin import process_spin
from core.upgrade import process_upgrade

import time
import json


class TabiZoo:
    def __init__(self):
        # 파일 디렉토리 가져오기
        self.data_file = base.file_path(file_name="data-proxy.json")
        self.config_file = base.file_path(file_name="config.json")

        # 라인 초기화
        self.line = base.create_line(length=50)

        # 배너 초기화
        self.banner = base.create_banner(game_name="TabiZoo")

        # 설정 가져오기
        self.auto_check_in = base.get_config(
            config_file=self.config_file, config_name="auto-check-in"
        )

        self.auto_do_task = base.get_config(
            config_file=self.config_file, config_name="auto-do-task"
        )

        self.auto_claim = base.get_config(
            config_file=self.config_file, config_name="auto-claim"
        )

        self.auto_spin = base.get_config(
            config_file=self.config_file, config_name="auto-spin"
        )

        self.auto_upgrade = base.get_config(
            config_file=self.config_file, config_name="auto-upgrade"
        )

    def main(self):
        while True:
            base.clear_terminal()
            print(self.banner)
            accounts = json.load(open(self.data_file, "r"))["accounts"]
            num_acc = len(accounts)
            base.log(self.line)
            base.log(f"{base.green}계정 수: {base.white}{num_acc}")

            for no, account in enumerate(accounts):
                base.log(self.line)
                base.log(f"{base.green}계정 번호: {base.white}{no+1}/{num_acc}")
                data = account["acc_info"]
                proxy_info = account["proxy_info"]
                parsed_proxy_info = base.parse_proxy_info(proxy_info)
                if parsed_proxy_info is None:
                    break

                actual_ip = base.check_ip(proxy_info=proxy_info)

                proxies = base.format_proxy(proxy_info=proxy_info)

                try:
                    # 정보 가져오기
                    get_info(data=data, proxies=proxies)

                    # 체크인
                    if self.auto_check_in:
                        base.log(f"{base.yellow}자동 체크인: {base.green}켜짐")
                        process_check_in(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}자동 체크인: {base.red}꺼짐")

                    # 작업 수행
                    if self.auto_do_task:
                        base.log(f"{base.yellow}자동 작업 수행: {base.green}켜짐")
                        process_do_project_task(data=data, proxies=proxies)
                        process_do_normal_task(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}자동 작업 수행: {base.red}꺼짐")

                    # 클레임
                    if self.auto_claim:
                        base.log(f"{base.yellow}자동 클레임: {base.green}켜짐")
                        process_claim(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}자동 클레임: {base.red}꺼짐")

                    # 스핀
                    if self.auto_spin:
                        base.log(f"{base.yellow}자동 스핀: {base.green}켜짐")
                        process_spin(data=data, multiplier=1, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}자동 스핀: {base.red}꺼짐")

                    # 업그레이드
                    if self.auto_upgrade:
                        base.log(f"{base.yellow}자동 업그레이드: {base.green}켜짐")
                        process_upgrade(data=data, proxies=proxies)
                    else:
                        base.log(f"{base.yellow}자동 업그레이드: {base.red}꺼짐")

                except Exception as e:
                    base.log(f"{base.red}오류: {base.white}{e}")

            print()
            wait_time = 60 * 60
            base.log(f"{base.yellow}{int(wait_time/60)}분 동안 대기! 스크립트 작성자: https://t.me/kjkresearch")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        tabi = TabiZoo()
        tabi.main()
    except KeyboardInterrupt:
        sys.exit()
