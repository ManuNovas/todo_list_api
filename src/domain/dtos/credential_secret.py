class CredentialSecret:
    bearer_secret: str
    refresh_secret: str

    def __init__(self, bearer_secret: str, refresh_secret: str):
        self.bearer_secret = bearer_secret
        self.refresh_secret = refresh_secret
