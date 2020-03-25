from pathlib import Path

from src.server import Server


def main():
    serv = Server.from_config(Path('rpc.ini'))
    serv.run()
