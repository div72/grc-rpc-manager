from pathlib import Path

from aiohttp import web, BasicAuth, ClientSession

from src.config import load_config


class Server:
    app = web.Application()

    async def handler(self, request):
        auth = BasicAuth.decode(request.headers.get('Authorization'))
        if auth is not None:
            try:
                user = self.users[auth.login]
            except KeyError:
                return web.Response(status=403)
            json = await request.json()
            if user.check_password(auth.password) and user.can_call(json['method']):
                async with self.session.post(self.wallet_url, json=json) as wallet_resp:
                    return web.Response(status=wallet_resp.status,
                                        body=await wallet_resp.text())
            else:
                return web.Response(status=403)
        else:
            return web.Response(status=401)

    async def close(self, app=None):
        await self.session.close()

    def __init__(self, port: int, wallet_config: dict):
        self.port = port
        self.wallet_url = wallet_config['url']

        self.app.add_routes([web.post('/', self.handler)])
        self.app.on_shutdown.append(self.close)

        self.session = ClientSession(auth=BasicAuth(wallet_config['username'], wallet_config['password']))
        self.users = {}

    @classmethod
    def from_config(cls, path: Path) -> 'Server':
        server_config, wallet_config, users = load_config(path)
        cls_ = cls(server_config.getint('port'),
                   wallet_config)

        cls_.users.update(users)

        return cls_

    def run(self):
        web.run_app(self.app, port=self.port)
