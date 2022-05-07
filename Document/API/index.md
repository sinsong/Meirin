## 全局说明

```
base: /v1/
```

## 授权 authorization

```
# 强制执行
GET    /enforce
```

## 策略管理 (需要管理员权限)

```
# 策略查询
GET    /policy       # 枚举
GET    /policy/{id}  # 详细信息

# 策略添加
POST   /policy
PUT    /policy

# 策略删除
DELETE /policy/{id}

# 策略修改
PATCH  /policy/{id}
```

## 错误

与 PDP 做出的决策无关，与系统的对接和使用有关的错误。

### 未认证

```
401 Unauthorized
# no body
```

## 资源 (需要管理员权限)

```
GET    subject/:id 主体
GET    object/:id  客体
GET    policy/:id  策略
```

## 认证和使用

需要配置 `apikey`

```
提供 apikey:
    返回结果
不提供 apikey:
    中断连接
```
