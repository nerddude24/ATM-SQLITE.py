from os import name
from typing import TypedDict


class Account:
    def __init__(self, name: str, password: str, credit: int, index=0) -> None:
        self.name = name
        self.password = password
        self.credit = credit
        self.index = index
