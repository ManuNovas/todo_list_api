class Token:
    bearer_token: str
    expires_in: int
    refresh_token: str

    def __init__(self, bearer_token: str, expires_in: int, refresh_token: str):
        self.bearer_token = bearer_token
        self.expires_in = expires_in
        self.refresh_token = refresh_token
