#!-/python

import logging
import signal
import sys
from DiskChecker import DiskChecker
from NaverBot import Bot
import json
import time

# Log handling
logger = logging.getLogger('DiskChecker')
logger.setLevel(logging.WARNING)  # 로거의 레벨 설정
file_handler = logging.FileHandler('/var/log/disk.log')
file_handler.setLevel(logging.WARNING)  # 파일 핸들러의 레벨 설정
formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s', datefmt='%y-%m-%d %H:%M:%S')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Error handling
def terminate_handler(signal, frame):
    logger.warning('Service Off')
    sys.exit(0)
signal.signal(signal.SIGTERM, terminate_handler)

# Main
if __name__ == '__main__':
    diskchecker = DiskChecker() # 디스크 점검 인스턴스
    bot = Bot() # 메시지 봇 인스턴스
    while True:
        diskchecker.get_drive_status() # 디스크 상태 업데이트
        diskchecker.get_drive_missing()
        diskchecker.get_drive_differences()
        if diskchecker.drives_curr and diskchecker.drives_prev!= diskchecker.drives_curr:
            logger.warning(json.dumps(diskchecker.drives_curr, ensure_ascii=False)) # 에러 발생 시 로깅
            try:
                bot.assertion() # 메시지 봇에 로그인
                users = bot.get_user_id('-') # 메시지 봇에서 발송할 대상자 체크
                bot.send_message(diskchecker.get_pretty_str(), users) # 메시지 발송
            except Exception as e:
                logger.exception(e)
        time.sleep(60)
