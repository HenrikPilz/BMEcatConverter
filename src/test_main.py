import os
import test
import unittest


def tests():
    if not os.path.exists("../test_data"):
        os.makedirs(os.path.join(os.path.dirname(__file__), "../test_data"), exist_ok=True)
    unittest.main(test)


# if __name__ == '__main__':
# Datenmodultests
tests()
