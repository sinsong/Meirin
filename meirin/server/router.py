from fastapi import APIRouter

from meirin.server.endpoints import (
    enforce,
    policy,
    metapolicy,
    test
)

# 应用路由
router = APIRouter()

router.include_router(enforce.router,                          tags=["interface"])
router.include_router(policy.router,     prefix="/policy",     tags=["policy manage"])
router.include_router(metapolicy.router, prefix="/metapolicy", tags=["metapolicy manage"])
router.include_router(test.router,       prefix="/test",       tags=["test"])
