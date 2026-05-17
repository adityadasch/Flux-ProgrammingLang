from typing import Tuple, Any

import parser
from collection import Datatype, Scope, __global__, __local__, Token
from writer import write

class Node:
    def __init__(self,value:str, children: Tuple['Node', 'Node']=None, parent: 'Node'=None):
        self.value = value
        self.children = children or ()

    def convert(self):
        """Convert the node's value to a different type, if necessary. (for children)"""
        pass
    def execute(self)->Any:
        """Execute the node's operation, if necessary. (for children)"""
        pass
    @property
    def left(self):
        return self.children[0]
    @property
    def right(self):
        return self.children[1]

class OpNode(Node):
    def __init__(self, children: Tuple['Node', 'Node']=None, value:str=''):
        super().__init__(value, children)
    def __repr__(self):
        return f'{self.__class__.__name__}({self.left}, {self.right})'

class FlexibleNode(Node):
    def __init__(self,value:str, children: Tuple['Node', 'Node']=None, scope: Scope= None):
        super().__init__('', children)
        self.value = value
        self.scope= scope
    def execute(self):
        value, dtenum = self.scope.variables.get(self.value)
        match dtenum:
            case Datatype.NUMBER:
                return NumNode(value).execute()
            case Datatype.STRING:
                return StrNode(value).execute()
            case Datatype.FLOAT:
                return FltNode(value).execute()
            case Datatype.BOOLEAN:
                return BoolNode(value).execute()
        return None

    def __repr__(self):
        return f'FlexibleNode({self.value})'

class AddNode(OpNode):
    def __init__(self, children: Tuple['Node', 'Node']=None):
        super().__init__(children)
    def execute(self):
        return self.left.execute() + self.right.execute()

class SubNode(OpNode):
    def __init__(self, children: Tuple['Node', 'Node']=None):
        super().__init__(children)
    def execute(self):
        return self.left.execute() - self.right.execute()

class MulNode(OpNode):
    def __init__(self, children: Tuple['Node', 'Node']=None):
        super().__init__(children)
    def execute(self):
        return self.left.execute() * self.right.execute()

class DivNode(OpNode):
    def __init__(self,value:str = '/', children: Tuple['Node', 'Node']=None):
        super().__init__(children)
        self.value = value
    def execute(self):
        match self.value:
            case '/':
                return self.left.execute() / self.right.execute()
            case '//':
                return self.left.execute() // self.right.execute()
            case '%':
                return self.left.execute() % self.right.execute()
        return None

class PowNode(OpNode):
    def __init__(self, children: Tuple['Node', 'Node']=None):
        super().__init__(children)
    def execute(self):
        return self.left.execute() ** self.right.execute()

class AssignNode(OpNode):
    def __init__(self, children: Tuple['Node', 'Node']=None, dtype:Datatype= Datatype.STRING):
        super().__init__(children)
        self.dtype = dtype
    def execute(self):
        name = self.left.value
        value = self.right.execute()
        __local__.assign(name, value, self.dtype)

        write("ASSIGN "+name+" "+str(value)+" "+str(self.dtype))
    def __repr__(self):
        return f'AssignNode({self.left}, {self.right})'

class RPNNode(OpNode):
    def __init__(self, value):
        super().__init__(value= value)
    def execute(self):
        stack = []

        for token in self.value.split():
            if token.isalnum():
                stack.append(token)
            else:
                op2 = stack.pop()
                op2 = __local__.variables.get(op2, (None, None))[0] if op2.isalpha() else float(
                    op2) if '.' in op2 else int(op2)

                op1 = stack.pop()
                op1 = __local__.variables.get(op1, (None, None))[0] if op1.isalpha() else float(
                    op1) if '.' in op1 else int(op1)

                append_ = lambda x: stack.append(str(x))
                match token:
                    case '+':
                        append_(op1 + op2)
                    case '-':
                        append_(op1 - op2)
                    case '*':
                        append_(op1 * op2)
                    case '/':
                        append_(op1 / op2)
                    case '^':
                        append_(op1 ** op2)

        return float(stack[0]) if '.' in stack[0] else int(stack[0]) if stack[0].isdigit() else stack[0]

    def __repr__(self):
        return f'RPNNode({self.value})'

class FuncNode(Node):
    def __init__(self, value:str):
        super().__init__(value)
    def execute(self):
        pass
    def __repr__(self):
        return f'FuncNode(name={self.value}, {self.children})'

class PrntNode(FuncNode):
    def __init__(self, arg: Node):
        super().__init__('print')
        self.display = arg
    def execute(self):
        print(self.display.execute())

    def __repr__(self):
        return f'PrntNode({self.display})'

class DtNode(Node):
    def __init__(self, value:str):
        super().__init__(value)
    def execute(self):
        return self.convert()
    def convert(self):pass
    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    @staticmethod
    def validate(value)->bool:
        """
        :param value: The value to validate.
        :return: bool: True if the value is valid for this datatype, False otherwise.
        """
        pass

class NumNode(DtNode):
    def __init__(self, value:str):
        super().__init__(value)
    def convert(self)->int:
        return int(self.value)
    @staticmethod
    def validate(value)->bool:
        try:
            int(value)
            return True
        except ValueError:
            return False

class StrNode(DtNode):
    def __init__(self, value:str):
        super().__init__(value)
    def convert(self)->str:
        return str(self.value)
    @staticmethod
    def validate(value)->bool:
        return isinstance(value, str)

class FltNode(DtNode):
    def __init__(self, value:str):
        super().__init__(value)
    def convert(self)->float:
        return float(self.value)

class BoolNode(DtNode):
    def __init__(self, value:str):
        super().__init__(value)
    def convert(self)->bool:
        return self.value.lower() in ['true', '1']

def RPN(value: Tuple[Token, ...]):
    opstack = []
    output = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    for token in value:
        tok_val = token.value

        if tok_val.isalnum():
            output.append(tok_val)
        elif tok_val == '(':
            opstack.append(tok_val)
        elif tok_val == ')':
            while opstack and opstack[-1] != '(':
                output.append(opstack.pop())
            opstack.pop()  # Pop the '(' from the stack
        elif tok_val in precedence:
            while opstack and precedence.get(opstack[-1], 0) >= precedence[tok_val]:
                output.append(opstack.pop())
            opstack.append(tok_val)
    while opstack:
        output.append(opstack.pop())

    return RPNNode(' '.join(output))