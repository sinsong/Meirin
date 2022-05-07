from lark import Tree

from meirin.concept import Context

from .parser import parser
from .executor import Executor

def evaluate(context :Context, expression :str):
    """对表达式求值

    Parameters:
        context (Context): 求值上下文
        expression (str): 表达式

    Returns:
        求值结果
    """
    tree = parser.parse(expression)
    executor = Executor(context)

    # 结果
    result = executor.transform(tree)

    assert isinstance(result, Tree)
    return result.children[0]

def expression_test(expression :str):
    """表达式测试接口

    Parameters:
        expression (str): 表达式

    Returns:
        字符串形式的语法树

    :raises LarkError: 表达式解析失败时抛出该异常。

    TODO: ``ParserError`` and ``LexerError``
    """
    tree = parser.parse(expression)
    return tree.pretty()
