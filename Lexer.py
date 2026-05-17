from typing import Tuple
from collection import Dictionary,CollectionType, TokenType, Token

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

    def generate_tokens(self) -> list[Token]:
        # Implement tokenization logic here
        while self.ch is not None:
            if self.ch == '#':
                break
            if self.ch in ' \t\n\r':
                self.read_next_char()
                continue
            elif self.ch in Dictionary.symbols:
                token_type = Dictionary.symbols[self.ch]
                self.token.append(Token(token_type, self.ch, CollectionType.SYMBOL))
            elif self.ch.isalpha():
                identifier = self.read_identifier()
                if identifier in Dictionary.keywords:
                    self.token.append(Token(TokenType.KEYWORD, identifier))
                else:
                    self.token.append(Token(TokenType.IDENTIFIER, identifier))
                continue
            elif self.ch.isdigit():
                number = self.read_number()
                self.token.append(Token(TokenType.NUMBER, number, CollectionType.NUMBER))
                continue

            self.read_next_char()
        return self.compress(self.token)

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

    def compress(self, tokens: list[Token]) -> list[Token]:
        """Compresses consecutive tokens of the same type into a single token with a combined value."""
        if not tokens:
            return []

        compressed_tokens = [tokens[0]]
        inString = False
        quoteIndex = None

        for index, token in enumerate(tokens[1:]):
            if token.type == TokenType.QUOTES or token.type == TokenType.DOUBLE_QUOTES:
                inString = not inString
                if inString:
                    quoteIndex = len(compressed_tokens)
                else:
                    compressed_tokens[quoteIndex] = Token(TokenType.STRING, ''.join(t.value for t in compressed_tokens[quoteIndex:]), CollectionType.STRING)
                    compressed_tokens = compressed_tokens[:quoteIndex+1]
            else:
                if token.value is not None and token.value in ('true', 'false'):
                    token = Token(TokenType.BOOLEAN, token.value)
                compressed_tokens.append(token)
        return compressed_tokens


    @staticmethod
    def chop(tokens: list[Token]) -> Tuple[Tuple[Token,...], ...]:
        """Returns token list as a list with list of tokens between each semicolon."""
        chopped:list[tuple[Token,...]] = []
        current:list[Token] = []
        for token in tokens:
            if token.type == TokenType.SEMICOLON:
                current.append(token)
                chopped.append(tuple(current))
                current.clear()
            else:
                current.append(token)
        return tuple(chopped)