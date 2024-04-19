from src.response.basic_card import Card
import re

class CreateWelcomeMessage:
    def __init__(self, json):
        params = json['action']['params']['mobile_card_image_url']
        department_match = re.search(r'department\s*->\s*([\w가-힣]+)', params)
        error_match = re.search(r'error_message\s*->\s*([\w가-힣]+)', params)

        self.department = None
        self.error_message = None

        if department_match is not None:
            self.department = department_match.group(1)
        if error_match is not None:
            self.error_message = error_match.group(1)
    
    def create_message(self):
        # 에러 메시지가 있으면 error 메서드를 호출하고 반환
        if self.error_message is not None:
            return self.error()
        # 그렇지 않으면 greet 메서드를 호출하고 반환
        return self.greet()

    def greet(self):
        return Card(title=f"🎉 {self.department} 인증 완료", 
                    description="커넥트 지누가 당신을 환영합니다 !",
                    thumbnail="https://www.gnu.ac.kr/images/web/main/sub_cnt/as_1_05.png").result_json()

    def error(self):
        return Card(title="🥲 인증 실패", 
                    description=f"{self.error_message}",
                    thumbnail="https://www.gnu.ac.kr/images/web/main/sub_cnt/as_1_42.png").result_json()
    