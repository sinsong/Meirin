from typing import Any, Optional, List

from fastapi import APIRouter, Query, Path, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from meirin.db.policy import Policy

from meirin.server import dep
from meirin.server.utils import orm_to_dict
from meirin.server.schema.policy import PolicySchema, PolicyInput

router = APIRouter()

@router.get("/")
def enum_policy(    
    offset :int = Query(0, title="Query Start", description="expect start"),
    limit  :int = Query(10, title="Query Size", description="expect number"),
    order  :str = Query("id", title="Query order", description="expect order"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> List[PolicySchema]:
    # map() helper
    def transform(orm_obj :Policy):
        return PolicySchema.parse_obj(orm_to_dict(orm_obj))

    query_and_map = map(
        transform,
        db.query(Policy)
          .order_by(Policy.id)
          .offset(offset)
          .limit(limit)
          .all()
    )
    return list(query_and_map)

@router.get("/{id:int}")
def query_policy(
    id :int = Path(..., title="Policy ID", description="Identifier of Policy"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> Policy:
    try:
        db_result = db.query(Policy).filter(Policy.id == id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Special policy not found")

    result = PolicySchema.parse_obj(orm_to_dict(db_result))
    return result

@router.post("/")
def insert_policy(
    input :PolicyInput,

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> PolicySchema:
    db_obj = Policy(**input.dict())

    db.add(db_obj)

    try:
        db.commit()
        db.refresh(db_obj)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"策略组指定的元策略 #{input.group} 不存在。")

    return PolicySchema.parse_obj(orm_to_dict(db_obj))
# TODO: PUT /

@router.delete("/{id:int}")
def delete_policy(
    id :int = Path(..., title="Policy ID", description="Identifier of Policy"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
):
    try:
        db_result = db.query(Policy).filter(Policy.id == id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Special policy not found")

    # 不需要检查完整性
    db.delete(db_result)
    db.commit()

@router.patch("/{id:int}")
def patch_policy(
    input :PolicyInput,
    id :int = Path(..., title="Policy ID", description="Identifier of Policy"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> PolicySchema:
    try:
        db_result :Policy = db.query(Policy).filter(Policy.id == id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Special policy not found")

    update_data = input.dict(exclude_unset=True)

    for field in update_data:
        setattr(db_result, field, update_data[field])

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return PolicySchema.parse_obj(orm_to_dict(db_result))

# count

@router.get("/count")
def count_policy(
    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> int:
    count = db.query(func.count(Policy.id)).scalar()
    return count
