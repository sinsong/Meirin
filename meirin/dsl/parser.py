from typing import List, Any
import pkgutil
from dataclasses import dataclass
from lark import Lark, Transformer, Token, Tree, ParseError

# AST 对象

@dataclass
class GetMem():
    obj :str
    mem :str

@dataclass
class Call():
    designator :str
    arguments :List[Any]

# tree[0] -> tree 的 children 的访问
# 返回 Token 或者别的啥 Token 有 value 属性

class ASTTransformer(Transformer):

    # constant expressions

    def number_constant(self, tree):
        num = tree[0].value
        parsed_num = int(num)
        return Tree('number', [parsed_num])

    def true_constant(self, tree):
        return Tree('bool', [True])

    def false_constant(self, tree):
        return Tree('bool', [False])

    def string_literal(self, tree):
        return Tree('string_literal', [tree[0].value[1:-1]])

    # handle getmem

    def getmem_expr(self, tree):
        obj = tree[0].children[0].value
        mem = tree[1].children[0].value

        # print("GETMEM {} {}".format(obj, mem))

        # error with `subject.id.help``
        if isinstance(obj, GetMem):
            raise ParseError("refuse nested getmem")

        if not (obj == 'subject' or obj == 'object' or obj == 'action' or obj == 'environment'):
            raise ParseError("only permit access `subject`, `object`, `action`, `environment`")

        return Tree('getmem', [GetMem(obj, mem)])

    def call_expr(self, tree):
        function_designator = tree[0].children[0].value

        def token_transform(tree):
            return tree.children[0]
        function_arguments = list(map(token_transform, tree[1].children))

        return Tree('call', [Call(function_designator, function_arguments)])

# grammar text
# https://stackoverflow.com/a/58941536
grammar = str(pkgutil.get_data(__name__, "meirin-dsl.lark"), encoding='utf8')

# 解析器
parser = Lark(grammar,
    start = "expr",
    parser = "lalr",
    transformer=ASTTransformer()
)
