from fastapi import FastAPI

from .router import router

from . import dep
from . import endpoints
from . import schema
from . import utils

# ASGI server object
app = FastAPI()

# 导入路由
app.include_router(router, prefix="/v1")
