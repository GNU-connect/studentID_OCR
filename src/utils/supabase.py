import os
from os.path import join, dirname

# 젠킨스 환경에서 실행 중인지 여부 확인
IN_JENKINS = 'JENKINS_HOME' in os.environ

# 젠킨스 환경에서는 .env 파일을 무시하고 그렇지 않은 경우에만 로드
if not IN_JENKINS:
    from dotenv import load_dotenv

    # 프로젝트 루트에 있는 .env 파일 경로 설정
    dotenv_path = join(dirname(dirname(dirname(__file__))), '.env')

    # .env 파일 로드
    load_dotenv(dotenv_path, verbose=True)

from supabase import create_client, Client

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