import os
from os.path import join, dirname
from supabase import create_client, Client
from dotenv import load_dotenv

# 프로젝트 루트에 있는 .env 파일 경로 설정
dotenv_path = join(dirname(dirname(dirname(__file__))), '.env')

# .env 파일 로드
load_dotenv(dotenv_path, verbose=True)

def supabase():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase

def supabase():
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase