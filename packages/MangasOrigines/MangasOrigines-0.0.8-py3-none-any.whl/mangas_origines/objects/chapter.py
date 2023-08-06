class Chapter:
    """
    A class to create a Chapter object

    ...

    Attributes
    ----------
    headers : dict
        use of personalized headers for requests
    chapter_url : str
        the scan URL
    chapter_id : str
        the chapter id
    images_url : str
        the chapter images URL
    """
    def __init__(
            self, headers: dict, chapter_url: str, chapter_id: str, images_url: str
    ):
        self.headers = headers
        self.chapter_url = chapter_url
        self.chapter_id = chapter_id
        self.images_url = images_url
