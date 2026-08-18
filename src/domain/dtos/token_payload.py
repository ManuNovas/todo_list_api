class TokenPayload:
    sk: str
    exp: int

    def __init__(self, sk: str, exp: int):
        self.sk = sk
        self.exp = exp
