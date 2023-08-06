from mangas_origines.exceptions.exceptions import ChapterDoesNotExist, NotConnectedError
from mangas_origines.objects.comment import Comment
from mangas_origines.objects.chapter import Chapter
from mangas_origines import utils
from bs4 import BeautifulSoup
import aiohttp
import json
import re


class Action(enumerate):
    """A class that contains the actions variables"""
    DEFAULT = 'wpdLoadMoreComments'
    CLASSIC = 'wpdSorting'
    MOST_REACTED = 'wpdMostReactedComment'
    MOST_POPULAR_COMMENT = 'wpdHottestThread'


class Sort(enumerate):
    """A class that contains the processing variables"""
    NEWEST = 'newest'
    OLDEST = 'oldest'
    BY_VOTE = 'by_vote'


class Scan:
    """
    A class to create an Scan object

    ...

    Attributes
    ----------
    mangas_origines: MangasOrigines
        MangasOrigines object
    scan_id: int
        the scan id
    name_id: str
        the scan name id
    url: str
        the scan URL
    genres: dict
        the scan genres
    types: dict
        the scan types
    title: str
        the scan title
    year_of_release: str
        the years of release
    image_url: str
        the cover URL
    author_name: str
        the author name
    author_url: str
        the author URL
    artist_name: str
        the artist name
    artist_url: str
        the artist URL
    notes: float
        the note of scan
    ratting_count: int
        the ratting count of scan

    Methods
    -------
    get_chapter_name(chapter: str) -> str
        Get the chapter name from URl
    get_chapter_season(chapter: str) -> str
        Get the chapter season from URl
    get_all_chapters_url() -> list
        Get all chapter URL from scan
    __get_chapter(chapter_url: str) -> Chapter
        Create chapter object from chapter URL
    get_chapter_by_url() -> Chapter
        Get a chapter object from URL
    get_chapter_by_name(chapter_name: str) -> Chapter
        Get a chapter object from name
    get_first_chapter() -> Chapter
        Get the first chapter of scan
    get_last_chapter() -> Chapter
        Get the last chapter of scan
    get_all_comments(action: Action = Action.DEFAULT, sort: Sort = Sort.NEWEST) -> list or bool
        Get all comments of scan
    mark_has_favorite() -> bool:
        Mark scan has favorite
    """
    def __init__(
            self, mangas_origines: dict, scan_id: int, name_id: str, url: str, genres: dict,
            types: dict, title: str, year_of_release: str, image_url: str, author_name: str,
            author_url: str, artist_name: str, artist_url: str, notes: float, ratting_count: int
    ):
        from mangas_origines.mangas_origines import MangasOrigines

        self.mangas_origines: MangasOrigines = mangas_origines
        self.scan_id = scan_id
        self.name_id = name_id
        self.url = url
        self.genres = genres
        self.types = types
        self.title = title
        self.year_of_release = year_of_release
        self.image_url = image_url
        self.author_name = author_name
        self.author_url = author_url
        self.artist_name = artist_name
        self.artist_url = artist_url
        self.notes = notes
        self.ratting_count = ratting_count
        self.chapters_url = []
        self.has_seasons = False
        self.has_comments = False
        self.comments = []

    @staticmethod
    def get_chapter_name(chapter: str) -> str:
        """Get chapter number by chapter URL

        Parameters
        ----------
        chapter: str
            The chapter URL
            e.g: https://mangas-origines.fr/manga/martial-peak/chapitre-1/

        Returns
        -------
        str
            the chapter number in URL
        """
        chapter_url_split = chapter.split('/')
        chapter = chapter_url_split[len(chapter_url_split) - 2].replace('chapitre-', '')
        if re.findall(r'-[a-zA-Z%]+', chapter):
            chapter = chapter.split(re.findall(r'-[a-zA-Z%]+', chapter)[0])[0]
        return chapter

    def get_chapter_season(self, chapter: str) -> str:
        """Get season by chapter URL

        Parameters
        ----------
        chapter: str
            The chapter URL
            e.g: https://mangas-origines.fr/manga/martial-peak/chapitre-1/

        Returns
        -------
        str
            the season in URL
        """
        if self.has_seasons is False:
            return

        chapter_url_split = chapter.split('/')
        season = chapter_url_split[len(chapter_url_split) - 3].replace('saison-', '')
        if re.findall(r'-[a-zA-Z%]+', season):
            season = season.split(re.findall(r'-[a-zA-Z%]+', season)[0])[0]
        return season

    async def get_all_chapters_url(self) -> list:
        """Get all chapters URL

        Returns
        -------
        list
            all chapters URL of scan
        """
        async with aiohttp.ClientSession(headers=self.mangas_origines.headers) as client_session:
            async with client_session.post(f'https://mangas-origines.fr/manga/{self.name_id}/ajax/chapters/') as r:
                bs = BeautifulSoup(await r.text(), 'html.parser')

        for a in bs.find_all('a', href=True):
            href = str(a.get('href'))
            if 'http' in href and href not in self.chapters_url:
                self.chapters_url.append(href)

        if self.chapters_url and 'saison' in self.chapters_url[0]:
            self.has_seasons = True

        self.chapters_url.reverse()

        return self.chapters_url

    async def __get_chapter(self, chapter_url: str) -> Chapter:
        """Create Scan object by URL of scan

        Parameters
        ----------
        chapter_url: str
            The chapter url.
            e.g: https://mangas-origines.fr/manga/martial-peak/chapitre-1/

        Returns
        -------
        Chapter
            a Chapter object to get some infos or execute action about chapter

        Raises
        ------
        ChapterDoesNotExist
            If the chapter is not found.
        """
        if self.chapters_url and chapter_url not in self.chapters_url:
            raise ChapterDoesNotExist(chapter_url)

        chapter = self.get_chapter_name(chapter_url)

        async with aiohttp.ClientSession(headers=self.mangas_origines.headers) as client_session:
            async with client_session.get(chapter_url + '?style=paged') as r:
                bs = BeautifulSoup(await r.text(), 'html.parser')

        images_list = []
        for script in bs.find_all('script'):
            if script.contents and 'chapter_preloaded_images' in script.contents[0]:
                content = str(script.contents[0]).replace(' ', '').replace('varchapter_preloaded_images=', '') \
                    .split(',chapter_images_per_page')[0].strip()

                for link in json.loads(content):
                    if link not in images_list:
                        images_list.append(link)

        if not images_list:
            raise ChapterDoesNotExist(chapter_url)

        return Chapter(
            self.mangas_origines.headers, chapter_url, chapter, images_list
        )

    async def get_chapter_by_url(self, chapter_url: str) -> Chapter:
        """Get a chapter by URL

        Returns
        -------
        Chapter
            a Chapter object to get some infos or execute action about chapter
        """
        return await self.__get_chapter(chapter_url)

    async def get_chapter_by_name(self, chapter_name: str) -> Chapter:
        """Get a chapter by name

        Returns
        -------
        Chapter
            a Chapter object to get some infos or execute action about chapter
        """
        return await self.__get_chapter(self.url + '/' + chapter_name + '/')

    async def get_first_chapter(self) -> Chapter:
        """Get the first chapter of scan

        Returns
        -------
        Chapter
            a Chapter object to get some infos or execute action about chapter
        """
        if not self.chapters_url:
            await self.get_all_chapters_url()

        return await self.__get_chapter(self.chapters_url[0])

    async def get_last_chapter(self) -> Chapter:
        """Get the last chapter of scan

        Returns
        -------
        Chapter
            a Chapter object to get some infos or execute action about chapter
        """
        if not self.chapters_url:
            await self.get_all_chapters_url()

        return await self.__get_chapter(self.chapters_url[len(self.chapters_url) - 1])

    async def get_all_comments(self, action: Action = Action.DEFAULT, sort: Sort = Sort.NEWEST) -> list or bool:
        """Get all comments of scan

        Returns
        -------
        Chapter
            a list contain all comments
        """
        data = aiohttp.FormData()
        data.add_field('action', action)
        data.add_field('sorting', sort)
        data.add_field('offset', '0')
        data.add_field('lastParentId', '0')
        data.add_field('isFirstLoad', '1')
        data.add_field('wpdType', '')
        data.add_field('postId', str(self.scan_id))

        async with aiohttp.ClientSession(headers=self.mangas_origines.headers) as client_session:
            async with client_session.post(
                    f'https://mangas-origines.fr/wp-content/plugins/wpdiscuz/utils/ajax/wpdiscuz-ajax.php',
                    data=data
            ) as r:
                json_return = await r.json()

        comment_data = json_return['data']['comment_list'] if 'comment_list' in json_return['data'] else \
            json_return['data']['message']
        bs = BeautifulSoup(comment_data, 'html.parser')
        comments = bs.find_all('div', {'class': 'wpd-comment'})

        if comments:
            self.has_comments = True

            for x in comments:
                div = utils.parse_comment_div(x)
                self.comments.append(Comment(self, div[0], div[1], div[2], div[3], div[4], div[5], div[6]))

        return self.comments if self.has_comments else False

    async def mark_has_favorite(self) -> bool:
        """Mark scan has favorite

        Returns
        -------
        bool
            return True on success, False otherwise

        Raises
        ------
        NotConnectedError
            If you aren't connected
        """
        if self.mangas_origines.auth is None:
            raise NotConnectedError('You must login to your account to use this method.')
        elif not self.mangas_origines.auth.cookies:
            raise NotConnectedError('No cookies saved.')
        else:
            data = aiohttp.FormData()
            data.add_field('action', 'wp-manga-user-bookmark')
            data.add_field('postID', self.scan_id)
            data.add_field('chapter', '')
            data.add_field('page', '1')

            async with aiohttp.ClientSession(
                headers=self.mangas_origines.headers, cookie_jar=aiohttp.CookieJar()
            ) as client_session:
                async with client_session.post(
                    'https://mangas-origines.fr/wp-admin/admin-ajax.php', cookies=self.mangas_origines.auth.cookies, data=data
                ) as r:
                    if r.status != 200:
                        return False
                    content = await r.json()
                    return 'success' in content and content['success'] is True
