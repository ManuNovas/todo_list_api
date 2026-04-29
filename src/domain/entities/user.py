USER_SK = "USER"

class User:
    pk: str
    sk: str
    name: str
    email: str
    password: str
    created_at: str
    updated_at: str | None

    def __init__(self, pk: str, name: str, email: str, password: str, created_at: str, updated_at: str | None):
        self.pk = pk
        self.sk = USER_SK
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
