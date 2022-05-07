from typing import Any, Optional, List

from fastapi import APIRouter, Query, Path, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound

from meirin.db.metapolicy import MetaPolicy

from meirin.server import dep
from meirin.server.utils import orm_to_dict
from meirin.server.schema.metapolicy import MetaPolicySchema, MetaPolicyInput

router = APIRouter()

@router.get("/")
def enum_metapolicy(
    offset :int = Query(0, title="Query Start", description="expect start"),
    limit  :int = Query(10, title="Query Size", description="expect number"),
    # TODO: ORDER BY `time` 添加 create_time 字段
    order  :str = Query("id", title="Query order", description="expect order"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> List[MetaPolicySchema]:
    # map() helper
    def transform(orm_obj :MetaPolicy):
        return MetaPolicySchema.parse_obj(orm_to_dict(orm_obj))

    query_and_map = map(
        transform,
        db.query(MetaPolicy)
          .order_by(MetaPolicy.id)
          .offset(offset)
          .limit(limit)
          .all()
    )
    return list(query_and_map)

@router.get("/{id:int}")
def query_metapolicy(
    id :int = Path(None, title="Metapolicy ID", description="Identifier of Metapolicy"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> MetaPolicySchema:
    try:
        db_result = db.query(MetaPolicy).filter(MetaPolicy.id == id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Special metapolicy not found")

    result = MetaPolicySchema.parse_obj(orm_to_dict(db_result))
    return result

@router.post("/")
def insert_metapolicy(
    input :MetaPolicyInput,

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> MetaPolicySchema:
    db_obj = MetaPolicy(**input.dict())

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return MetaPolicySchema.parse_obj(orm_to_dict(db_obj))
# TODO: PUT /

@router.delete("/{id:int}")
def delete_metapolicy(
    id :int = Path(..., title="Metapolicy ID", description="Identifier of Metapolicy"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
):
    try:
        db_result = db.query(MetaPolicy).filter(MetaPolicy.id == id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Special metapolicy not found")

    db.delete(db_result)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"该元策略含有子策略，不可删除。")

@router.patch("/{id:int}")
def patch_metapolicy(
    input :MetaPolicyInput,
    id :int = Path(..., title="Metapolicy ID", description="Identifier of Metapolicy"),

    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
):
    try:
        db_result :MetaPolicy = db.query(MetaPolicy).filter(MetaPolicy.id == id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Special metapolicy not found")

    update_data = input.dict(exclude_unset=True)

    for field in update_data:
        setattr(db_result, field, update_data[field])

    db.add(db_result)
    db.commit()
    db.refresh(db_result)

    return MetaPolicySchema.parse_obj(orm_to_dict(db_result))

# count

@router.get("/count")
def count_metapolicy(
    db :Session = Depends(dep.db.get_db),
    credential :None = Depends(dep.credential.meirin_credential)
) -> int:
    count = db.query(func.count(MetaPolicy.id)).scalar()
    return count
