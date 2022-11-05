import unittest
from cdkkBoard import Board

class Test_cdkkBoard(unittest.TestCase):
    def test_Board1(self):
        board = Board()
        self.assertEqual(board.xsize, 0)
        self.assertEqual(board.ysize, 0)

    def test_Board2(self):
        board = Board(3, 8)
        self.assertEqual(board.xsize, 3)
        self.assertEqual(board.ysize, 8)
        success = board.resize(4, 6)
        self.assertTrue(success)
        self.assertEqual(board.xsize, 4)
        self.assertEqual(board.ysize, 6)

    def test_get(self):
        board = Board(3, 8)
        x = board.get(0,0)
        self.assertEquals(board.get(0,0), " ")
        self.assertEquals(board.get(0,10), "?")
        self.assertEquals(board.get(10,0), "?")
        self.assertTrue(board.get(0, 0, False) == 0)
        self.assertTrue(board.get(0, 10, False) < 0)
        self.assertTrue(board.get(10, 0, False) < 0)

    def test_set1(self):
        board = Board(4, 5)
        success = board.set(0, 0, 1)
        self.assertTrue(success)
        self.assertTrue(board.get(0, 0, False) == 1)

        success = board.set(3, 4, 2)
        self.assertTrue(success)
        self.assertTrue(board.get(3, 4, False) == 2)

        board.set(2, 3, 5)
        success = board.set(2, 3, 6)
        self.assertTrue(success)
        self.assertTrue(board.get(2, 3, False) == 6)

    def test_set2(self):
        board = Board(4, 5)
        success = board.set(0, 0, 1)
        self.assertTrue(success)

        success = board.set(0, 0, 2)
        self.assertTrue(success)

        success = board.set(0, 0, 2, overwrite_ok=False)
        self.assertFalse(success)

    def test_clear(self):
        board = Board(6, 2)
        success = board.set(1, 1, 1)
        self.assertTrue(success)
        self.assertTrue(board.get(1, 1, False) == 1)

        success = board.clear(1, 1)
        self.assertTrue(success)
        self.assertTrue(board.get(1, 1, False) == 0)

    def test_clear_all(self):
        board = Board(3, 2)
        board.set(0, 0, 1)
        board.set(1, 1, 2)
        board.set(2, 1, 3)
        self.assertTrue(board.get(2, 1, False) == 3)
        board.clear_all()
        self.assertTrue(board.get(0, 0, False) == 0)
        self.assertTrue(board.get(1, 1, False) == 0)
        self.assertTrue(board.get(2, 1, False) == 0)

    def test_strings1(self):
        board = Board(3, 3)
        board.symbols({0:".", 1:"X", 2:"O", -1:"?"})
        strs = board.strings()
        self.assertEquals(strs[0], ". . .")

        board.set(0, 0, 1)
        board.set(1, 1, 1)
        board.set(2, 2, 2)
        strs = board.strings()
        self.assertEquals(strs[0], ". . O")
        self.assertEquals(strs[1], ". X .")
        self.assertEquals(strs[2], "X . .")

        board.set(0, 2, 9)
        strs = board.strings()
        self.assertEquals(strs[0], "? . O")

    def test_strings2(self):
        board = Board(3, 2)
        board.set(1, 1, 1)

        strs = board.strings(as_symbol=False)
        self.assertEquals(strs[0], "0 1 0")
        self.assertEquals(strs[1], "0 0 0")
 
        strs = board.strings(digits=2, as_symbol=False)
        self.assertEquals(strs[0], "00 01 00")

        strs = board.strings(sep="-", as_symbol=False)
        self.assertEquals(strs[1], "0-0-0")

    def test_frequency(self):
        board = Board(3, 3)
        board.set(0, 0, 1)
        board.set(1, 1, 1)
        board.set(2, 2, 2)
        freq = board.frequency()
        self.assertEquals(freq[0], 6)
        self.assertEquals(freq[1], 2)
        self.assertEquals(freq[2], 1)

    def test_inv_symbols(self):
        board = Board(3, 3)
        board.symbols({0:".", 1:"X", 2:"O", -1:"?"})
        self.assertEquals(board._inv_symbols["."], 0)
        self.assertEquals(board._inv_symbols["X"], 1)
        self.assertEquals(board._inv_symbols["O"], 2)
        self.assertEquals(board._inv_symbols["?"], -1)

    def test_to_from_symbols(self):
        board = Board(3, 3)
        board.symbols({0:".", 1:"X", 2:"O", -1:"@"})
        self.assertEquals(board.to_symbol(1), 'X')
        self.assertEquals(board.to_symbol(2), 'O')
        self.assertEquals(board.to_symbol(9), '@')
        self.assertEquals(board.from_symbol('X'), 1)
        self.assertEquals(board.from_symbol('.'), 0)
        self.assertEquals(board.from_symbol('#'), -1)

    def test_in_a_row(self):
        board = Board(6, 5)
        board.set(1, 2, 9)
        board.set(5, 3, 9)
        board.set(4, 0, 9)
        # . . . . . .
        # . . . . . X
        # . X . . . .
        # . . . . . .
        # . . . . X .
        self.assertEquals(board._in_a_row_dir(0, 0, 'N'), 5)
        self.assertEquals(board._in_a_row_dir(0, 0, 'E'), 4)
        self.assertEquals(board._in_a_row_dir(0, 0, 'S'), 1)
        self.assertEquals(board._in_a_row_dir(0, 0, 'W'), 1)

        self.assertEquals(board._in_a_row_dir(1, 3, 'N'), 2)
        self.assertEquals(board._in_a_row_dir(1, 3, 'E'), 4)
        self.assertEquals(board._in_a_row_dir(1, 3, 'S'), 1)
        self.assertEquals(board._in_a_row_dir(1, 3, 'W'), 2)

        counts = board.in_a_row(1,3)
        self.assertEquals(counts['SE'], 3)
        self.assertEquals(counts['NS'], 2)
        self.assertEquals(counts['EW'], 5)
        self.assertEquals(counts['NESW'], 3)
        self.assertEquals(counts['cell'], ' ')

    def test_split_turn(self):
        board = Board(3,3)
        x,y,c = board.split_turn("1,2,go")
        self.assertEquals(x, 0)
        self.assertEquals(y, 1)
        self.assertEquals(c, "go")

        x,y,c = board.split_turn("2,3")
        self.assertEquals(x, 1)
        self.assertEquals(y, 2)
        self.assertEquals(c, "")

        x,y,c = board.split_turn("1;2;go")
        self.assertEquals(x, -1)
        self.assertEquals(y, -1)
        self.assertEquals(c, "1;2;go")

        x,y,c = board.split_turn("1,3,go")
        self.assertEquals(x, 0)
        self.assertEquals(y, 2)
        self.assertEquals(c, "go")

        x,y,c = board.split_turn("1,3,go", start_at_1=False)
        self.assertEquals(x, -1)
        self.assertEquals(y, -1)
        self.assertEquals(c, "1,3,go")

        x,y,c = board.split_turn("4,3,go")
        self.assertEquals(x, -1)
        self.assertEquals(y, -1)
        self.assertEquals(c, "4,3,go")

if __name__ == '__main__':
    unittest.main()