class UserSession:
    current_user = None

    def __init__(self):
        pass

    def connect(self, user):
        UserSession.current_user = user
