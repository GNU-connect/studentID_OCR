from src.utils.supabase import supabase
import torchvision.transforms as T
import pytesseract
import torch
from numpy import dot
from numpy.linalg import norm
import requests
from PIL import Image
import os
import json
from os.path import join, dirname
from dotenv import load_dotenv
import gdown
from torchvision import models
import re
import logging
logger = logging.getLogger("verification")

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
drive_file_url = os.environ['CARD_VARIFICATION_IMAGE_URL']
test_image_file_path = join(dirname(dirname(dirname(__file__))), 'temp', 'test.jpg')
os.makedirs(os.path.dirname(test_image_file_path), exist_ok=True)
gdown.download(drive_file_url, test_image_file_path, quiet=False)

# 이미지 OCR 함수
def img_ocr(img):
    custom_configs = [r'--oem 1 --psm 4', r'--oem 3 --psm 6', r'--oem 1 --psm 3']
    for config in custom_configs:
        texts = pytesseract.image_to_string(img, lang='kor', config=config)
        text_list = [text.strip() for text in texts.split('\n')]
        
        for text in text_list:
            text = re.sub(r'\s+', '', text)
            if text in departments:
                return text
    return None

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

# 코사인 유사도 계산 함수
def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

# 특성 추출 및 유사도 계산 함수
def capture_similarity(original_image_path, test_image_path):
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

# 데이터베이스에 사용자 정보 저장
def save_user_info(user_id, department_id):
    # 'kakao-user' 테이블에 데이터 삽입
    data = {'id': user_id, 'department_id': department_id}
    supabase().table('kakao-user').upsert(data).execute()

# 사용자 모바일 카드 확인
def verify_user_mobile_card(params):
    value = json.loads(params['action']['params']['mobile_card_image_url'])
    
    # 이미지를 2개 이상 보낸 경우
    if value['imageQuantity'] != '1':
        return {'status': "FAIL", 'value': {'error_message': '이미지를 1개만 보내주세요.'}}

    # 이미지 URL을 가져옵니다.
    image_url = value['secureUrls'][5:-1]
    user_id = params['userRequest']['user']['id']

    # DB에 사용자 정보가 있는지 확인합니다.
    user_info = supabase().table('kakao-user').select('id').eq('id', user_id).execute().data
    if user_info:
        return {'status': "FAIL", 'value': {'error_message': '이미 인증된 사용자입니다.'}}
    
    # 이미지 파일 경로를 설정합니다.
    file_name = join(dirname(dirname(dirname(__file__))), 'temp', f'{user_id}.jpg')

    # 이미지를 다운로드합니다.
    try:
        response = requests.get(image_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
    except requests.RequestException as e:
        return {'status': "FAIL"}

    try:
        # 이미지 OCR 기능을 수행하여 학과 정보를 추출합니다.
        img = Image.open(file_name)
        department = img_ocr(img)

        # 학과 정보가 없는 경우
        if department is None:
            return {'status': "FAIL", 'value': {'error_message': '학과 정보를 찾을 수 없습니다. 지속적인 오류 발생 시 1:1 문의를 이용해주세요.'}}

        # 유사도가 기준 미달인 경우
        if capture_similarity(test_image_file_path, file_name) < 0.7 or department is None:
            return {'status': "FAIL", 'value': {'error_message': '올바르지 않은 이미지입니다. 다시 시도해주세요. 지속적인 오류 발생 시 1:1 문의를 이용해주세요.'}}
        
        # 학과 정보 매칭
        department_id = match_department(department)
        if department_id is None:
            return {'status': "FAIL", 'value': {'error_message': '학과 정보를 찾을 수 없습니다. 지속적인 오류 발생 시 1:1 문의를 이용해주세요.'}}
        # 사용자 정보 저장
        save_user_info(user_id, department_id)
        logger.logger.info(f"{user_id} - {department} 인증 완료")
        return {'status': "SUCCESS", 'value': {'department': department}}
    
    except Exception as e:
        print(f"사용자 모바일 카드 이미지 처리 중 오류 발생: {e}")
        return {'status': "FAIL", 'value': {'error_message': '이미지 처리 중 오류가 발생했습니다. 지속적인 오류 발생 시 1:1 문의를 이용해주세요.'}}
    finally:
        os.remove(file_name)

# 학과 정보 매칭
def match_department(department):
    # department가 None인 경우와 매칭할 학과 정보가 없는 경우를 분리합니다.
    if department is None:
        return None

    # 학과 정보 매칭
    for row in supabase_response:
        if row['department_ko'] == department:
            return row['id']

    # 매칭이 실패한 경우 None 반환
    return None