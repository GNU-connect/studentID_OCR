from src.common.utils.supabase import supabase
import torchvision.transforms as T
import pytesseract
import torch
from numpy import dot
from numpy.linalg import norm
import requests
from PIL import Image
import os
from os.path import join, dirname
from dotenv import load_dotenv
import gdown
from torchvision import models
import re
from src.common.utils.slack import Slack_Notifier
from src.common.response.basic_card import Card
import logging
logger = logging.getLogger()

# .env 파일을 불러오기 위한 설정
dotenv_path = join(dirname(dirname(dirname(__file__))), '.env')
load_dotenv(dotenv_path)

# 학과 정보 불러오기
supabase_response = supabase().table('department').select("id", "department_ko").execute().data
departments = [row['department_ko'].replace(' ', '') for row in supabase_response]

# 사전 훈련된 ResNet18 모델 로드
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.eval()

# test 이미지 저장 경로 설정
drive_file_url = os.getenv('CARD_VARIFICATION_IMAGE_URL')
test_image_file_path = join(dirname(dirname(dirname(__file__))), 'temp', 'test.jpg')
os.makedirs(os.path.dirname(test_image_file_path), exist_ok=True)
if not os.path.exists(test_image_file_path):
    gdown.download(drive_file_url, test_image_file_path, quiet=False)

# 사용자 모바일 카드 확인
def verify_user_mobile_card(user_id, image_url):
    # 이미지 다운로드 함수
    def download_user_mobile_card(image_url, file_name):
        try:
            response = requests.get(image_url)
            with open(file_name, 'wb') as f:
                f.write(response.content)
        except Exception as e:
            logger.error(e)
    
    # 이미지 OCR 함수
    def img_ocr(img):
        configs = [r'--oem 1 --psm 4', r'--oem 3 --psm 6', r'--oem 1 --psm 3']
        try:
            for config in configs:
                img = img.convert('L') # 흑백 이미지로 변환
                texts = pytesseract.image_to_string(img, lang='kor', config=config)
                text_list = [text.strip() for text in texts.split('\n')]
                logger.info(f"OCR 결과: {text_list}")
                
                for text in text_list:
                    text = re.sub(r'\s+', '', text)
                    logger.info(f"학과 정보: {text}")
                    if text in departments:
                        return text
        except Exception as e:
            logger.error(e)
    
    # 특성 추출 및 유사도 계산 함수
    def capture_similarity(original_image_path, test_image_path):
        # 이미지 로드 및 전처리 함수
        def image_preprocess(image_path):
            image = Image.open(image_path).convert("RGB")
            preprocess = T.Compose([
                T.Resize(224),
                T.CenterCrop(224),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            return preprocess(image).unsqueeze(0)
        
        def cos_sim(A, B):
            return dot(A, B) / (norm(A) * norm(B))
        try:
            # 이미지 전처리
            original_image = image_preprocess(original_image_path)
            test_image = image_preprocess(test_image_path)
            
            # 특성 추출
            with torch.no_grad():
                original_embedding = model(original_image).flatten().numpy()
                test_embedding = model(test_image).flatten().numpy()
            
            # 코사인 유사도 계산
            similarity = cos_sim(original_embedding, test_embedding)
            
            return similarity
        except Exception as e:
            logger.error(e)

    # 데이터베이스에 사용자 정보 저장
    def save_user_info(user_id, department_id):
        # 'kakao-user' 테이블에 데이터 삽입
        data = {'id': user_id, 'department_id': department_id}
        supabase().table('kakao-user').upsert(data).execute()
    
    # 학과 정보 매칭
    def match_department(department):
        for row in supabase_response:
            if row['department_ko'] == department:
                return row['id']
        return None

    try:
        user_info = supabase().table('kakao-user').select('id').eq('id', user_id).execute().data
        # 예외 처리: 이미 인증된 사용자인 경우
        if user_info:
            info_message = '이미 인증된 사용자입니다.'
            logger.info(info_message)
            return {'status': "FAIL", 'value': {'error_message': info_message}}
        
        # 이미지 파일 경로를 설정합니다.
        file_name = join(dirname(dirname(dirname(__file__))), 'temp', f'{user_id}.jpg')

        # 이미지 다운로드
        if os.getenv("FLASK_ENV") != 'test':
            download_user_mobile_card(image_url, file_name)
        
        # 예외 처리: 유사도가 기준 미달인 경우
        similarity = capture_similarity(test_image_file_path, file_name)
        if similarity < 0.7:
            warn_message = '올바르지 않은 이미지입니다. 다시 시도해주세요.'
            logger.warn(f"{warn_message} - 유사도: {similarity}")
            return {'status': "FAIL", 'value': {'error_message': f'{warn_message} 지속적인 오류 발생 시 1:1 문의를 이용해주세요.'}}
        
        # 이미지 로드
        img = Image.open(file_name)
        department = img_ocr(img)

        # 예외 처리: 학과 정보가 없는 경우
        if department is None:
            warn_message = '모바일 카드에서 학과 정보를 인식할 수 없습니다. 다시 시도해주세요.'
            logger.error(warn_message)
            return {'status': "FAIL", 'value': {'error_message': f'{warn_message} 지속적인 오류 발생 시 1:1 문의를 이용해주세요.'}}
        
        # 사용자 정보 저장
        if os.getenv("FLASK_ENV") != 'test':
            save_user_info(user_id, match_department(department))

        logger.info(f"[성공] 유저 id: {user_id} - {department} 인증 완료, 유사도: {similarity}")
        return {'status': "SUCCESS", 'value': {'department': department}}
    
    except Exception as e:
        logger.error(e)
        Slack_Notifier().fail(e)
        return {'status': "FAIL", 'value': {'error_message': '이미지 처리 중 오류가 발생했습니다. 지속적인 오류 발생 시 1:1 문의를 이용해주세요.'}}
    finally:
        if os.getenv("FLASK_ENV") != 'test':
            os.remove(file_name)

class CreateWelcomeMessage:
    def __init__(self, certification_result):
        self.department = certification_result['value']['department'] if 'value' in certification_result \
                            and 'department' in certification_result['value'] else None
        self.error_message = certification_result['value']['error_message'] if 'value' in certification_result \
                             and 'error_message' in certification_result['value'] else None
    
    def create_message(self):
        # 에러 메시지가 있으면 error 메서드를 호출하고 반환
        if self.error_message is not None:
            return self.error()
        # 그렇지 않으면 greet 메서드를 호출하고 반환
        return self.greet()

    def greet(self):
        return Card(title=f"🎉 {self.department} 인증 완료", 
                    description="커넥트 지누가 당신을 환영합니다 !",
                    thumbnail="https://mir-s3-cdn-cf.behance.net/project_modules/disp/626139154238883.633e7921e8b21.gif").result_json()

    def error(self):
        return Card(title="🥲 인증 실패", 
                    description=f"{self.error_message}",
                    thumbnail="https://mir-s3-cdn-cf.behance.net/project_modules/disp/087699154238883.633e7921ea3ae.gif").result_json()