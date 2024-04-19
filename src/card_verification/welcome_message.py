import json
from src.response.basic_card import Card

class CreateWelcomeMessage:
    def __init__(self, params):
        self.name = params.json['userRequest']['user']['name']
        self.department = params.json['value']['department']

    def greet(self):
        return Card({
            "title": "🎉 우리 학교 인증 완료",
            "description": f"{self.department} {self.name}님 커넥트 지누의 다양한 서비스를 이용해보세요 :)",
            "thumbnail": {
                "imageUrl": "https://www.gnu.ac.kr/images/web/main/sub_cnt/as_1_05.png"
            }
        }).to_dict()
    