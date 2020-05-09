from user import User


class Community(User):

    def __init__(self, name=None, type=None, enabled=False):
        super(Community, self).__init__(name=name, enabled=enabled, type=type)
        self.USER_REQUESTS_COMMUNITY = {}

    def get_user_request(self):
        user_request = {
            'name': self.name,
            'type': self.type,
            'enabled': self.enabled
        }
        return user_request


