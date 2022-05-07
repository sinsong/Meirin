import sys
from pprint import pprint
from meirin.dsl import parser
from meirin.dsl.executor import Executor

if len(sys.argv) < 2:
    print("need argument", file=sys.stderr)

tree = parser.parse(sys.argv[1])
print(tree.pretty()) # '|-->'
#print(tree)

# xxx.get
# xxx.update
class Context:
    @property
    def subject(self):
        return {
            'id': 1
        }
    def object(self):
        return {
            'id': 1
        }
    def action(self):
        return {
            value: 'read'
        }
    def environment(self):
        return {
            time: '2022-04-17T12:00Z+08'
        }

print("===== Executor =====")

try:
    context = Context()
    result = Executor(context).transform(tree)
    print('=>', result)
except Exception as e:
    print(e)
