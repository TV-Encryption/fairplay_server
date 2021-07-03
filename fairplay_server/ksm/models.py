from uuid import UUID


class KeyRequestBody:
    def __init__(self, key_ref: UUID, spc: str):
        self.key_ref: UUID = key_ref
        self.spc: str = spc


class KeyResponseBody:
    def __init__(self, ckc: str):
        self.ckc: str = ckc
