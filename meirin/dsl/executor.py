from lark import Transformer, Tree
from .parser import GetMem, Call

class Executor(Transformer):

    def __init__(self, context):
        self.context = context
    
    # logical operator

    def or_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('or_expr', [lhs or rhs])

    def and_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('and_expr', [lhs and rhs])

    # equlity operator

    def equ_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('equ_expr', [lhs == rhs])

    def neq_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('neq_expr', [lhs != rhs])

    # relational operator

    def rela_lt_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('rela_lt_expr', [lhs < rhs])

    def rela_gt_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('rela_gt_expr', [lhs > rhs])

    def rela_lte_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('rela_lte_expr', [lhs <= rhs])

    def rela_gte_expr(self, tree):
        lhs = tree[0].children[0]
        rhs = tree[1].children[0]
        return Tree('rela_gte_expr', [lhs >= rhs])

    # unary operator

    def neg_expr(self, tree):
        opan = tree[0].children[0]
        return Tree('neg_expr', [not opan])

    # identifier

    # ASTTransformer 中是把带 identifier 的树转换成 getmem 的，所以要放这里
    def identifier(self, tree):
        raise RuntimeError('remove identifier support')

    # builtin functions

    def getmem(self, tree):
        # GetMem object
        getmem :GetMem= tree[0]

        # print(getmem.obj, getmem.mem)

        queue_object = self.context.__getattribute__(getmem.obj)

        # 查询成员是否存在，因为 get 会返回 NoneType
        if getmem.mem in queue_object:
            value = queue_object.get(getmem.mem)
        else:
            #raise ValueError("{}.{} not existed".format(getmem.obj, getmem.mem))
            return Tree('bool', [False])

        return Tree('getedmem', [value])

    def call(self, tree):
        callinfo :Call = tree[0]
        return tree
