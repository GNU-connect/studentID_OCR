class ListCard:
    def __init__(self, title, items, buttons, is_carousel=False):
        self.title = title
        self.items = items
        self.buttons = buttons
        self.is_carousel = is_carousel

    def to_dict(self):
        card_dict = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "listCard": {
                            "header": {
                                "title": self.title
                            },
                            "items": [item.to_dict() for item in self.items]
                        }
                    }
                ]
            }
        }
        
        # buttons가 있는 경우에만 buttons를 추가
        if self.buttons:
            card_dict['template']['outputs'][0]['listCard']['buttons'] = [button.to_dict() for button in self.buttons]
        
        # is_carousel이 True인 경우에만 carousel을 추가
        if self.is_carousel:
            card_dict['template']['outputs'][0]['listCard']['type'] = 'carousel'
        
        return card_dict

class ListItem:
    def __init__(self, title, imageUrl=None, link=None, action=None, blockId=None, messageText=None, extra=None, description=None):
        self.title = title
        self.description = description
        self.imageUrl = imageUrl
        self.link = link
        self.action = action
        self.blockId = blockId
        self.messageText = messageText
        self.extra = extra

    def to_dict(self):
        item_dict = {
            "title": self.title,
        }
        if self.imageUrl:
            item_dict["imageUrl"] = self.imageUrl
        if self.description:
            item_dict["description"] = self.description
        if self.link:
            item_dict["link"] = self.link
        if self.action:
            item_dict["action"] = self.action
        if self.blockId:
            item_dict["blockId"] = self.blockId
        if self.messageText:
            item_dict["messageText"] = self.messageText
        if self.extra:
            item_dict["extra"] = self.extra
        return item_dict