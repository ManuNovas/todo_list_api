TOKEN_ALGORITHM = "HS256"

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

class LoginDto:
    email: str
    password: str

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class BearerTokenDto:
    token: str

    def __init__(self, token: str):
        self.token = token
