import inspect
from typing import Tuple, Any
from collection import Dictionary, CollectionType, TokenType, Token, Datatype
from tree_parser_test import (Node, AddNode, SubNode, MulNode, DivNode, PowNode,
                              AssignNode, RPN, PrntNode, __local__)  # Importing operation nodes for parsing expressions
from tree_parser_test import FlexibleNode, StrNode, BoolNode, NumNode, FltNode # Importing nodes for handling different data types

class Parser:
    @staticmethod
    def parse(tokens: Tuple[Tuple[Token, ...],...])-> tuple[Any, ...] | None:
        ast = []
        for each in tokens:
            if each[-1].type != TokenType.SEMICOLON:
                # Handle missing semicolon error
                print("Error: Expected ';' at the end of the statement")
                return None

            ast.append(Parser.parse_(each))
        return tuple(ast)

    @staticmethod
    def ret_type(token: Token):
        if token.type == TokenType.NUMBER:
            return FltNode(token.value) if '.' in token.value else NumNode(token.value)
        elif token.type == TokenType.STRING:
            return StrNode(token.value)
        elif token.type == TokenType.BOOLEAN:
            return BoolNode(str(token.value == 'true'))
        elif token.type == TokenType.IDENTIFIER:
            return FlexibleNode(token.value, scope=__local__)
        else:
            # Handle invalid single token error
            print(f"Error: Invalid single token '{token.value}'")
            return None

    @staticmethod
    def parse_(tokens: Tuple[Token, ...]):
        # Implement parsing logic here
        position = 0

        while position < len(tokens):
            token = tokens[position]
            is_keyword = token.type == TokenType.KEYWORD

            if token.type == TokenType.SEMICOLON:
                position+=1
                continue

            if is_keyword and token.value == 'var' and position + 4 < len(tokens):
                'var name: dt = value'
                datatype = tokens[position + 3].value
                identifier = tokens[position+1].value

                if tokens[position+2].type != TokenType.COLON:
                    # Handle missing datatype error
                    print(f"Error: Expected \':\' after '{identifier}'")
                if datatype not in Dictionary.dtypes:
                    # Handle invalid datatype error
                    print(f"Error: Invalid datatype '{datatype}'")

                elif tokens[position+4].type not in (TokenType.EQUAL,TokenType.SEMICOLON):
                    # Handle missing equal sign error
                    print("Error: Expected '=' or '; after variable name")

                if tokens[position+4].type == TokenType.SEMICOLON:
                    # Implement variable declaration without initialization
                    pass
                dtype = Datatype.STRING if datatype == 'string' else \
                        Datatype.BOOLEAN if datatype == 'bool' else \
                        Datatype.FLOAT if datatype == 'float' else \
                        Datatype.NUMBER

                value = tokens[position + 5:-1]
                rhs = Parser.parse_(value) if dtype != Datatype.STRING else StrNode(tokens[position + 5].value) if tokens[position + 5].type == TokenType.STRING else None
                return AssignNode((StrNode(identifier),rhs), dtype=dtype)

            elif len(tokens) == 2:
                Parser.ret_type(token)

            elif is_keyword and token.value == 'pull' and position + 1 <= len(tokens):
                if position+1 == len(tokens):
                    # Handle missing data
                    return PrntNode(StrNode(''))

                elif position+1 == len(tokens)-1:
                    return PrntNode(Parser.ret_type(tokens[position+1]))



                return PrntNode(RPN(tokens[position+1:-1]))

            else:
                DEBUG = tokens[::-1]
                return RPN(DEBUG)

            position+=1
        return None


