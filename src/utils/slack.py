import requests
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(verbose=True)

class Slack_Notifier:
    def __init__(self):
        # Slack 웹훅 URL 환경 변수에서 가져오기
        self.url = os.getenv("SLACK_WEBHOOK_URL")
        # HTTP 헤더 설정
        self.headers = {
            'Content-Type': 'application/json',
        }
    
    def success(self):
        # 성공 메시지 생성
        data = {
            'text': 'Successfully scraped all web pages.'
        }
        # Slack에 메시지 보내기
        response = requests.post(self.url, headers=self.headers, json=data)
        
        # 응답 상태 코드 확인
        if response.status_code != 200:
            print('Failed to send success notification:', response.status_code, response.text)
    
    def fail(self, error_message=None):
        # 실패 메시지 생성
        data = {
            'text': error_message
        }
        # Slack에 메시지 보내기
        response = requests.post(self.url, headers=self.headers, json=data)
        
        # 응답 상태 코드 확인
        if response.status_code != 200:
            print('Failed to send success notification:', response.status_code, response.text)