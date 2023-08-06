import asyncio
import sys


class ArgumentsBuilder:
    """
    A class to create an arguments builder

    ...

    Attributes
    ----------
    description : str
        the script description
    args : list
        the list of arguments to parse
    arguments : dict
        the list containing information about the arguments
    arguments : dict
        the list containing information about the arguments
    __help_content : dict
        the contents of the help command

    Methods
    -------
    add_argument(argument_name: str, action=None, description: str = None, command_usage: str = None)
        Add an argument to consider in the script
    build_help()
        Generate and print the help command
    build()
        Build and launch the arguments builder
    """

    def __init__(self, description: str, args: list = None):
        if args is None:
            args = sys.argv

        self.description = description
        self.args = args

        self.arguments = {}
        self.__help_content = None

    def add_argument(
            self, argument_name: str, action=None, description: str = None, command_usage: str = None
    ):
        """Add an argument to consider

        Parameters
        ----------
        argument_name : str
            The argument that calls the function
        action
            The function/coroutine to run when the command is executed.
        description : str
            Description of the command.
        command_usage : str
            The use of the command.
        """
        self.arguments[argument_name] = {'action': action, 'description': description, 'command_usage': command_usage}

    def build_help(self):
        """Generate and print the help command"""
        if self.__help_content is None:
            self.__help_content = f"\n\033[1m{self.description}\033[0m\n\nCommand list:\n"
            for x in self.arguments:
                self.__help_content += f'・\033[1mmangas-origines {self.arguments[x]["command_usage"]}\033[0m | {self.arguments[x]["description"]}\n'

        print(self.__help_content)

    def build(self):
        """Build and launch the arguments builder"""
        if len(self.args) == 1 or '--help' in self.args or '-H' in self.args:
            return self.build_help()

        for i, x in enumerate(self.args):
            if x in self.arguments:
                self.arguments[x]['args'] = self.args
                if asyncio.iscoroutinefunction(self.arguments[x]['action']):
                    asyncio.get_event_loop().run_until_complete(self.arguments[x]['action'](self.arguments[x]))
                else:
                    self.arguments[x]['action'](self.arguments[x])
