class ScanNotFound(Exception):
    """A class for handling exception when a scan not found"""
    def __init__(self, scan: str):
        super().__init__(f"I can't find {scan}!")


class WrongDomain(Exception):
    """A class for handling exception when enter domain is not correct"""
    def __init__(self):
        super().__init__('This program only work with mangas-origines.fr.')


class BadScanIdFormat(Exception):
    """A class for handling exception when the scan ID is in bad format"""
    def __init__(self):
        super().__init__("I can't get scan ID.")


class ChapterDoesNotExist(Exception):
    """A class for handling exception when the chapter URL is not found"""
    def __init__(self, chapter_url):
        super().__init__(f"The chapter: {chapter_url} doesn't exist.")


class LoginError(Exception):
    """A class for handling exception when the login not work correctly"""
    def __init__(self, login_message: str):
        super().__init__(login_message)


class NotConnectedError(Exception):
    """A class for handling exception when user is not connected"""
    def __init__(self, error_message: str):
        super().__init__(error_message)


class MangasOriginesNotAvailable(Exception):
    """
    A class for handling exception when status code isn't 200 and 404

    ...

    Attributes
    ----------
    error_code: int
        the error code that was returned
    """
    def __init__(self, error_code: int):
        self.error_code = str(error_code)
        super().__init__(f'Mangas Origines is not available, error: {self.error_code}!')
