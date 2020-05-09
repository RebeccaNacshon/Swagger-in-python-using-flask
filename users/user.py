import json


class User(object):

    def __init__(self, name=None, password=None, enabled=False, type=None):

        self.name = name
        self.password = password
        self.enabled = enabled
        self.type = type
        self.USER_REQUESTS = {}
        self.type_jsons = {'local': 'jsons/local.json',
                           'snmp': 'jsons/snmp.json',
                           'community': 'jsons/community.json',
                            'user':'jsons/user.json'}

    def get_user_request(self):
        user_request = {
            'name': self.name,
            'password': self.password,
            'type': self.type,
            'enabled': self.enabled
        }
        return user_request

    def get_users(self):
        return self.USER_REQUESTS

    def add_user(self, new_uuid, type):
        try:
            with open(self.type_jsons[type], 'r') as f:
                user_request_dict = json.load(f)
        except ValueError:
            user_request_dict = {}
        with open(self.type_jsons[type], 'w') as f:
            user_request_dict[new_uuid] = self.get_user_request()
            json.dump(user_request_dict, f)

        with open(self.type_jsons['user'], 'r') as f:
            self.USER_REQUESTS = json.load(f)

        with open(self.type_jsons['user'], 'w') as f:
            self.USER_REQUESTS[new_uuid] = self.get_user_request()
            json.dump(self.USER_REQUESTS, f)
