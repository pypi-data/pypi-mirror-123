from YeetsMenu.generics.selectable import Selectable
import typing
import traceback
from colorama import Style, Fore


class Option(Selectable):
    def __init__(self, name: str, function: typing.Callable, *func_args):
        super().__init__(name)

        self.function: typing.Callable = function
        self.func_args = func_args

    def run(self):
        try:
            self.function(*self.func_args)
        except Exception as e:
            print(f"{Fore.LIGHTMAGENTA_EX}A error occurred while running {self.function.__name__}:{Style.RESET_ALL}")
            print(traceback.format_exc())

        input(f"{Fore.CYAN}Press enter to continue...{Style.RESET_ALL}")


