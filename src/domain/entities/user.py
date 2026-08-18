USER_PK = "USER"
USER_EMAIL_INDEX = "users_email_gsi"


class User:
    pk: str
    sk: str
    name: str
    email: str
    password: str
    created_at: str
    updated_at: str | None

    def __init__(self, sk: str, name: str, email: str, password: str, created_at: str, updated_at: str | None):
        self.pk = USER_PK
        self.sk = sk
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
