from mangas_origines import utils
from bs4 import BeautifulSoup
import aiohttp


class Comment:
    """
    A class to create a Comment object

    ...

    Attributes
    ----------
    scan : Scan
        use of personalized headers for requests
    comment_id : int
        the comment ID
    author : str
        the author of comment
    author_role : str
        the author role
    text : str
        the chapter content
    date : str
        the date the comment was published
    vote : str
        the comment vote
    avatar : str
        the user's avatar

    Methods
    -------
    get_all_response() -> list or bool
        Get all the answers of the comment
    """
    def __init__(
            self, scan, comment_id: int, author: str, author_role: str, text: str, date: str,
            vote: str, avatar: str
    ):
        self.scan = scan
        self.comment_id = comment_id
        self.author = author
        self.author_role = author_role
        self.text = text
        self.date = date
        self.vote = vote
        self.avatar = avatar
        self.has_responses = False
        self.responses = []

    async def get_all_response(self) -> list or bool:
        """Get all responses of comment

        Returns
        -------
        Chapter
            a list contain all responses of comment
        """
        data = aiohttp.FormData()
        data.add_field('action', 'wpdShowReplies')
        data.add_field('commentId', str(self.comment_id))
        data.add_field('postId', str(self.scan.scan_id))

        async with aiohttp.ClientSession(headers=self.scan.headers) as client_session:
            async with client_session.post(
                f'https://mangas-origines.fr/wp-content/plugins/wpdiscuz/utils/ajax/wpdiscuz-ajax.php', data=data
            ) as r:
                json_return = await r.json()

        bs = BeautifulSoup(json_return['data']['comment_list'], 'html.parser')
        comments = bs.find_all('div', {'class': 'wpd-comment'})

        if comments and len(comments) >= 2:
            self.has_responses = True
            comments.pop(0)

            for x in comments:
                div = utils.parse_comment_div(x)
                self.responses.append(Comment(self.scan, div[0], div[1], div[2], div[3], div[4], div[5], div[6]))

        return self.responses if self.has_responses else False
