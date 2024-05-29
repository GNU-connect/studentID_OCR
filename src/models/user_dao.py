from src.common.utils.supabase import supabase

# 사용자 정보 조회
def get_user_info(user_id):
    return supabase().table('kakao-user').select('id', 'department_id').eq('id', user_id).execute().data

# 데이터베이스에 사용자 정보 저장
def save_user_info(user_id, department_id):
    # 'kakao-user' 테이블에 데이터 삽입
    data = {'id': user_id, 'department_id': department_id}
    supabase().table('kakao-user').upsert(data).execute()
