import unittest
from cdkkConfig import Config


class Test_cdkkConfig(unittest.TestCase):

    def test_get_config(self):
        cfg = Config()
        self.assertEqual(cfg.get("foo"), None)
        self.assertEqual(cfg.get("foo", "bar"), "bar")

    def test_set_config(self):
        cfg = Config()
        cfg.set("foo", "bar")
        self.assertEqual(cfg.get("foo", "bar"), "bar")
        self.assertEqual(cfg.get("foo", "buzz"), "bar")

    def test_update_config(self):
        cfg = Config()
        cfg.set("foo", "bar")
        cfg.set("ping", "pong")
        cfg.update({"foo":"one", "ping":"two"})
        self.assertEqual(cfg.get("foo"), "one")
        self.assertEqual(cfg.get("ping"), "two")

    def test_dict(self):
        cfg = Config()
        cfg.set("foo", "bar")
        cfg.set("ping", "pong")
        self.assertEqual(cfg.dict, {"foo":"bar", "ping":"pong"})

    def test_copy(self):
        cfg_from = Config()
        cfg_to = Config()
        cfg_from.set("foo", "bar")
        cfg_from.set("ping", "pong")
        cfg_to.copy("foo", cfg_from, "ERROR")
        cfg_to.copy("ping", cfg_from, "ERROR")
        cfg_to.copy("see", cfg_from, "saw")
        self.assertEqual(cfg_to.get("foo"), "bar")
        self.assertEqual(cfg_to.get("ping"), "pong")
        self.assertEqual(cfg_to.get("see"), "saw")


if __name__ == '__main__':
    unittest.main()