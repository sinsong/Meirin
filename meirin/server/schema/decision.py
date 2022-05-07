from pydantic import BaseModel

from meirin.concept import Decision

class DecisionSchema(BaseModel):
    """访问控制结果
    """
    decision :Decision
