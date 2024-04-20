from dotenv import load_dotenv
import gdown
from os.path import join, dirname
from torchvision import models
import os
from src.utils.supabase import supabase

# .env 파일을 불러오기 위한 설정
dotenv_path = join(dirname(dirname(dirname(__file__))), '.env')
load_dotenv(dotenv_path)

# 학과 정보 불러오기
supabase_response = supabase().table('department').select("id", "department_ko").execute().data
departments = [row['department_ko'].replace(' ', '') for row in supabase_response]

# 사전 훈련된 ResNet18 모델 로드
model = models.resnet18(pretrained=True)
model.eval()

# test 이미지 저장 경로 설정
drive_file_url = os.environ['CARD_VARIFICATION_IMAGE_URL']
test_image_file_path = join(dirname(dirname(dirname(__file__))), 'temp', 'test.jpg')
os.makedirs(os.path.dirname(test_image_file_path), exist_ok=True)
gdown.download(drive_file_url, test_image_file_path, quiet=False)