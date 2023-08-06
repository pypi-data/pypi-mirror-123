from bs4.element import Tag
import re
import os


def truncate_emojis(text: str) -> str:
    """Remove emojis in string

    Parameters
    ----------
    text: str
        The text to clean

    Returns
    -------
    str
        the text without the emojis
    """
    pattern = re.compile(
        pattern="["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF" u"\U0001F1E0-\U0001F1FF"
                "]+", flags=re.UNICODE
    )
    return pattern.sub(r'', text)


def create_folder(folder: str):
    """Create folders recursively

    Parameters
    ----------
    folder: str
        The folder path to create
    """
    if os.path.exists(folder) is False:
        os.makedirs(folder)


def delete_folder(folder: str):
    """Delete folders recursively

    Parameters
    ----------
    folder: str
        The folder path to delete
    """
    import shutil
    if os.path.exists(folder):
        shutil.rmtree(folder)


def print_error(text: str):
    """Print text in red

    Parameters
    ----------
    text: str
        The text to print in red
    """
    print('\033[91m' + text + '\033[91m')


async def limit_tasks(number: int, *tasks) -> list:
    """Limitation of coroutines launched simultaneously

    Parameters
    ----------
    number: int
        The maximum number of tasks
    tasks
        The list of tasks to launch

    Returns
    -------
    list
        the coroutines list passed with tasks variable
    """
    import asyncio

    semaphore = asyncio.Semaphore(number)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))


def clear_line():
    """Clear actual Terminal line"""
    print('\r\033[K', end='')


def replace_french_months_by_english(date: str):
    """Replace french months by english in string

    Parameters
    ----------
    date: str
        Number of current elements
    """
    return date.replace('janvier', 'January').replace('février', 'February').replace('mars', 'March') \
        .replace('avril', 'April').replace('mai', 'May').replace('juin', 'June').replace('juillet', 'July') \
        .replace('août', 'August').replace('septembre', 'September').replace('octobre', 'October') \
        .replace('novembre', 'November').replace('décembre', 'December')


def parse_comment_div(div: Tag) -> tuple:
    """Retrieve useful information from a comment div

    Parameters
    ----------
    div: Tag
        Comment in BeautifulSoup4 Tag format

    Returns
    -------
    tuple
        useful information in the comments
    """
    import datetime

    comment_id = int(div.get('id').replace('wpd-comm-', '').replace('_0', ''))
    comment_div = div.find('div', {'class': 'wpd-comment-text'})
    comment = comment_div.text.strip() if comment_div.find('p') is None else comment_div.find('p').text
    author = div.find('div', {'class': 'wpd-comment-author'}).text.strip()
    role_div = div.find('div', {'class': 'wpd-comment-label'})
    role = None if role_div is None else role_div.get('wpd-tooltip')
    date = datetime.datetime.strptime(
        replace_french_months_by_english(div.find('div', {'class': 'wpd-comment-date'}).get('title')),
        '%d %B %Y %H:%M'
    )
    vote = div.find('div', {'class': 'wpd-vote-result'}).get('title')
    avatar = div.find('div', {'class': 'wpd-avatar'}).find('img').get('src')

    return comment_id, author, role, comment, date, vote, avatar
