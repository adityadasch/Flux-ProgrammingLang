from Lexer import Lexer
import parser
from collection import __global__
from writer import close

text = '''
var x: int = 5;
var y: int = 10;
var z: int = x + y;
'''

tok = Lexer(text).generate_tokens()
tok = Lexer.chop(tok)
ast = parser.Parser.parse(tok)
for tree in ast:
    tree.execute()

print(__global__)

close()