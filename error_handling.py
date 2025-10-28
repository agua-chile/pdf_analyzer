# Library imports
import traceback
import sys
from textwrap import indent
from colorama import Fore, Style, init


# Initialize Colorama (auto-reset ensures colors don't 'leak')
init(autoreset=True)


def handle_error(exc: Exception, msg: str = ''):
    exc_type, exc_value, exc_tb = sys.exc_info()
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))

    print('\n' + Fore.RED + '=' * 100)
    print(Fore.RED + Style.BRIGHT + '🚨  ERROR OCCURRED')
    if msg:
        print(Fore.YELLOW + f'Context: {msg}')
    print(Fore.RED + '-' * 100)
    print(Fore.CYAN + f'Type: {exc_type.__name__}')
    print(Fore.MAGENTA + f'Message: {exc}')
    print(Fore.RED + '-' * 100)
    print(Fore.WHITE + Style.BRIGHT + 'Traceback (most recent call last):\n')
    print(indent(Fore.LIGHTBLACK_EX + tb_str.strip(), '  '))
    print(Fore.RED + '=' * 100 + Style.RESET_ALL + '\n')
