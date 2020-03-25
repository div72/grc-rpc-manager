import hashlib
from hmac import compare_digest


class User:
    def __init__(self, name: str, password: str, password_hash: str, allowed_commands: set):
        self.name = name
        self.password = password
        self.hash_function = getattr(hashlib, password_hash)
        self.allowed_commands = allowed_commands

    @classmethod
    def from_section(cls, section):
        cls_ = cls(name=section.name.split(':')[1],
                   password=section['password'],
                   password_hash=section['password_hash'],
                   allowed_commands=set(section['allowed_commands'].split(';')))
        return cls_

    def can_call(self, method: str):
        return method in self.allowed_commands

    def check_password(self, password: str):
        return compare_digest(self.password, self.hash_function(password.encode()).hexdigest())
