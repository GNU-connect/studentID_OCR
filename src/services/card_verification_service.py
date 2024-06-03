from src.models.college_dto import get_college_info_by_department_id
from src.models.department_dto import get_department_name_by_id
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
from difflib import SequenceMatcher
from src.common.utils.slack import Slack_Notifier
from src.common.response.basic_card import Card
from src.models.user_dao import get_user_info, save_user_info
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
        def get_similarity(a, b):
            return SequenceMatcher(None, a, b).ratio()
        
        configs = [r'--oem 1 --psm 4', r'--oem 3 --psm 6', r'--oem 1 --psm 3']
        try:
            for config in configs:
                img = img.convert('L') # 흑백 이미지로 변환
                texts = pytesseract.image_to_string(img, lang='kor', config=config)
                text_list = [text.strip() for text in texts.split('\n')]
                logger.info(f"{config} 옵션 ocr 결과\n{text_list}")

                # TODO: text_list가 너무 많은 경우 예외 처리 필요
                
                # 1차: 학과명이 정확히 일치하는 경우 탐색
                for text in text_list:
                    for department in departments:
                        if text.replace(' ', '') == department:
                            return department

                # 2차: 유사도가 0.75 이상인 학과 탐색
                for text in text_list:
                    for department in departments:
                        similarity = get_similarity(text.replace(' ', ''), department)
                        if similarity >= 0.75:
                            return department
                
                # 3차: 유사도가 0.55 이상인 학과 탐색
                # TODO: 영어영문학부 같이 하위 학과가 있는 경우 예외 처리 필요
                for text in text_list:
                    for department in departments:
                        similarity = get_similarity(text.replace(' ', ''), department)
                        if similarity >= 0.55:
                            return department

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
            logger.info(f"유사도: {similarity}")
            
            return similarity
        except Exception as e:
            logger.error(e)
    
    # 학과 정보 매칭
    def match_department(department):
        for row in supabase_response:
            if row['department_ko'] == department:
                return row['id']
        return None

    user_info = get_user_info(user_id)
    # 예외 처리: 이미 인증된 사용자인 경우
    if user_info:
        department_name = get_department_name_by_id(user_info[0]['department_id'])
        college_name = get_college_info_by_department_id(user_info[0]['department_id'])['name_ko']
        info_message = f'이미 {college_name} {department_name}로 인증된 상태야! 혹시라도 학과 정보가 잘못 등록된 것 같다면 관리자에게 문의해줘!'
        logger.info(info_message)
        return {'status': "FAIL", 'value': {'error_message': info_message}}
        
    try:
        # 이미지 파일 경로를 설정합니다.
        file_name = join(dirname(dirname(dirname(__file__))), 'temp', f'{user_id}.jpg')

        # 이미지 다운로드
        if os.getenv("FLASK_ENV") != 'test':
            download_user_mobile_card(image_url, file_name)
        
        # 예외 처리: 유사도가 기준 미달인 경우
        similarity = capture_similarity(test_image_file_path, file_name)
        if similarity < 0.7:
            warn_message = '올바르지 않은 이미지인 것 같아 ㅠㅠ'
            logger.warn(f"{warn_message}")
            return {'status': "FAIL", 'value': {'error_message': f'{warn_message} 오류가 계속 발생하면 관리자에게 문의해줘!'}}
        
        # 이미지 로드
        img = Image.open(file_name)
        department = img_ocr(img)

        # 예외 처리: 서비스에서 등록되지 않은 학과인 경우
        if department is None:
            warn_message = '학과 정보를 확인할 수 없어 ㅠㅠ'
            logger.error(warn_message)
            return {'status': "FAIL", 'value': {'error_message': f'{warn_message} 오류가 계속 발생하면 관리자에게 문의해줘!'}}
        
        department_id = match_department(department)
        college_info = get_college_info_by_department_id(department_id)
        # 사용자 정보 저장
        if os.getenv("FLASK_ENV") != 'test':
            save_user_info(user_id, department_id)

        logger.info(f"[성공] 유저 id: {user_id} - {department} 인증 완료, 유사도: {similarity}")
        return {'status': "SUCCESS", 'value': {'department': department, 'college': college_info}}
    
    except Exception as e:
        logger.error(e)
        Slack_Notifier().fail(e)
        return {'status': "FAIL", 'value': {'error_message': '이미지 처리 중 오류가 발생했어 ㅠㅠ 오류가 계속 발생하면 관리자에게 문의해줘!'}}
    finally:
        if os.getenv("FLASK_ENV") != 'test' and user_info is None:
            print(user_info)
            os.remove(file_name)

class CreateWelcomeMessage:
    def __init__(self, certification_result):
        self.department = certification_result['value']['department'] if 'value' in certification_result \
                            and 'department' in certification_result['value'] else None
        self.college = certification_result['value']['college'] if 'value' in certification_result \
                            and 'college' in certification_result['value'] else None
        self.error_message = certification_result['value']['error_message'] if 'value' in certification_result \
                             and 'error_message' in certification_result['value'] else None
    
    def create_message(self):
        # 에러 메시지가 있으면 error 메서드를 호출하고 반환
        if self.error_message is not None:
            return self.error()
        # 그렇지 않으면 greet 메서드를 호출하고 반환
        return self.greet()

    def greet(self):
        # 단과대학 로고가 없는 경우 기본 이미지로 설정
        return Card(
            title=f"🎉 {self.college['name_ko']} {self.department} 인증 완료!",
            description="혹시라도 잘못 인증된 것 같다면 관리자에게 문의해줘!",
            thumbnail=self.college["thumbnail_url"]
        ).result_json()

    def error(self):
        return Card(title="🥲 인증 실패", 
                    description=f"{self.error_message}",
                    thumbnail="https://mir-s3-cdn-cf.behance.net/project_modules/disp/087699154238883.633e7921ea3ae.gif").result_json()