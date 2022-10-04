import io
from search_tests_helper import get_print
from unittest import TestCase, main
from unittest.mock import patch
import sys

@patch('builtins.input')
def test_all(answers, input_mock):
    print(get_print(input_mock, answers))

if __name__ == '__main__':
    keyword = input()
    option = int(input())
    none = [1, 3, 6]
    if option not in none:
        resp = input() if option != 2 else int(input())
        test_all([keyword, option, resp])
    else:
        test_all([keyword, option])
