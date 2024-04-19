from src.response.basic_card import Card
import re

class CreateWelcomeMessage:
    def __init__(self, json):
        params = json['action']['params']['mobile_card_image_url']
        department_match = re.search(r'department\s*->\s*([\w가-힣]+)', params)
        error_match = re.search(r'error\s*->\s*([\w가-힣]+)', params)
        self.department = department_match.group(1) if department_match else None
        self.error_message = error_match.group(1) if error_match else None
    
    def create_message(self):
        print(self.department, self.error_message)
        return self.error() if self.error_message else self.greet() # 에러 메시지가 있는 경우 에러 메시지를 반환하고, 없는 경우 환영 메시지를 반환합니다.

    def greet(self):
        return Card(title=f"🎉 {self.department} 인증 완료", 
                    description="커넥트 지누가 당신을 환영합니다 !",
                    thumbnail="https://www.gnu.ac.kr/images/web/main/sub_cnt/as_1_05.png").result_json()

    def error(self):
        return Card(title="🥲 인증 실패", 
                    description=f"{self.error_message}",
                    thumbnail="https://www.gnu.ac.kr/images/web/main/sub_cnt/as_1_42.png").result_json()
    