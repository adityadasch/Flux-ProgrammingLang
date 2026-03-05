from enum import  Enum
from typing import List, Optional

class CollectionType(Enum):
    NUMBER = 0
    IDENTIFIER = 1
    STRING = 2
    SYMBOL = 3

class TokenType(Enum):
    ILLEGAL = 0
    EOF = 1
    STRING = 2
    NUMBER = 3
    IDENTIFIER = 4
    BOOLEAN = 5
    EXCLAIM = 6
    AT = 7
    AMPERSAND = 8
    DOLLAR = 9
    SLASH = 10
    LEFT_PAREN = 11
    RIGHT_PAREN = 12
    LEFT_BRACE = 13
    RIGHT_BRACE = 14
    LEFT_CURLY = 15
    RIGHT_CURLY = 16
    COMMA = 17
    SEMICOLON = 18

    PLUS = 19
    MINUS = 20
    CARROT = 21
    ASTERISK = 22
    DOUBLE_DIVIDE = 23
    EQUAL = 24
    DOUBLE_EQUAL = 25
    NOT_EQUAL = 26
    LESS_THAN = 27
    LESS_THAN_OR_EQUAL = 28
    GREATER_THAN = 29
    GREATER_THAN_OR_EQUAL = 30
    QUOTES = 31
    DOUBLE_QUOTES = 32

    IGNORE = 33


class Dictionary:
    symbols = {'!': TokenType.EXCLAIM, '@': TokenType.AT, '&': TokenType.AMPERSAND, '$': TokenType.DOLLAR, '/': TokenType.SLASH, '(': TokenType.LEFT_PAREN, ')': TokenType.RIGHT_PAREN, '{': TokenType.LEFT_BRACE, '}': TokenType.RIGHT_BRACE, '[': TokenType.LEFT_CURLY, ']': TokenType.RIGHT_CURLY, ',': TokenType.COMMA, ';': TokenType.SEMICOLON, '+': TokenType.PLUS, '-': TokenType.MINUS, '^': TokenType.CARROT, '*': TokenType.ASTERISK, '=': TokenType.EQUAL, '<': TokenType.LESS_THAN, '>': TokenType.GREATER_THAN, '\'': TokenType.QUOTES, '\"': TokenType.DOUBLE_QUOTES}
