import unittest
from cdkkGame import Game

class Test_cdkkGame(unittest.TestCase):
    def test_Game(self):
        game = Game()
        self.assertFalse(game.game_over)

    def test_counts1(self):
        game = Game()
        game.init()
        counts = game.counts
        self.assertEquals(counts["players"], 1)
        self.assertEquals(counts["turns"], 0)
        self.assertEquals(counts["games"], 0)
        self.assertEquals(counts["wins"][0], 0)

    def test_counts2(self):
        game = Game({"players":3})
        game.init()
        counts = game.counts
        self.assertEquals(counts["players"], 3)
        self.assertEquals(counts["wins"][2], 0)

    def test_start(self):
        game = Game()
        game.init()
        game.start()
        counts = game.counts
        self.assertEquals(counts["turns"], 1)
        self.assertEquals(counts["games"], 1)

    def test_take(self):
        game = Game()
        game.start()
        game.take(None)
        counts = game.counts
        self.assertEquals(counts["turns"], 2)
        self.assertEquals(counts["games"], 1)

        game.take(None)
        game.take(None)
        counts = game.counts
        self.assertEquals(counts["turns"], 4)

    def test_max_turns(self):
        game = Game()
        self.assertTrue(game.max_turns > 999999999)
        game = Game({"max_turns":6})
        self.assertEquals(game.max_turns, 6)
        counts = game.counts
        self.assertEquals(counts["max_turns"], 6)

    def test_take_turns1(self):
        game = Game(({"players":2}))
        game.init()
        game.start()
        self.assertEquals(game.current_player, 1)
        game.take(None)
        self.assertEquals(game.current_player, 2)
        game.take(None)
        self.assertEquals(game.current_player, 1)

    def test_take_turns2(self):
        game = Game(({"players":2}))
        game.next_after_update = False
        game.init()
        game.start()
        self.assertEquals(game.current_player, 1)
        game.take(None)
        self.assertEquals(game.current_player, 1)
        game.next_after_update = True
        game.take(None)
        self.assertEquals(game.current_player, 2)

if __name__ == '__main__':
    unittest.main()