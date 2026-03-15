from Tokens import Token
from collection import Dictionary,CollectionType, TokenType

class Lexer:
    def __init__(self, code:str):
        self.input = None
        self.position = None
        self.read_position = None
        self.ch = None
        self.token: list[Token] = []

        self.reset(code)

    def reset(self, code: str):
        self.input = code
        self.position = 0
        self.read_position = 0
        self.ch = ''

        self.token: list[Token] = []

        self.read_next_char()

    def read_next_char(self):
        if self.read_position >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def read_next_char_peek(self):
        if self.read_position >= len(self.input):
            return None
        else:
            return self.input[self.read_position]

    def generate_tokens(self):
        # Implement tokenization logic here
        while self.ch is not None:
            if self.ch == '#':
                break
            if self.ch in ' \t\n\r':
                self.read_next_char()
                continue
            elif self.ch in Dictionary.symbols:
                token_type = Dictionary.symbols[self.ch]
                self.token.append(Token(token_type))
            elif self.ch.isalpha():
                identifier = self.read_identifier()
                self.token.append(Token(TokenType.IDENTIFIER, identifier))
                continue
            elif self.ch.isdigit():
                number = self.read_number()
                self.token.append(Token(TokenType.NUMBER, number, CollectionType.NUMBER))
                continue

            self.read_next_char()

    def read_identifier(self) -> str:
        """Reads an identifier and returns it as a string."""
        start_position = self.position
        while self.ch is not None and (self.ch.isalnum() or self.ch == '_'):
            self.read_next_char()
        return self.input[start_position:self.position]

    def read_number(self) -> (str, bool):
        """Returns the number as a string."""
        start_position = self.position
        while self.ch is not None and (self.ch.isdigit() or self.ch in ('f','F','d','D','.','e','E')):
            self.read_next_char()
            if self.ch in ('+','-'):
                if self.input[self.position-1] in ('e','E'):
                    self.read_next_char()
                else:
                    break
        return self.input[start_position:self.position]

lex = Lexer(input(">"))
lex.generate_tokens()
print(lex.token)