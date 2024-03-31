class Thumbnail:
    def __init__(self, imageUrl):
        self.imageUrl = imageUrl

    def to_dict(self):
        return {
            "imageUrl": self.imageUrl
        }

class Card:
    def __init__(self, title, thumbnail, buttons, description=None):
        self.title = title
        self.thumbnail = thumbnail
        self.buttons = buttons
        self.description = description

    def to_dict(self):
        item_dict = {
            "title": self.title,
            "thumbnail": self.thumbnail.to_dict(),
            "buttons": [button.to_dict() for button in self.buttons]
        }
        if self.description:
            item_dict["description"] = self.description
        return item_dict

class Carousel:
    def __init__(self, items):
        self.items = items

    def to_dict(self):
        return {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": [item.to_dict() for item in self.items]
                        }
                    }
                ]
            }
        }