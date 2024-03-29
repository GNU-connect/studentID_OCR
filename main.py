from flask import Flask
from flask import request
import requests
import pytesseract
from PIL import Image
import os
from supabase import create_client, Client
import torch
from numpy import dot
from numpy.linalg import norm
from torchvision.models import efficientnet_b0
from torchvision.models.feature_extraction import create_feature_extractor
import torchvision.transforms as T
from dotenv import load_dotenv

load_dotenv(verbose=True) # .env 파일로부터 환경변수 로드

#url,key값 입력
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(url, key)
supabaseResponse = supabase.table('department').select("id","department_ko").execute().data
department=[]
for i in supabaseResponse:
    department.append(i['department_ko'])

app = Flask(__name__)


def img_ocr(img,filename='test'):
    custom_configs=[r'--oem 1 --psm 4',r'--oem 3 --psm 6',r'--oem 1 --psm 3']
    founded=False
    for i in range(len(custom_configs)):
        texts = pytesseract.image_to_string(img, lang='kor', config=custom_configs[i])
        founded_dept=''
        text_parts=texts.split()
        for part in text_parts:
            if part in department:
                founded_dept=part
                founded=True
        if founded:
            break
    if founded:
        print(f'학과:{founded_dept} , 파일명:{filename}')
        return founded_dept
    else:
        print(f'학과 발견 불가 , 파일명:{filename}')
        return False

# EfficientNet 모델 불러오기
model = efficientnet_b0(weights=None)
model = create_feature_extractor(model, return_nodes={'avgpool': 'avgpool'})
model.eval()

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
    data = {'kakao_id': user_id, 'department_id': department}
    response,count = supabase.table('user').upsert(data).execute()

# 서버 테스트 코드
@app.route('/cafeteria-diet', methods=['POST'])
def get_cafeteria_diet():
    data = request.json
    diet_content = '''
[A코스/한식]
쌀밥,어묵국,적어무조림,마늘쫑햄볶음,세발나무무침,배추김치,오렌지주스

[B코스/일품]
바지락칼국수,양파링튀김,단무지,배추김치,오렌지주스
    '''

    print(data)
    # 기본 값은 '가좌캠퍼스'
    campus = data['action']['detailParams'].get('sys_campus')
    if campus is not None:
        campus = campus.get('value')
    diet_date = data['action']['detailParams'].get('sys_date')
    if diet_date is not None:
        diet_date = diet_date.get('origin')
    diet_time = data['action']['detailParams'].get('sys_time')
    if diet_time is not None:
        diet_time = diet_time.get('value')

    return {
        "answer": {
                "status": "normal",
                "cafeteria_name": data['action']['params']['sys_cafeteria_name'],
                "campus": campus if campus is not None else '가좌캠퍼스',
                "diet_content": diet_content,
                "diet_date": diet_date if diet_date is not None else '2023-03-29',
                "diet_time": diet_time if diet_time is not None else '점심',
                "image_url": "https://cf-ea.everytime.kr/attach/133/66414961/everytime-1711679608338.jpg?Expires=1711692207&Key-Pair-Id=APKAICU6XZKH23IGASFA&Signature=atL-wCR605e5SeGAcpVn1ksFUfRi2uty0snZf~psTpJN7~7a~OQFuXBRLVlFV-0vAqEF3mSeVUkQXq27r2fV~NxxZkUub8XmK6lnnY74DkgxALygMBZ6Fop4WFyjvpt2Tu8YvMmES4TC6Uvvsj4Zi1XvHb1lE5VefGxnv4fvytZ93cAOgvutK5yZlwrHu92DYXRjprNGzdD9frHA89eGAXz6ciVM1dat2wJF87EPj~NgTVdBike-~l7lDph1AlfqBfrquktJpYUEYNPY26swBPXMg61NwhTjQ1ktosiOBUMrKefMsnki8mINHmWteXpA8hYUH3wHpgKIymedysqvPA__"
        }
    }
    
@app.route('/test', methods=['POST'])
def test():
    params = request.json
    #print(params)
    #print(params['value']['origin'])
    image_url=params['value']['origin'][5:-1]
    userID=params['user']['id']
    userID = int(userID, 16)
    response = requests.get(image_url)
    if response.status_code == 200:
        with open('temp/downloaded_image.jpg', 'wb') as f:
            f.write(response.content)
    else:
        pass
    img = Image.open('temp/downloaded_image.jpg')
    dept=img_ocr(img)
    deptID = None
    for row in supabaseResponse:
        if row['department_ko'] == dept:
            deptID = row['id']
            break
    
    similarity=capture_probability('test.jpg','temp/downloaded_image.jpg')
    if dept!=False and similarity>0.84:
        save_user_info(userID,deptID)
    return 'True'


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


