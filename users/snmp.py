from user import User


class Snmp(User):

    def __init__(self, name=None, password_a=None, password_b=None, type='snmp', enabled=False):
        super(Snmp, self).__init__(name, password_a, enabled, type)
        self.password_b = password_b
        self.USER_REQUESTS_SNMP = {}

    def get_user_request(self):
        user_request = {
            'name': self.name,
            'password_a': self.password,
            'password_b': self.password_b,
            'type': self.type,
            'enabled': self.enabled
        }
        return user_request
