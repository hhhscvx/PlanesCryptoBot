import asyncio
from random import randint
from time import time
from urllib.parse import unquote

from aiohttp import ClientSession
import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView
from pyrogram.errors import FloodWait

from bot.utils import logger, Profile
from bot.config import InvalidSession
from .headers import headers
from bot.config import settings


class Tapper:
    def __init__(self, tg_client: Client) -> None:
        self.session_name = tg_client.name
        self.tg_client = tg_client

    async def get_tg_web_data(self, proxy: str | None) -> str:
        if proxy:
            proxy: Proxy = Proxy.from_str(proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            with_tg = True

            if not self.tg_client.is_connected:
                with_tg = False
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('planesCryptobot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"{self.session_name} | FloodWait {fl}")
                    logger.info(f"{self.session_name} | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=peer,
                bot=peer,
                platform='android',
                from_bot_menu=False,
                url='https://planescrypto.com/'
            ))

            auth_url = web_view.url
            query = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            if with_tg is False:
                await self.tg_client.disconnect()

            return query

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=3)

    async def login(self, http_client: ClientSession, tg_web_data: str) -> dict:
        """access_token, is_first_auth, start_bonus"""
        try:
            response = await http_client.post('https://backend.planescrypto.com/auth',
                                              json={'init_data': tg_web_data})
            response.raise_for_status()

            return await response.json()
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while Login: {error}")
            await asyncio.sleep(delay=3)

    async def get_profile(self, http_client: ClientSession) -> Profile:
        try:
            response = await http_client.get(url='https://backend.planescrypto.com/user/profile')
            response.raise_for_status()

            resp_json = await response.json()
            profile = Profile.model_validate(resp_json)

            return profile
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error when Get Profile: {error}")
            await asyncio.sleep(delay=3)

    async def check_proxy(self, http_client: aiohttp.ClientSession, proxy: Proxy) -> None:
        try:
            response = await http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def run(self, proxy: str | None) -> None:
        access_token_expires_at = 0

        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
            if proxy:
                await self.check_proxy(http_client=http_client, proxy=proxy)

            while True:
                try:
                    if access_token_expires_at == 0 or time() > access_token_expires_at:
                        tg_web_data = await self.get_tg_web_data(proxy=proxy)
                        login = await self.login(http_client=http_client, tg_web_data=tg_web_data)

                        access_token = login['access_token']
                        http_client.headers["Authorization"] = f'Bearer {access_token}'
                        headers["Authorization"] = f'Bearer {access_token}'
                        access_token_expires_at = time() + 3600

                    profile = await self.get_profile(http_client)

                    logger.success(f"{self.session_name} | Login! | Balance: {profile.balance}")
                    await asyncio.sleep(20)

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    logger.error(f"{self.session_name} | Unknown error: {error}")
                    await asyncio.sleep(delay=3)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client).run(proxy=proxy)
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
