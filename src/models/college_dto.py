from src.common.utils.supabase import supabase

# departmentId로 단과대학 정보 조회
def get_college_info_by_department_id(department_id):
    response = supabase().table('department') \
    .select('college_id, college(college_ko, thumbnail_url)') \
    .eq('id', department_id).execute().data
    if len(response) == 0:
        return None
    return {
        'name_ko': response[0]['college']['college_ko'],
        'thumbnail_url': response[0]['college']['thumbnail_url']
    }