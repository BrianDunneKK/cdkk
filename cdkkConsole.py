from rich import print as rprint
from rich.prompt import Prompt as richPrompt
from rich.console import Console as richConsole
from cdkkConfig import Config

# ----------------------------------------

class Prompt(richPrompt):
    prompt_suffix = ""

class Console:
    default_config = {
        "silent": False           # True = Hide all console output
        ,"cls_first_print": True  # True = Clear the screen when print is first called
    }
    console = richConsole()

    def __init__(self, init_config={}):
        self.config = Config(Console.default_config)
        self.config.update(init_config)
        self.clear_next_print = self.config.get("cls_first_print", False)

    def print(self, *args, **kwargs):
        if self.clear_next_print:
            self.clear()
            self.clear_next_print = False
        if not self.config.get("silent", False):
            Console.console.print(*args, **kwargs, highlight = False)

    def clear(self):
        if not self.config.get("silent", False):
                self.console.clear()
    
# ----------------------------------------

if __name__ == '__main__':
    console = Console()
    console.print('\n [red]WELCOME[/red] [green]TO[/green] [blue]Console[/blue] \n')
