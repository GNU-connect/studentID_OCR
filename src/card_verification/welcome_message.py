from src.response.basic_card import Card
import re

class CreateWelcomeMessage:
    def __init__(self, json):
        params = json['action']['params']['mobile_card_image_url']
        self.department, self.error_message = self.parse_params(params)
    
    def parse_params(params):
        # department와 error_message를 선택적으로 추출하는 정규 표현식 패턴
        pattern = r'department\s*->\s*(.+)|error_message\s*->\s*(.+)'

        # 정규 표현식 패턴을 사용하여 `params`에서 매치 찾기
        match = re.search(pattern, params)

        # `department`와 `error_message` 필드의 값 초기화
        department = None
        error_message = None

        # 매치가 있으면 `department`와 `error_message` 필드 값 추출
        if match:
            # 각 그룹의 매치 결과를 `None`에 대해 체크
            if match.group(1) is not None:
                department = match.group(1).strip(')')  # department 값 추출
            if match.group(2) is not None:
                error_message = match.group(2).strip(')')  # error_message 값 추출

        return department, error_message
    
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
    