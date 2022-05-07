from typing import List

from meirin.concept import Decision

# 这里实现合并算法
# http://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html#_Toc325047268

def deny_overrides(decisions :List[Decision]) -> Decision:
    """Deny-overrides

    1. 含有 deny 则直接决策为 deny (override 的含义)
    2. 不含 deny 情况下，存在 permit 则决策为 permit
    3. 不含有 permit deny 决策，则决策为 notapplicable
    """
    havePermit = False

    for decision in decisions:
        if decision == Decision.DENY:
            return Decision.DENY
        if decision == Decision.PERMIT:
            havePermit = True
            continue
    
    if havePermit:
        return Decision.PERMIT
    
    return Decision.NOTAPPLICABLE

def permit_overrides(decisions :List[Decision]) -> Decision:
    """Permit-overrides

    1. 含义 permit 则直接 permit (override 的含义)
    2. 不含 permit 情况下，存在 deny 则决策为 deny
    3. 不含有 permit deny 决策，则决策为 notapplicable
    """
    haveDeny = False
    
    for decision in decisions:
        if decision == Decision.DENY:
            haveDeny = True
            continue
        if decision == Decision.PERMIT:
            return Decision.PERMIT
    
    if haveDeny:
        return Decision.DENY

    return Decision.NOTAPPLICABLE

def deny_unless_permit(decisions :List[Decision]) -> Decision:
    """Deny-unless-permit

    1. permit 优先于 deny
    2. 不做出 indeterminate 或 notapplicable 决策；做出确定性 permit 或 deny 决策。

    行为：
    1. 决策集合含有 permit 则做出 permit 决策
    2. 否则，做出 deny 决策
    """
    for decision in decisions:
        if decision == Decision.PERMIT:
            return Decision.PERMIT
    return Decision.DENY

def permit_unless_deny(decisions :List[Decision]) -> Decision:
    """Permit-unless-deny
    1. deny 优先于 permit
    2. 不做出 indeterminate 或 notapplicable 决策；做出确定性 permit 或 deny 决策。

    行为：
    1. 决策集合含有 deny 则做出 deny juece
    2. 否则，做出 permit 决策
    """
    for decision in decisions:
        if decision == Decision.DENY:
            return Decision.DENY
    return Decision.PERMIT

# 使用 mode 属性 dispatch 到各个算法

def decision(mode :str, decisions :List[Decision]) -> Decision:
    """做出决策

    可用的决策模式有：
    1. deny-overrides
    2. permit-overrides
    3. deny-unless-permit
    4. permit-unless-deny
    """
    if   mode == "deny-overrides":
        return deny_overrides(decisions)
    elif mode == "permit-overrides":
        return permit_overrides(decisions)
    elif mode == "deny-unless-permit":
        return deny_unless_permit(decisions)
    elif mode == "permit-unless-deny":
        return permit_unless_deny(decisions)
    else:
        raise RuntimeError(f"unexpect mode `{mode}`")
