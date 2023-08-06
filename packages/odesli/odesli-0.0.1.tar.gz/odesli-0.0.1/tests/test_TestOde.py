import unittest

from odesli.Odesli import Odesli

class TestOde(unittest.TestCase):

    def test_isupper(self):
        o = Odesli()
        e = o.getByUrl('https://www.youtube.com/watch?v=GYDTcCf0xvw')
        self.assertTrue('FOO'.isupper())

if __name__ == '__main__':
    unittest.main()
