from cdkkConsole import Console
from cdkkGamePiece import *
from cdkkBoard import *

console = Console()
card = Card(53, context = {"style":"red"}) # Joker
console.print(*card.richtext(), sep="\n")


board = Board(3, 3)
board = Board(3, 3, {0:" ", -1:"?"})
board.set_unused(0, 0)
board.set_unused(0, 2)
board.set_unused(2, 0)
board.set_unused(2, 2)
board.set(0, 0, piece = GamePiece(1, context={"style":"red"}))
board.set(1, 0, piece = GamePiece(2, context={"style":"green"}))
board.set(2, 0, piece = GamePiece(3, context={"style":"red"}))
board.set(0, 1, piece = GamePiece(4, context={"style":"red"}))
board.set(1, 1, piece = GamePiece(5, context={"style":"blue"}))
board.set(2, 1, piece = GamePiece(6, context={"style":"blue"}))
board.set_style(1, 1, "default on blue")
board.rt_stylise(Board.borders_single1, style="blue")
console.print("\nborders_single1")
console.print(*board.richtext(borders=Board.borders_single1, unused = Text('#', style = "yellow bold"), gridref = "bright_black"), sep="\n")
console.print("\nborders_outside1 - No grid ref")
console.print(*board.richtext(borders=Board.borders_outside1), sep="\n")
console.print("\nborders_outside1 - With grid ref")
console.print(*board.richtext(borders=Board.borders_outside1, gridref = "bright_black"), sep="\n")
console.print("\nNo borders")
console.print(*board.richtext(borders={}, unused = Text('#', style = "yellow bold")), sep="\n")
console.print("\nStrings")
console.print(*board.strings(), sep="\n")

br = "default on red"
bg = "default on green"
bb = "default on blue"
board = Board(8, 8)
board.set_style_pattern([[br, bg, bb],[bg, bb, br],[bb, br, bg]])
console.print("\nRGB pattern")
console.print(*board.richtext(borders={}), sep="\n")

bk0 = "default on cornsilk1"
bk1 = "default on orange4"
chequered = [[bk0, bk1],[bk1, bk0]]
board = Board(8, 8)
board.set_style_pattern(chequered)
board.set(0,0,1)
board.set(1,0,2)
board.set(2,0,3)
console.print("\nChess board pattern")
console.print(*board.richtext(borders={}), sep="\n")
console.print("\nChess board pattern - Outside border")
console.print(*board.richtext(borders=Board.borders_outside1, gridref = "bright_black"), sep="\n")
