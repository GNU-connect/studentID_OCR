import json
from src.response.basic_card import Card
import re

class CreateWelcomeMessage:
    def __init__(self, json):
        print(json)
        params = json['action']['params']['mobile_card_image_url']
        department_match = re.search(r'department\s*->\s*([\w가-힣]+)', params)
        self.department = department_match.group(1)

    def greet(self):
        return Card(title=f"🎉 {self.department} 인증 완료", 
                    description="커넥트 지누가 당신을 환영합니다 !",
                    thumbnail="https://www.gnu.ac.kr/images/web/main/sub_cnt/as_1_05.png").result_json()
    