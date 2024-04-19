class Thumbnail:
    def __init__(self, imageUrl):
        self.imageUrl = imageUrl

    def to_dict(self):
        return {
            "imageUrl": self.imageUrl
        }

class Card:
    def __init__(self, title, thumbnail, buttons=None, description=None):
        self.title = title
        self.thumbnail = thumbnail
        self.buttons = buttons
        self.description = description
    
    def result_json(self):
        result = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "basicCard": {
                            "title": self.title,
                            "thumbnail": self.thumbnail.to_dict()
                        }
                    }
                ]
            }
        }
        
        # buttons가 있는 경우에만 buttons를 추가
        if self.buttons:
            result['template']['outputs'][0]['basicCard']['buttons'] = [button.to_dict() for button in self.buttons]
        
        if self.description:
            result['template']['outputs'][0]['basicCard']['description'] = self.description
        
        return result