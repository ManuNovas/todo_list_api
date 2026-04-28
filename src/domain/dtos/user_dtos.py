class CreateDto:
    name: str
    email: str
    password: str

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password

class TokenDto:
    bearer_token: str

    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token
