import configparser
from pathlib import Path

from src.user import User


def load_config(path: Path) -> tuple:
    parser = configparser.ConfigParser()
    parser.read(path)

    server_conf = parser['Server']

    wallet_conf = parser['Wallet']

    users = {}
    for section in parser.sections():
        type_ = section.split(':')[0]
        if type_ == 'User':
            section = parser[section]
            users[section.name.split(':')[1]] = User.from_section(section)

    return server_conf, wallet_conf, users
