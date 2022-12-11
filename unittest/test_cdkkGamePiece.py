import unittest
from cdkkGamePiece import *

class Test_cdkkGamePiece(unittest.TestCase):
    def test_GamePiece(self):
        piece = GamePiece()
        self.assertEquals(piece.code, 0)
        self.assertEquals(piece.value, 0)
        self.assertEquals(piece.symbol, " ")
        self.assertEquals(piece.str_xcols, 1)
        self.assertEquals(piece.str_yrows, 1)

    def test_GamePiece5(self):
        piece = GamePiece(5)
        self.assertEquals(piece.code, 5)
        self.assertEquals(piece.value, 5)
        self.assertEquals(piece.symbol, "5")

    def test_GamePiece7X(self):
        piece = GamePiece(7, symbol="X")
        self.assertEquals(piece.code, 7)
        self.assertEquals(piece.value, 7)
        self.assertEquals(piece.symbol, "X")

    def test_GamePiece7O9(self):
        piece = GamePiece(7, 9, symbol="O")
        self.assertEquals(piece.code, 7)
        self.assertEquals(piece.value, 9)
        self.assertEquals(piece.symbol, "O")

    def test_clear(self):
        piece = GamePiece(5)
        self.assertEquals(piece.code, 5)
        piece.clear()
        self.assertEquals(piece.code, 0)

    def test_context(self):
        piece = GamePiece(5, context = {"player":"Fred"})
        self.assertEquals(piece.context["player"], "Fred")
        piece.context["player"] = "Barney"
        self.assertEquals(piece.context["player"], "Barney")

    def test_gamepieceset(self):
        set = GamePieceSet([GamePiece(1, 10), GamePiece(2, 20), GamePiece(3, 30), GamePiece(4, 40), GamePiece(5, 50)])
        self.assertEquals(set.count, 5)
        self.assertEquals(sorted(set.codes), [1,2,3,4,5])
        self.assertEquals(sorted(set.values), [10,20,30,40,50])
        self.assertEquals(set.strings, [["1"],["2"],["3"],["4"],["5"]])

# ----------------------------------------

class Test_cdkkGamePieceSet(unittest.TestCase):
    def test_GamePieceSet1(self):
        gpset = GamePieceSet()
        self.assertEquals(gpset.count, 0)

    def test_GamePieceSet2(self):
        p1 = GamePiece(1)
        p2 = GamePiece(2)
        p3 = GamePiece(3)
        gpset = GamePieceSet([p1,p2,p3])
        self.assertEquals(gpset.count, 3)
        self.assertEquals(gpset.codes, [1,2,3])
        self.assertEquals(gpset.values, [1,2,3])

    def test_GamePieceSet3(self):
        gpset = GamePieceSet()
        p1 = GamePiece(1)
        p2 = GamePiece(2)
        p3 = GamePiece(3)
        self.assertEquals(gpset.count, 0)
        gpset.append(p3)
        self.assertEquals(gpset.count, 1)
        gpset.append(p2)
        self.assertEquals(gpset.codes, [3,2])
        gpset.append(p1)
        self.assertEquals(gpset.values, [3,2,1])
        ppop = gpset.pop()  # LIFO
        self.assertEquals(gpset.values, [3,2])

    def test_GamePieceSet4(self):
        p1 = GamePiece(1)
        p2 = GamePiece(2)
        p3 = GamePiece(3)
        p4 = GamePiece(4)
        gpset = GamePieceSet([p1,p2])
        gpset.append(p3)
        gpset.appendleft(p4)
        self.assertEquals(gpset.values, [4,1,2,3])
        ppop1 = gpset.pop()
        self.assertEquals(gpset.values, [4,1,2])
        ppop2 = gpset.popleft()
        self.assertEquals(gpset.values, [1,2])

    def test_popN(self):
        gpset = GamePieceSet()
        for i in range(10):
            gpset.append(GamePiece(i+1))
        self.assertEquals(gpset.count, 10)

        gpset2 = gpset.popN(6)
        self.assertEquals(gpset.count, 4)
        self.assertEquals(gpset2.count, 6)

# ----------------------------------------

class Test_cdkkDice(unittest.TestCase):
    def test_Dice(self):
        piece = Dice()
        self.assertEquals(piece.code, 0)
        self.assertEquals(piece.value, 0)
        self.assertEquals(piece.symbol, " ")
        self.assertEquals(piece.str_xcols, 9)
        self.assertEquals(piece.str_yrows, 5)
        self.assertEquals("".join(piece.strings()), "┌───────┐│       ││       ││       │└───────┘")

    def test_Dice3(self):
        piece = Dice(3)
        self.assertEquals(piece.code, 3)
        self.assertEquals(piece.value, 3)
        self.assertEquals(piece.symbol, "3")
        self.assertEquals("".join(piece.strings()), "┌───────┐│ ●     ││   ●   ││     ● │└───────┘")

    def test_random(self):
        piece = Dice(random_dice = True)
        self.assertTrue(piece.code > 0)
        self.assertEquals(piece.value, piece.code)
        self.assertEquals(piece.symbol, str(piece.code))

    def test_context(self):
        piece = Dice(5, context = {"player":"Fred"})
        self.assertEquals(piece.context["player"], "Fred")
        piece.context["player"] = "Barney"
        self.assertEquals(piece.context["player"], "Barney")

# ----------------------------------------

class Test_cdkkCard(unittest.TestCase):
    def test_Card(self):
        piece = Card()
        self.assertEquals(piece.code, 0)
        self.assertEquals(piece.value, 0)
        self.assertEquals(piece.symbol, "  ")
        self.assertEquals(piece.suit, " ")
        self.assertEquals(piece.rank, " ")
        self.assertEquals(piece.str_xcols, 11)
        self.assertEquals(piece.str_yrows, 9)

    def test_Card5(self):
        piece = Card(5)
        self.assertEquals(piece.code, 5)
        self.assertEquals(piece.value, 5)
        self.assertEquals(piece.symbol, "5♠")
        self.assertEquals(piece.suit, "♠")
        self.assertEquals(piece.rank, "5")

    def test_Card143852(self):
        piece = Card(14)
        self.assertEquals(piece.symbol, "A♥")
        piece = Card(38)
        self.assertEquals(piece.symbol, "Q♦")
        piece = Card(52)
        self.assertEquals(piece.symbol, "K♣")

    def test_joker(self):
        piece = Card(53)
        self.assertEquals(piece.code, 53)
        self.assertEquals(piece.value, 53)
        self.assertEquals(piece.symbol, "Joker")
        self.assertEquals(piece.suit, "Joker")
        self.assertEquals(piece.rank, "☺")

    def test_random_code1(self):
        piece = Card(random_card = True)
        self.assertTrue(piece.code > 0)
        code = piece.random_code()
        self.assertTrue(code > 0)

    def test_context(self):
        piece = Card(5, context = {"hidden":True})
        self.assertTrue(piece.context["hidden"])
        piece.context["player"] = False
        self.assertFalse(piece.context["player"])

# ----------------------------------------

class Test_cdkkCardDeck(unittest.TestCase):
    def test_CardDeck(self):
        deck = CardDeck()
        self.assertEquals(deck.count, 52)

# ----------------------------------------

if __name__ == '__main__':
    unittest.main()