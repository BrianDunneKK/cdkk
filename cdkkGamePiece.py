import random

class GamePiece:
    def __init__(self, code: int = 0, value: int = -1, symbol: str = "", symbol_dict: dict = {}, random_code: bool = False, context: dict = {}):
        # Code = 0 ... Placeholder = Blank = Not a game piece
        if random_code:
            code = self.random_code()
        self.context = {}
        self.set(code, value, symbol, symbol_dict, context = context)

    @property
    def code(self) -> int:
        return self._code

    @property
    def value(self) -> int:
        return self._value

    @property
    def symbol(self) -> str:
        return self._symbol

    @symbol.setter
    def symbol(self, sym: str):
        self._symbol = sym

    def set(self, code: int = 0, value: int = -1, symbol: str = "", symbol_dict: dict = {}, context: dict = {}) -> int:
        self._code = code
        self._value = code if value == -1 else value
        self.context = self.context | context

        if symbol == "" and len(symbol_dict) > 0:
            default_sym = symbol_dict.get(-1, "")
            symbol = symbol_dict.get(code, default_sym)
        if symbol == "":
            if code == 0:
                self.symbol = " "
            else:
                self.symbol = str(code)
        else:
            self.symbol = symbol
        return code

    def random_code(self) -> int:
        return 0

    @property
    def str_xcols(self) -> int:
        return (len(self.strings()[0]))

    @property
    def str_yrows(self) -> int:
        return (len(self.strings()))

    def clear(self) -> int:
        return self.set()

    def strings(self) -> list[str]:
        return [f"{self.symbol}"]

# ----------------------------------------

class GamePieceSet:
    def __init__(self, pieces: list[GamePiece]) -> None:
        self.pieces = pieces

    @property
    def count(self) -> int:
        return len(self.pieces)

    @property
    def codes(self) -> list[int]:
        lst = [p.code for p in self.pieces]
        return lst

    @property
    def values(self) -> list[int]:
        lst = [p.value for p in self.pieces]
        return lst

    @property
    def strings(self) -> list[list[str]]:
        lst = [p.strings() for p in self.pieces]
        return lst

# ----------------------------------------

class Dice(GamePiece):
    pips = {
        0 : "         "
        ,1: "    ●    "
        ,2: "●       ●"
        ,3: "●   ●   ●"
        ,4: "● ●   ● ●"
        ,5: "● ● ● ● ●"
        ,6: "● ●● ●● ●"
        ,9: "●●●●●●●●●"
    }

    def __init__(self, code: int = 0, random_dice: bool = False, context: dict = {}):
        super().__init__(code, -1, "", random_code = random_dice, context = context)

    def random_code(self) -> int:
        return random.randint(1, 6)

    def strings(self) -> list[str]:
        pips = Dice.pips[self.code]
        return  [
            "┌───────┐"
            ,f"│ {pips[0]} {pips[1]} {pips[2]} │"
            ,f"│ {pips[3]} {pips[4]} {pips[5]} │"
            ,f"│ {pips[6]} {pips[7]} {pips[8]} │"
            ,"└───────┘"]
        

# ----------------------------------------

class Card(GamePiece):
    card_sym = {1: "A", 2:"2", 3:"3", 4:"4", 5:"5", 6:"6", 7:"7", 8:"8", 9:"9", 10:"10", 11:"J", 12:"Q", 13:"K"}
    suit_sym = {0: "♠", 1: "♥", 2: "♦", 3: "♣"}
    suit_char = {0: "S", 1: "H", 2: "D", 3: "C"}
    suit_name = {0: "Spades", 1: "Hearts", 2: "Diamonds", 3: "Clubs"}

    def __init__(self, code: int = 0, random_card: bool = False, context: dict = {}):
        super().__init__(code, -1, "", random_code = random_card, context = context)

    def set(self, code: int = 0, value: int = -1, symbol: str = "", symbol_dict: dict = {}, context: dict = {}) -> int:
        # Code = 1..52, Code % 13 = Card, Code // 13 = Suit
        # Code = 53 = Joker
        if code >= 1 and code <= 52:
            card_value = ((code-1) % 13) + 1
            self.rank = Card.card_sym[card_value]
            self.suit = Card.suit_sym[(code-1) // 13]
        elif code == 53:
            card_value = code
            self.rank = "☺"
            self.suit = "Joker"
        else:
            card_value = code
            self.rank = " "
            self.suit = " "
        if code == 53:
            sym = "Joker"
        else:
            sym = f"{self.rank}{self.suit}"
        return super().set(code, card_value, sym, symbol_dict, context = context)

    def random_code(self) -> int:
        return random.randint(1, 52)

    def strings(self) -> list[str]:
        if self.code == 0:
            return ["           "] * 9
        elif self.code < 100:
            return  [
                "┌─────────┐"
                ,f"│{self.rank:<2}       │"
                ,f"│         │"
                ,f"│         │"
                ,f"│  {self.suit:^5}  │"
                ,f"│         │"
                ,f"│         │"
                ,f"│       {self.rank:>2}│"
                ,"└─────────┘"]
        else: # ░ ▒ ▓ █
            return  [
                "┌─────────┐"
                ,"│▒▒▒▒▒▒▒▒▒│"
                ,"│▒▒▒▒▒▒▒▒▒│"
                ,"│▒▒▒▒▒▒▒▒▒│"
                ,"│▒▒▒▒▒▒▒▒▒│"
                ,"│▒▒▒▒▒▒▒▒▒│"
                ,"│▒▒▒▒▒▒▒▒▒│"
                ,"│▒▒▒▒▒▒▒▒▒│"
                ,"└─────────┘"]
        

# ----------------------------------------

if __name__ == '__main__':
    ttt_x = GamePiece(1, symbol="X")
    ttt_o = GamePiece(2, symbol="O")
    print(*ttt_x.strings(), sep="\n")
    print(*ttt_o.strings(), sep="\n")
    for i in range(6):
        die = Dice(i+1)
        print(*die.strings(), sep = "\n")

    card = Card(5)
    print(card.symbol)
    print(*card.strings(), sep="\n")
    card = Card(25)
    print(card.symbol)
    print(*card.strings(), sep="\n")
    card = Card(53)
    print(card.symbol)
    print(*card.strings(), sep="\n")
    card = Card(0)
    print(card.symbol)
    print(*card.strings(), sep="\n")
    card = Card(101)
    print(card.symbol)
    print(*card.strings(), sep="\n")