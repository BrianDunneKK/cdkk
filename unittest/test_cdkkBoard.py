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
        self.assertTrue(board.get(0,0) == 0)
        self.assertTrue(board.get(0,10) < 0)
        self.assertTrue(board.get(10,0) < 0)

    def test_set1(self):
        board = Board(4, 5)
        success = board.set(0, 0, 1)
        self.assertTrue(success)
        self.assertTrue(board.get(0,0) == 1)

        success = board.set(3, 4, 2)
        self.assertTrue(success)
        self.assertTrue(board.get(3,4) == 2)

        board.set(2, 3, 5)
        success = board.set(2, 3, 6)
        self.assertTrue(success)
        self.assertTrue(board.get(2,3) == 6)

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
        self.assertTrue(board.get(1,1) == 1)

        success = board.clear(1, 1)
        self.assertTrue(success)
        self.assertTrue(board.get(1,1) == 0)

    def test_clear_all(self):
        board = Board(3, 2)
        board.set(0, 0, 1)
        board.set(1, 1, 2)
        board.set(2, 1, 3)
        self.assertTrue(board.get(2,1) == 3)
        board.clear_all()
        self.assertTrue(board.get(0,0) == 0)
        self.assertTrue(board.get(1,1) == 0)
        self.assertTrue(board.get(2,1) == 0)

    def test_strings1(self):
        board = Board(3, 3)
        board.symbols({0:".", 1:"X", 2:"O", -1:"?"})
        strs = board.strings()
        self.assertEquals(strs[2], ". . .")

        board.set(0, 0, 1)
        board.set(1, 1, 1)
        board.set(2, 2, 2)
        strs = board.strings()
        self.assertEquals(strs[0], "X . .")
        self.assertEquals(strs[1], ". X .")
        self.assertEquals(strs[2], ". . O")

        board.set(0, 2, 9)
        strs = board.strings()
        self.assertEquals(strs[2], "? . O")


    def test_strings2(self):
        board = Board(3, 2)
        board.set(1, 1, 1)

        strs = board.strings(as_int=True)
        self.assertEquals(strs[0], "0 0 0")
        self.assertEquals(strs[1], "0 1 0")

        strs = board.strings(digits=2, as_int=True)
        self.assertEquals(strs[1], "00 01 00")

        strs = board.strings(sep="-", as_int=True)
        self.assertEquals(strs[0], "0-0-0")

    def test_frequency(self):
        board = Board(3, 3)
        board.set(0, 0, 1)
        board.set(1, 1, 1)
        board.set(2, 2, 2)
        freq = board.frequency()
        self.assertEquals(freq[0], 6)
        self.assertEquals(freq[1], 2)
        self.assertEquals(freq[2], 1)


if __name__ == '__main__':
    unittest.main()