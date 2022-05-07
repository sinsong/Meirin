# `GET /policy` 策略查询

## 请求

查询参数
| key      | default | 解释 |
|:---------|:--------|:-----|
| `offset` | `0`     | 查询偏移 |
| `limit`  | `10`    | 返回个数 |
| `order`  | `time`  | 排序规则 |

## 响应

```json
[
    {
        "id": ...,
        "name": "",
        "group": "",
        "match": "",
        "effect": ""
    }
]
```
