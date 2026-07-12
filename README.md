# francisDiskMonitoring
나만의 디스크 모니터링 코드

1. NaverBot.py 의 아래의 값을 잘 채워 넣는다.
    self.__client_id = ''
    self.__client_secret = ''
    self.__service_account = ''
    self.__bot_id = ''
    self.__baseurl = ''
    with open('-pk.key', 'rb') as f:
        self.__private_key = f.read()

2. main.py 의 아래의 값을 잘 채워 넣는다.
#!-/python
users = bot.get_user_id('-') # 메시지 봇에서 발송할 대상자 체크

3. main.py를 실행시킨다. 
