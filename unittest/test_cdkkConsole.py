import unittest
from cdkkConsole import Console
from cdkkConsole import Prompt

class Test_cdkkGame(unittest.TestCase):
    def test_Console(self):
        console = Console()
        console.print('\n [red]Testing[/red] [green]cdkkConsole[/green] [blue]class[/blue] \n')
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()