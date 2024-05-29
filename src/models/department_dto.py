from src.common.utils.supabase import supabase

# departmentId로 department 이름 조회
def get_department_name_by_id(department_id):
    response = supabase().table('department') \
    .select('department_ko') \
    .eq('id', department_id).execute().data
    if len(response) == 0:
        return None
    return response[0]['department_ko']