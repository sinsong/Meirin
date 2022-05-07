## 顶层

策略

```yaml
id: 1
name: example policy
group: policy group (search name -> store id)

match: {}
effect: permit | deny
```

元策略 + 策略组

```yaml
id: 1 # groupid
name: metapolicy

match: {}
mode: ... # 合并算法 & PDP 模式
```

## match

```yaml
match: # 内部同时满足
  <help name>: expr # 表达式
  ...
```

## 表达式

### 内置对象

```
subject
object
action
environment
```

### 操作

```
<object>.attributeName 属性访问
funcname() 函数调用
&& || 逻辑组合
```
