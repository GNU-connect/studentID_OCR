from src.response.list_card import ListCard, ListItem
from src.response.button import Button
from src.common.user import get_user_department_info
from src.utils.supabase import supabase

def _group_notice_by_category(notice_list):
    # 빈 딕셔너리를 생성합니다.
    categories = {}

    # 각 항목을 category_id를 기준으로 딕셔너리에 추가합니다.
    for notice in notice_list:
        category_id = notice['category_id']
        if category_id not in categories:
            categories[category_id] = []
        categories[category_id].append(notice)

    return categories

def _get_category_name_by_category_id(college_en, category_id):
    return supabase().table(f'{college_en}-category').select('category').eq('id', category_id).execute().data[0]['category']

def get_existing_notice(college_en, department_id):
    return supabase().table(f'{college_en}-notice').select('*').eq("department_id", department_id).execute().data

def get_notice(user_id):
    department_data = get_user_department_info(user_id)
    department_id, college_en = department_data['department_id'], department_data['department']['college']['college_en']
    notice_list = get_existing_notice(college_en, department_id)
    notice_list = _group_notice_by_category(notice_list)

    items = []
    categories = []
    buttons = []
    
    for category_id, notices in notice_list.items():
        category_name = _get_category_name_by_category_id(college_en, category_id)
        for notice in notices:
            categories.append(ListItem(title=notice['title'], description=notice['created_at'], imageUrl=notice['thumbnail_url']))
        buttons.append(Button(label="더 보기", action="message", messageText="Test"))
        items.append(ListCard(category_name, categories, buttons))
    
    response = {
      "version": "2.0",
      "template": {
        "outputs": [
          {
            "carousel": {
              "type": "listCard",
              "items": [
                {
                  "header": {
                    "title": "공지사항1"
                  },
                  "items": [
                    {
                      "title": "경남 건축사회 회장 당선(87학번 정일현 동문)",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "2024년 삼성중공업 상반기 대졸 신입 공채 채용상담회 안내(~3/11, 신청)",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "「2024학년도 GNU창의·융합동아리」모집 안내 (협조)",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "「2024학년도 GNU창의·융합동아리」모집 안내(~4/28)",
                      "description": "2024-04-01",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "[장학] ’24학년도 1학기 등록금재원 사회적배려장학금 신청 안내(~3/31)",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    }
                  ],
                  "buttons": [
                    {
                      "label": "더 보기",
                      "action": "message",
                      "messageText": "Test"
                    }
                  ]
                },
                {
                  "header": {
                    "title": "공지사항2"
                  },
                  "items": [
                    {
                      "title": "채용공고1",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "채용공고2",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    }
                  ],
                  "buttons": [
                    {
                      "label": "더 보기",
                      "action": "message",
                      "messageText": "Test"
                    }
                  ]
                },
                {
                  "header": {
                    "title": "공지사항3"
                  },
                  "items": [
                    {
                      "title": "채용공고1",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "채용공고2",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    }
                  ],
                  "buttons": [
                    {
                      "label": "더 보기",
                      "action": "message",
                      "messageText": "Test"
                    }
                  ]
                },
                {
                  "header": {
                    "title": "공지사항4"
                  },
                  "items": [
                    {
                      "title": "채용공고1",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "채용공고2",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    }
                  ],
                  "buttons": [
                    {
                      "label": "더 보기",
                      "action": "message",
                      "messageText": "Test"
                    }
                  ]
                },
                {
                  "header": {
                    "title": "공지사항5"
                  },
                  "items": [
                    {
                      "title": "채용공고1",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    },
                    {
                      "title": "채용공고2",
                      "description": "2024-04-01",
                      "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/img_001.jpg",
                      "link": {
                        "web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
                      }
                    }
                  ],
                  "buttons": [
                    {
                      "label": "더 보기",
                      "action": "message",
                      "messageText": "Test"
                    }
                  ]
                }
              ]
            }
          }
        ]
      }
    }



    return response
            
    

