from mangas_origines.exceptions.exceptions import LoginError
from bs4 import BeautifulSoup
import aiofiles
import aiohttp
import json
import os


class Auth:
    """
    A class to create an Auth object

    ...

    Attributes
    ----------
    headers: dict
        use of personalized headers for requests
    export_cookies_to: str
        the path for JSON who contains the cookies
    cookies: dict
        the dict who contains the cookies

    Methods
    -------
    __save_cookies(session: aiohttp.ClientSession)
        Save cookies dict to JSON file
    __import_cookies_from_file() -> dict
        Import cookies from JSON file
    login(username: str, password: str) -> bool
        Login on mangas-origines.fr
    """
    def __init__(self, headers: dict = None, export_cookies_to: str = None):
        self.headers = headers
        self.export_cookies_to = export_cookies_to

        self.cookies = {}

        if self.headers is None:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

    async def __save_cookies(self, session: aiohttp.ClientSession):
        """Save cookies dict to JSON file

        Parameters
        ----------
        session: aiohttp.ClientSession
            The aiohttp session object
        """
        if self.export_cookies_to is not None:
            cookies_to_save = {}
            for key, cookie in session.cookie_jar.filter_cookies('https://mangas-origines.fr/').items():
                cookies_to_save[key] = cookie.value

            self.cookies = cookies_to_save

            async with aiofiles.open(self.export_cookies_to, 'wb') as f:
                await f.write(json.dumps(cookies_to_save, ensure_ascii=False).encode('utf-8'))

    async def __import_cookies_from_file(self) -> dict:
        """Import cookies from JSON file

        Returns
        -------
        dict
            a dict who contains cookies
        """
        if self.export_cookies_to is not None and os.path.exists('/mnt/hdd/Downloads/cookies.json'):
            async with aiofiles.open('/mnt/hdd/Downloads/cookies.json', 'r', encoding='utf-8') as f:
                file_content = await f.read()
                self.cookies = json.loads(file_content)
                return self.cookies

    async def login(self, username: str, password: str) -> bool:
        """Login on mangas-origines.fr

        Parameters
        ----------
        username: str
            The username of email of user
        password: str
            The password of user

        Returns
        -------
        bool
            return True on success, False otherwise

        Raises
        ------
        LoginError
            If the credentials are wrong.
        """
        await self.__import_cookies_from_file()
        if self.cookies:
            return True

        async with aiohttp.ClientSession(headers=self.headers, cookie_jar=aiohttp.CookieJar()) as client_session:
            async with client_session.get('https://mangas-origines.fr/') as r:
                bs = BeautifulSoup(await r.text(), 'html.parser')
            get_script = json.loads(bs.find(
                'script', attrs={'id': 'wp-manga-login-ajax-js-extra'}).string.replace(
                '/* <![CDATA[ */\nvar wpMangaLogin = ', ''
            ).replace(';\n/* ]]> */', '').strip())

            data = aiohttp.FormData()
            data.add_field('action', 'wp_manga_signin')
            data.add_field('login', username)
            data.add_field('pass', password)
            data.add_field('rememberme', 'forever')
            data.add_field('nonce', get_script['nonce'])

            async with client_session.post(
                    'https://mangas-origines.fr/wp-admin/admin-ajax.php', data=data
            ) as r:
                content = await r.json()
                if 'success' in content and content['success'] is True:
                    await self.__save_cookies(client_session)
                    return True
                else:
                    raise LoginError(content['data'] if 'data' in content else 'Your credentials are probably wrong.')
