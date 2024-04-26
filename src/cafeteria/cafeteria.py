from src.utils.supabase import supabase
from src.common.user import get_user_campus_info
from src.response.list_card import ListCard, ListItem
from src.response.button import Button
import logging
import logging.config
logger = logging.getLogger("cafeteria")

def get_cafeteria_info(user_id, campus_id=None):
    cafeteria_list = []
    items = []
    buttons = []
    block_id = '66067167cdd882158c759fc2'
    response = None

    user_campus_info = get_user_campus_info(user_id)

    # 유저 아이디로 캠퍼스 정보 조회 시 캠퍼스 정보가 없는 경우 혹은 더 보기를 눌렀을 때 (캠퍼스 선택)
    if campus_id == 0 or (not user_campus_info and not campus_id):
        query = supabase().table('campus') \
                .select('id, campus_name_ko, thumbnail_url') \
                .limit(4) \
                .order('id')
        campus_data = query.execute().data
        campus_list = [(campus['id'], campus['campus_name_ko'], campus['thumbnail_url']) for campus in campus_data]

        for campus_info in campus_list:
            campus_id, campus_name_ko, thumbnail_url = campus_info
            items.append(ListItem(campus_name_ko, thumbnail_url, 
                                action="block", 
                                blockId=block_id,
                                extra={"sys_campus_id": campus_id}
                                ))
        response = ListCard("어떤 캠퍼스 식당 정보가 궁금하세요?", items, buttons)
    # 캠퍼스 정보가 있는 경우
    else:
        campus_id = campus_id if campus_id else user_campus_info['campus_id']
        query = supabase().table('cafeteria') \
                .select('cafeteria_name_ko, thumbnail_url, campus(campus_name_ko)') \
                .eq("campus_id", campus_id) \
                .order('cafeteria_name_ko')
        cafeteria_data = query.execute().data

        cafeteria_list = [(cafeteria['campus']['campus_name_ko'], cafeteria['cafeteria_name_ko'], cafeteria['thumbnail_url']) for cafeteria in cafeteria_data]
        
        for cafeteria_info in cafeteria_list:
            campus_name_ko, cafeteria_name_ko, thumbnail_url = cafeteria_info
            items.append(ListItem(title=cafeteria_name_ko, description=campus_name_ko, imageUrl=thumbnail_url, 
                                action="message", 
                                messageText=f"{campus_name_ko} {cafeteria_name_ko}"))
            
        buttons.append(Button(label="더 보기", action="block", blockId=block_id, extra={"sys_campus_id": 0}))
        response = ListCard("어떤 교내 식당 정보가 궁금하세요?", items, buttons)
    logger.info(f"유저 id: {user_id} - {campus_id}번 교내 식당 정보 조회 완료")
    return response.to_dict()