## 概念

ABAC 基本概念

|Concept                |概念                        |解释                  |
|:----------------------|:---------------------------|:---------------------|
|`subject`              |**主体**：人类用户或非人类实体|发起访问的实体          |
|`object`               |**客体**：对象、资源         |被保护的资源或实体      |
|`policy`               |**策略**：规则、关系         |决定访问请求是否被允许  |
|`environment condition`|环境条件                    |访问请求相关的环境上下文 |

attribute 属性：主体、客体、环境的特征。

|symbol |mean                    |含义         |
|:------|:-----------------------|:------------|
| `PEP` |Policy Decision Point   |策略决策点    |
| `PEP` |Policy Enforcement Point|策略强制执行点|

enforce: （强制）执行

决策结果

| term            | 含义                     |
|:----------------|:-------------------------|
| `permit`        | 允许                     |
| `deny`          | 拒绝                     |
| `indeterminate` | 不确定；无法做出决定      |
| `notapplicable` | 没有应用；没匹配到任何策略 |

## 场景

1. subject 请求访问 object
2. 访问控制系统评估
  - 规则 rules
  - 主体属性 subject attributes
  - 客体属性 object attributes
  - 环境条件 environment conditions
3. 做出决策，如果授权则允许访问
