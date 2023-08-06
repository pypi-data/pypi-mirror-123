class ProgressBar:
    """
    A class to create a progress bar

    ...

    Attributes
    ----------
    total: dict
        the total of element to progress
    prefix: str
        the prefix to show before the progress bar
    iteration: float
        the actual iteration

    Methods
    -------
    progress(iteration: float)
        update the iterator to custom value
    __update_progress_bar()
        update the progress bar display
    """

    def __init__(self, total: float, prefix: str):
        self.total = total
        self.prefix = prefix

        self.iteration: float = 0

    def progress(self, iteration: float):
        self.iteration = iteration
        self.__update_progress_bar()

    def __update_progress_bar(self):
        f = int(100 * self.iteration // self.total)
        print(f"{self.prefix} [{'█' * f + ' ' * (100 - f)}] {100 * (self.iteration / float(self.total)):.2f}%", end='\r')

        if self.iteration == self.total:
            print()
