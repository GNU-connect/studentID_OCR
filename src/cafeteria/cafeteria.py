from src.utils.supabase import supabase
from src.common.user import get_user_campus_info

def get_cafeteria_quick_replies(user_id):
    cafeteria_list = []
    cafeteria_names = []

    campus_info = get_user_campus_info(user_id)
    if campus_info is None:
        cafeteria_list = supabase().table('cafeteria').select('cafeteria_name_ko, campus(campus_name_ko)').execute().data
        cafeteria_names = [cafeteria['campus']['campus_name_ko'] + ' ' + cafeteria['cafeteria_name_ko'] for cafeteria in cafeteria_list]
    else:
        cafeteria_list = supabase().table('cafeteria').select('cafeteria_name_ko').eq('campus_id', campus_info['campus_id']).execute().data
        cafeteria_names = [cafeteria['cafeteria_name_ko'] for cafeteria in cafeteria_list]
    quick_replies = [{'label': cafeteria_name, 'action': 'message', 'messageText': cafeteria_name} for cafeteria_name in cafeteria_names]
    return quick_replies