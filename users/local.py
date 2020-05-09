from user import User
import json


class Local(User):

    def __init__(self, name=None, password=None, type='local', enabled=False):
        super(Local, self).__init__(name=name, password=password, enabled=enabled, type=type)
        self.USER_REQUESTS_LOCAL = {}

    def get_local_users(self):
        with open('jsons/local.json', 'r') as f:
            self.USER_REQUESTS_LOCAL = json.load(f)
            return self.USER_REQUESTS_LOCAL

    def get_user_request(self):
        user_request = {
            'name': self.name,
            'password': self.password,
            'type': self.type,
            'enabled': self.enabled
        }
        return user_request

