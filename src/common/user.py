from src.utils.supabase import supabase

# 사용자 학과 정보로 캠퍼스 정보 조회
def get_user_campus_info(user_id):
    response = supabase().table('kakao-user') \
    .select('department_id, department(college_id, college(campus_id, campus(campus_name_ko)))') \
    .eq('kakao_id', user_id).execute().data
    if len(response) == 0:
        return None
    return {
        'campus_id': response[0]['department']['college']['campus_id'],
        'campus_name_ko': response[0]['department']['college']['campus']['campus_name_ko']
    }

# 사용자 아이디로 학과 정보 조회
def get_user_department_info(user_id):
    response = supabase().table('kakao-user') \
    .select('department_id, department(department_ko, college(college_en)))').execute().data
    return response[0]