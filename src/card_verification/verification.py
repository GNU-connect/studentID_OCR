from src.utils.supabase import supabase
import torchvision.transforms as T
import pytesseract
import torch
from numpy import dot
from numpy.linalg import norm
import requests
from PIL import Image, UnidentifiedImageError
from torchvision.models import efficientnet_b0
from torchvision.models.feature_extraction import create_feature_extractor
import os
import json
import re
import urllib.request
from dotenv import load_dotenv
from os.path import join, dirname

# .env 파일을 불러오기 위한 설정
dotenv_path = join(dirname(dirname(dirname(__file__))), '.env')
load_dotenv(dotenv_path)

# 학과 정보 불러오기
supabaseResponse = supabase().table('department').select("id","department_ko").execute().data
departments=[]
for i in supabaseResponse:
    department_ko = i['department_ko'].replace(' ', '')
    departments.append(department_ko)

# EfficientNet 모델 불러오기
model = efficientnet_b0(weights=None)
model = create_feature_extractor(model, return_nodes={'avgpool': 'avgpool'})
model.eval()

# test 이미지 저장
drive_file_url = os.environ['CARD_VARIFICATION_IMAGE_URL']
test_image_file_path = join(dirname(dirname(dirname(__file__))), 'temp', 'test.jpg')
temp_dir = os.path.dirname(test_image_file_path)
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
if not os.path.exists(test_image_file_path):
    urllib.request.urlretrieve(drive_file_url, test_image_file_path)
    print("test.jpg 파일을 다운로드 받았습니다.")

def img_ocr(img):
    custom_configs=[r'--oem 1 --psm 4',r'--oem 3 --psm 6',r'--oem 1 --psm 3']
    for i in range(len(custom_configs)):
        texts = pytesseract.image_to_string(img, lang='kor', config=custom_configs[i])
        text_list = texts.split('\n')
        
        for text in text_list:
            text = re.sub(r'\s+', '', text)
            if text in departments:
                founded_dept=text
                return founded_dept
    return False

# 이미지 로드 및 전처리 함수
def image_preprocess(image_path):
    image = Image.open(image_path).convert("RGB")
    preprocess = T.Compose([
        T.Resize(256, interpolation=T.InterpolationMode.BICUBIC),
        T.CenterCrop(224),
        T.ToTensor()
    ])
    return preprocess(image).unsqueeze(0)

# 코사인 유사도 계산 함수
def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))

def capture_probability(original_image_path, test_image_path):
    # 원본 이미지와 테스트 이미지의 특성 벡터 추출
    original_embedding = torch.flatten(model(image_preprocess(original_image_path))['avgpool']).detach().numpy()
    test_embedding = torch.flatten(model(image_preprocess(test_image_path))['avgpool']).detach().numpy()
    
    # 코사인 유사도 계산
    similarity = cos_sim(original_embedding, test_embedding)
    
    return similarity

# 데이터베이스에 사용자 정보 저장
def save_user_info(user_id, department):
    # 'users' 테이블에 데이터 삽입
    data = {'id': user_id, 'department_id': department}
    response,count = supabase().table('kakao-user').upsert(data).execute()

def verify_user_mobile_card(params):
    resolved_params = json.loads(params['value']['resolved'])

    # 이미지를 2개 이상 보낸 경우
    if resolved_params['imageQuantity'] != '1':
        return {'status': "FAIL"}

    # 이미지 URL을 가져옵니다.
    image_url = params['value']['origin'][5:-1]
    userID = params['user']['id']
    
    # 이미지 파일 경로를 설정합니다.
    file_name = join(dirname(dirname(dirname(__file__))), 'temp', f'{userID}.jpg')

    # 이미지를 다운로드합니다.
    try:
        response = requests.get(image_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)
    except requests.RequestException:
        print("사용자 모바일 카드 이미지 다운로드에 실패했습니다.")
        return {'status': "FAIL"}

    try:
        img = Image.open(file_name)
        # OCR 기능을 수행하여 학과 정보를 추출합니다.
        dept = img_ocr(img)
        deptID = None
        # 학과 정보를 찾습니다.
        for row in supabaseResponse:
            if row['department_ko'] == dept:
                deptID = row['id']
                break
        print(f"사용자 학과 정보: {dept}")
        print(file_name, test_image_file_path)
        # 학과 정보가 없는 경우 실패로 처리합니다.
        if deptID is None:
            return {'status': "FAIL"}
        # 유사도가 0.84 이하인 경우 실패로 처리합니다.
        if capture_probability(test_image_file_path, file_name) <= 0.84:
            return {'status': "FAIL"}
        save_user_info(userID, deptID) # 사용자 정보 저장
        result = {
            'status': "SUCCESS",
            'value': {
                'name': '홍길동',  # '홍길동'은 임의의 이름입니다.
                'department': dept,
            }
        }
        return result
    except Exception as e:
        print(f"사용자 모바일 카드 이미지 처리 중 오류가 발생했습니다. {e}")
        return {'status': "FAIL"}
    finally:
        os.remove(file_name)