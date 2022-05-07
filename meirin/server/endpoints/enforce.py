from typing import List
from logging import getLogger
from time import time

from fastapi import APIRouter, Depends, Header, HTTPException, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel

from meirin.concept import Context, Decision, parseDecision
from meirin.deduction import decision
from meirin.dsl import evaluate
from meirin.db.metapolicy import MetaPolicy
from meirin.db.policy import Policy

from meirin.server import dep
from meirin.server.schema.decision import DecisionSchema

router = APIRouter()
logger = getLogger(__name__)

class ACRequest(BaseModel):
    subject     :dict
    object      :dict
    action      :dict
    environment :dict

# Context helper
class RequestContext(Context):
    def __init__(self, subject, object, action, environment):
        self._subject = subject
        self._object = object
        self._action = action
        self._environment = environment

    @property
    def subject(self):
        return self._subject

    @property
    def object(self):
        return self._object

    @property
    def action(self):
        return self._action

    @property
    def environment(self):
        return self._environment

@router.post("/enforce")
def enforce(
    request :ACRequest = Body(None, title="Access Control Request", description="Request informations input to AC system."),
    
    db :Session = Depends(dep.db.get_db)
) -> DecisionSchema:
    # prepare context
    environment = {
        "time": time(),
    }
    context = RequestContext(request.subject, request.object, request.action, request.environment.update(environment))

    # 先匹配 MetaPolicy 确定 Policy 组和决议模式

    metapolicies :List[MetaPolicy]= db.query(MetaPolicy).all()

    if len(metapolicies) == 0:
        return DecisionSchema(decision=Decision.NOTAPPLICABLE)

    matched_metapolicy = []
    for metapolicy in metapolicies:
        # TODO: 重命名为 matchMetaPolicy
        match_result = evaluate(context, metapolicy.match)
        if match_result == True:
            matched_metapolicy.append(metapolicy)
            logger.debug(f"match metapolicy: `{metapolicy!r}`")
    
    if len(matched_metapolicy) < 1:
        return DecisionSchema(decision=Decision.NOTAPPLICABLE)
    elif len(matched_metapolicy) > 1:
        return DecisionSchema(decision=Decision.INDETERMINATE)

    # 应用 Policy，评估表达式

    policy_group_id = matched_metapolicy[0].id
    decision_mode = matched_metapolicy[0].mode
    decision_set = []

    policies = db.query(Policy).filter(Policy.group == policy_group_id).all()

    if len(policies) == 0:
        return DecisionSchema(decision=Decision.NOTAPPLICABLE)

    for policy in policies:
        # TODO: 改为 context -> policy -> Decision
        policy_result = evaluate(context, policy.match)
        if policy_result == True:
            # TODO: parseDecison 可能抛出异常
            decision_set.append(parseDecision(policy.effect))

    # 合并 decision_set
    try:
        enforce_decision = decision(decision_mode, decision_set)
    except RuntimeError:
        return DecisionSchema(decision=Decision.INDETERMINATE)

    return DecisionSchema(decision=enforce_decision)
