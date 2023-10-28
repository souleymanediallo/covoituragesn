from flask_login import UserMixin, current_user


class User(UserMixin):
    def __init__(self, uid):
        self.id = uid