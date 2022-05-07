from sqlalchemy.orm import registry

# ORM 的基类

mapper_registry = registry()
Base = mapper_registry.generate_base()
