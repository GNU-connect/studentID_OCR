from src.response.basic_card import Card
import re

class CreateWelcomeMessage:
    def __init__(self, json):
        params = json['action']['params']['mobile_card_image_url']
        pattern = r'department\s*->\s*([\w가-힣]+)|error\s*->\s*([\w가-힣]+)'
        matches = re.findall(pattern, params)
        print(matches)

        self.department = None
        self.error_message = None

        for match in matches:
            if match[0]:
                self.department = match[0]
            if match[1]:
                self.error_message = match[1]
    
    def create_message(self):
        print(self.department, self.error_message)
        # 에러 메시지가 있으면 error 메서드를 호출하고 반환
        if self.error_message:
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
    