import unittest

from lark import Tree, Token

from meirin.dsl.parser import parser

class TestParser(unittest.TestCase):
    def test_1(self):
        expr = '1 == 1'
        expect =Tree(('equ_expr'),[
            1,
            1
        ])
        self.assertEqual(parser.parse(expr), expect)

if __name__ == "__main__":
    unittest.main()

"true || false && (true && false)"

