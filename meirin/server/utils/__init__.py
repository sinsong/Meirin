from sqlalchemy import inspect

def orm_to_dict(obj):
    """将 SQLAlchemy ORM 对象转换为 dict

    Parameters:
        obj (Any): SQLAlchemy ORM 对象
    
    Returns:
        Python 原生 ``dict`` 对象
    """
    return { c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs }
