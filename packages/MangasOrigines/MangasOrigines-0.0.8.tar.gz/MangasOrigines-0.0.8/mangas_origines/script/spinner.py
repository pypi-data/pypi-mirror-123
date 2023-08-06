from mangas_origines.utils import clear_line
import asyncio


class Spinner:
    """
    A class to create a spinner

    ...

    Attributes
    ----------
    text: dict
        the text to show after spinner
    dots: list
        a list who contains the spinner chars
    task
        the actual launching task

    Methods
    -------
    __start_spinner()
        launch the spinner
    start()
        initialize the spinner launch
    stop()
        stop the spinner task
    set_text(new_text: str)
        edit the text after spinner
    """

    def __init__(self, text: str = None):
        self.text = text

        self.dots = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠦', '⠧', '⠇', '⠏']
        self.task = None

    async def __start_spinner(self):
        while True:
            for item in self.dots:
                text = '' if self.text is None else ' ' + self.text
                print('\033[92m' + item + '\033[0m' + text, end='\r')
                await asyncio.sleep(0.08)

    async def start(self):
        self.task = asyncio.get_event_loop().create_task(self.__start_spinner())

    async def stop(self):
        if self.task is not None:
            self.task.cancel()
            clear_line()

    def set_text(self, new_text: str):
        self.text = new_text
