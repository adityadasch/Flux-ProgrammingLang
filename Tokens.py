from dataclasses import dataclass
from collection import TokenType,CollectionType

@dataclass
class Token:
    type: TokenType
    value: str = None
    collection: CollectionType = None
    def __repr__(self):
        return f'Token<{self.type}, {self.value}>' if self.value else f'Token<{self.type}>'
