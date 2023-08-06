from mangas_origines.objects.scan import Scan
import aiohttp


class Favorite:
    """
    A class to create an Favorite object

    ...

    Attributes
    ----------
    __mangas_origines: MangasOrigines
        MangasOrigines object
    __scan: Scan
        Scan object

    Methods
    -------
    get_scan() -> Scan
        Get Scan object of current favorite
    remove_favorite() -> bool
        Remove the current favorite
    """
    def __init__(self, mangas_origines, scan):
        self.__mangas_origines = mangas_origines
        self.__scan = scan

    def get_scan(self) -> Scan:
        """Return the Scan object of current favorite"""
        return self.__scan

    async def remove_favorite(self) -> bool:
        """Remove the current favorite

        Returns
        -------
        bool
            return True on success, False otherwise
        """
        data = aiohttp.FormData()
        data.add_field('action', 'wp-manga-delete-bookmark')
        data.add_field('postID', self.__scan.scan_id)
        data.add_field('isMangaSingle', '0')

        async with aiohttp.ClientSession(
            headers=self.__mangas_origines.headers, cookie_jar=aiohttp.CookieJar()
        ) as client_session:
            async with client_session.post(
                    'https://mangas-origines.fr/wp-admin/admin-ajax.php', cookies=self.__mangas_origines.auth.cookies,
                    data=data
            ) as r:
                if r.status != 200:
                    return False
                content = await r.json()
                return 'success' in content and content['success'] is True
