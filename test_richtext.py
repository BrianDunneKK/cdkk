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
board.rt_stylise(Board.borders_single1, style="blue")
console.print(*board.richtext(borders=Board.borders_single1, unused = Text('#', style = "yellow bold"), gridref = "bright_black"), sep="\n")
console.print(*board.strings(), sep="\n")

