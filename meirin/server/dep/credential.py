from fastapi import Header, HTTPException

from meirin.server.config import settings

def meirin_credential(
    x_meirin_credential :str = Header(None, title="Meirin manage credential", description="Secret key to manage meirin AC system")
) -> None:
    if x_meirin_credential != settings.SECRET_KEY:
        raise HTTPException(status_code=401, detail="管理系统需要认证，未经认证或凭据无效")
    return
