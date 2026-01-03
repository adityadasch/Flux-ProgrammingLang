import Tokens
from Error import SyntaxError, raise_
from Tokens import *

class Lexer:
    def __init__(self):
        self.char: str = ''
        self.code: str = None
        self.index: int = -1
        self.tokens: list[Token] = list()
        self.basic_characters = {'\n':NEWLINE, '\t': TAB,
                            '=': EQUAL, '+': PLUS, '-': MINUS, '*': MUL, '^':'CARAT',
                            '/': DIV, '#':HASH, '%':MOD, '&':AND, '|': OR, '!': NOT,
                            '(': LEFT_PAREN, ')': RIGHT_PAREN, '[': LEFT_BRACE, ']': RIGHT_BRACE,
                            '{': LEFT_SET, '}': RIGHT_SET, ':': COLON, ';': END, '$':VARIABLE,'@':LABEL,
                            '>': GREATER, '<': LESSER
                            }
        self.alpha = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper()
        self.numeric = '0123456789'
        self.alpha_numeric = set(self.alpha + self.numeric + '_')
        self.alpha = set(self.alpha)
        self.numeric = set(self.numeric)

    def advance(self):
        self.index += 1 if self.index < len(self.code) else 0
        self.char = self.code[self.index] if self.index < len(self.code) else None

    def generate_tokens(self, code: str) -> list[Token]:
        # ---------------- Variables---------------------
        self.tokens = []
        self.code = code.replace('    ', '\t')

        # ---------------- Looping---------------------
        self.advance()
        while self.char:
            match self.char:
                case char if char in self.basic_characters:
                    self.tokens.append(Token(self.basic_characters.get(self.char)))
                case '"' | "'":
                    end = self.code.find('"' if self.char == '"' else "'", self.index+1)
                    if end == -1:
                        raise_(SyntaxError('Console','1',f'Missing quotation({self.char}) mark', code))
                    self.tokens.append(Token(type_= STRING, value= self.code[self.index+1:end]))
                    self.index = end
                case char if char in self.alpha:
                    start = self.index
                    while self.char and self.char in self.alpha_numeric:
                        self.advance()
                    self.tokens.append(Token(type_=IDENTIFIER, value = code[start:self.index]))
                    self.index -= 1
                case char if char in self.numeric:
                    start = self.index
                    dot_count = 0
                    while self.char and (self.char in self.numeric or self.char == '.'):
                        if self.char == '.':
                            dot_count += 1
                            if dot_count > 1:
                                raise_(SyntaxError('Console','1',f'Invalid float format; Double floating point is not allowed', code))
                        self.advance()
                    token_type = FLOAT if dot_count == 1 else INTEGER
                    self.tokens.append(Token(type_=token_type, value=code[start:self.index]))
                    self.index -= 1
            self.advance()

        return Lexer.compress(self.tokens)

    @staticmethod
    def compress(tokens:list[Token]):
        def make_replacer(new_type):
            return lambda tokens, idx, pop_tok: (
                pop_tok.append(idx),
                setattr(tokens[idx - 1], "type", new_type)
            )

        replacers = {
            Tokens.EQUAL: make_replacer(Tokens.DEQUAL),
            Tokens.GREATER: make_replacer(Tokens.GEQUAL),
            Tokens.LESSER: make_replacer(Tokens.LEQUAL),
            Tokens.COLON: make_replacer(Tokens.REASSIGN),
            Tokens.NOT: make_replacer(Tokens.NEQUAL),
        }

        pop_tok = []
        for index, token in enumerate(tokens):
            if token.type == Tokens.EQUAL and index > 0:
                prev_type = tokens[index - 1].type
                if prev_type in replacers:
                    replacers[prev_type](tokens, index, pop_tok)

            if token.type == Tokens.PLUS and index > 0:
                if tokens[index - 1].type == Tokens.PLUS:
                    pop_tok.append(index)
                    tokens[index - 1].type = Tokens.INCREMENT
            if token.type == Tokens.MINUS and index > 0:
                if tokens[index - 1].type == Tokens.MINUS:
                    pop_tok.append(index)
                    tokens[index - 1].type = Tokens.DECREMENT

        for p in pop_tok[::-1]:
            tokens.pop(p)
        return tokens