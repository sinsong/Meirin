from meirin.db import engine
from meirin.db.base_class import mapper_registry

# 基类
from meirin.db.base_class import Base

# 导入所有 ORM 对象
from meirin.db.policy     import Policy
from meirin.db.metapolicy import MetaPolicy

# 创建数据库结构
def create_all():
    mapper_registry.metadata.create_all(bind=engine)