# from Tokens import Token
# from collection import Dictionary, CollectionType, TokenType, ParserTree
#
#
# class Parser:
#     position = 0
#     parse_tree = ParserTree()
#
#     @classmethod
#     def parse(cls, tokens: list[Token]):
#         # Implement parsing logic here
#         while cls.position < len(tokens):
#             token = tokens[cls.position]
#             if tokens[-1].type != TokenType.SEMICOLON:
#                 # Handle missing semicolon error
#                 print("Error: Expected ';' at the end of the statement")
#
#             is_keyword = token.type == TokenType.KEYWORD
#
#             if is_keyword and token.value == 'var':
#                 datatype = tokens[cls.position+1].value
#                 if datatype not in ['int', 'float', 'string', 'bool']:
#                     # Handle invalid datatype error
#                     print(f"Error: Invalid datatype '{datatype}'")
#                 elif tokens[cls.position+2].type != TokenType.IDENTIFIER:
#                     # Handle missing variable name error
#                     print("Error: Expected variable name after datatype")
#                 elif tokens[cls.position+3].type != TokenType.EQUAL and tokens[cls.position+3].type != TokenType.SEMICOLON:
#                     # Handle missing equal sign error
#                     print("Error: Expected '=' or '; after variable name")
#                 elif tokens[cls.position+4].type not in [TokenType.NUMBER, TokenType.STRING, TokenType.BOOLEAN] and \
#                         tokens[cls.position+3].type == TokenType.EQUAL:
#                     # Handle invalid value error
#                     print("Error: Expected a valid value after '='")
#                 else:
#                     name = tokens[cls.position+2].value
#                     cls.parse_tree.add(
#                         ('VAR ' + name + ' ' + datatype + ' ' + tokens[cls.position+4].value) \
#                             if tokens[cls.position+3].type != TokenType.SEMICOLON else \
#                         ('DVAR ' + name + ' ' + datatype)
#                     )
#
#                 cls.position = cls.position + 5 if tokens[cls.position+3].type != TokenType.SEMICOLON else cls.position + 2
#
#             elif is_keyword and token.value == 'call':
#                 func_name = tokens[cls.position+1].value
#                 cls.parse_tree.add('CALL ' + func_name)
#                 cls.position += 1
#
#             elif is_keyword and token.value == 'return':
#                 cls.parse_tree.add(('RETURN'+ ' ' + tokens[cls.position+1].value) if tokens[cls.position+1].type in [TokenType.IDENTIFIER, TokenType.NUMBER, TokenType.BOOLEAN]\
#                                                 else f'RETURNS {tokens[cls.position+1].value}' if tokens[cls.position+1].type == TokenType.STRING else 'RETURN')
#                 cls.position += 1
#
#             elif is_keyword and token.value == 'pull':
#                 if tokens[cls.position+1].type != TokenType.IDENTIFIER:
#                     # Handle missing variable name error
#                     print("Error: Expected variable name after 'pull'")
#
#                 var_name = tokens[cls.position+1].value
#                 cls.parse_tree.add('PULL ' + var_name)
#                 cls.position += 1
#
#             elif token.type == TokenType.IDENTIFIER or token.type == TokenType.NUMBER or token.type == TokenType.AMPERSAND:
#                 if token.type == TokenType.AMPERSAND:
#                     cls.parse_tree.add(
#                         'LOADR a'
#                     )
#                 else:
#                     cls.parse_tree.add('SET ' + token.value + ' a' if token.type == TokenType.NUMBER else \
#                                                     'LOADV ' + token.value + ' a')
#
#                 tok = tokens[cls.position + 2]
#                 if tok.type == TokenType.AMPERSAND:
#                     cls.parse_tree.add(
#                         'LOADR b'
#                     )
#                 else:
#                     cls.parse_tree.add('SET ' + tok.value + ' a' if tok.type == TokenType.NUMBER else \
#                                                     'LOADV ' + tok.value + ' b')
#
#                 match tokens[cls.position + 1].type:
#                     case TokenType.PLUS:
#                         cls.parse_tree.add('ADD')
#                     case TokenType.MINUS:
#                         cls.parse_tree.add('SUB')
#                     case TokenType.ASTERISK:
#                         cls.parse_tree.add('MUL')
#                     case TokenType.SLASH:
#                         cls.parse_tree.add('DIV')
#                     case TokenType.CARROT:
#                         cls.parse_tree.add('POW')
#                     case TokenType.DOUBLE_EQUAL:
#                         cls.parse_tree.add('EQ')
#                     case _:
#                         # Handle invalid operator error
#                         print(f"Error: Invalid operator '{tokens[cls.position + 1].value}'")
#
#                 cls.position += 2
#
#             cls.position += 1
#         print(cls.parse_tree.value)