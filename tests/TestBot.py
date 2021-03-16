import unittest
import bot
from unittest.mock import patch
from datetime import datetime

class TestBot(unittest.TestCase):
    # def test_next_day(self):
    #     self.assertEqual(bot.next_day(0), 6)

    def test_day_name_to_num(self):
        self.assertEqual(bot.day_name_to_num('Monday'), 0)
        self.assertEqual(bot.day_name_to_num('thursday'), 3)