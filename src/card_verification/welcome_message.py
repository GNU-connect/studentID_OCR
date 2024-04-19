import json
from src.response.basic_card import Card
import re

class CreateWelcomeMessage:
    def __init__(self, json):
        params = json['action']['params']['mobile_card_image_url']
        # Map(department -> 컴퓨터공학과, name -> 홍길동)
        name_match = re.search(r'name\s*->\s*([\w가-힣]+)', params)
        department_match = re.search(r'department\s*->\s*([\w가-힣]+)', params)
        self.name = name_match.group(1)
        self.department = department_match.group(1)

    def greet(self):
        return Card(title="🎉 우리 학교 인증 완료", 
                    description=f"{self.department} {self.name}님 커넥트 지누의 다억한 서비스를 이용해보세요 :)", 
                    thumbnail="https://www.gnu.ac.kr/images/web/main/sub_cnt/as_1_05.png").result_json()
    