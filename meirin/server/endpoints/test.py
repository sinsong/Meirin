from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Body
from lark.exceptions import LarkError

from meirin.dsl import expression_test
from meirin.server import dep

router = APIRouter()

@router.post("/expression")
def test_expression(
    expression :str = Body(None),

    credential :None = Depends(dep.credential.meirin_credential)
) -> Any:
    try:
        return expression_test(expression)
    except LarkError as e:
        return str(e)
