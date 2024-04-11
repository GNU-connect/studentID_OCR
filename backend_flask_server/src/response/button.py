class Button:
    def __init__(self, label, action=['message', 'webLink', 'block'], blockId=None, extra=None, messageText=None, webLinkUrl=None):
        self.label = label
        self.action = action
        self.blockId = blockId
        self.extra = extra
        self.messageText = messageText
        self.webLinkUrl = webLinkUrl

    def to_dict(self):
        button_dict = {
            "label": self.label,
            "action": self.action,
        }
        if self.action == 'block':
          if self.blockId:
              button_dict["blockId"] = self.blockId
        if self.action == 'message':
          if self.messageText:
            button_dict["messageText"] = self.messageText
        if self.action == 'webLink':
          if self.webLinkUrl:
              button_dict["webLinkUrl"] = self.webLinkUrl
        if self.extra:
            button_dict["extra"] = self.extra
        return button_dict