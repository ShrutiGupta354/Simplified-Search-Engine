import re
import unittest

below = "TESTS BELOW"
filename = 'search_tests.py'

def function_count(func):
  count = 0

  with open(filename, 'r') as f:
    lines = f.readlines()
    student_code = False
    for line in lines:
      if student_code:
        if bool(re.search('assert ' + func, line)):
          count += 1
      elif below.lower() in line.lower():
        student_code = True
  return count

class CheckTests(unittest.TestCase):

  def test_function_count(self):
    function = input()
    required = input()
    count = function_count(function)
    print("Function tested: {}".format(function))
    print("Required number of tests: {}".format(required))
    print("Found number of tests: {}".format(count if count else 0))
    print("OK" if count >= int(required) else "Not enough tests")

if __name__ == '__main__':
    unittest.main()
