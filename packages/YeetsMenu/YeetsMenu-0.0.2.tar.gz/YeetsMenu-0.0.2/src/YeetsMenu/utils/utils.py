import os
from colorama import Style, Fore


def clear_screen():
    os.system("clear")


def enter_confirmation():
    input(f"{Fore.CYAN}Press enter to continue...{Style.RESET_ALL}")