import os
import sys
from argparse import ArgumentParser, HelpFormatter

import startds

class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """
    def __init__(self, *, missing_args_message=None, **kwargs):
        self.missing_args_message = missing_args_message
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if (self.missing_args_message and (args is not None) and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.missing_args_message)
        
        return super().parse_args(args, namespace)

    def error(self, message):
        super().error(message)


class BaseCommand:
    """
    1. loads the command class and calls its ``run_from_argv()`` method.

    2. The ``run_from_argv()`` method calls ``create_parser()`` to get
       an ``ArgumentParser`` for the arguments, parses them, and then 
       calls the ``execute()`` method, passing the parsed arguments.

    3. The ``execute()`` method attempts to carry out the command by
       calling the ``handle()`` method with the parsed arguments; any
       output produced by ``handle()`` will be printed to stdout.

    Thus, the ``handle()`` method is typically the starting point for
    subclasses; many built-in commands and command types either place
    all of their logic in ``handle()``, or perform some additional
    parsing work in ``handle()`` and then delegate from it to more
    specialized methods as needed.

    Several attributes affect behavior at various steps along the way:

    ``help``
        A short description of the command, which will be printed in
        help messages.
    """
    # Metadata about this command.
    help = ''
    def __init__(self):
        pass

    def create_parser(self, prog_name, subcommand, **kwargs):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = CommandParser(
            prog='%s %s' % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
            missing_args_message=getattr(self, 'missing_args_message', None),
            **kwargs
        )
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this command, derived from
        ``self.usage()``.
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        parser = self.create_parser(argv[0], argv[1])
        parser.add_argument('args', nargs='*')  # catch-all
        parser.add_argument('-f', nargs='*')  # catch-all
        parser.add_argument('--api', nargs='*')  # catch-all
        parser.add_argument('--mode', nargs='*')  # catch-all
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)

        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop('args', ())

        try:
            self.execute(*args, **cmd_options)
        except Exception:
            sys.exit()

    def execute(self, *args, **options):
        """
        Try to execute this command, performing system checks if needed (as
        controlled by the ``requires_system_checks`` attribute, except if
        force-skipped).
        """
        output = self.handle(*args, **options)
        return output

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')