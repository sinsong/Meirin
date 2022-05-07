from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings

class Settings(BaseSettings):
    """配置对象
    """

    # 数据库
    DATABASE_URL :str

    # 安全
    SECRET_KEY :str # 原本是密钥，现在改为密码，管理本系统需要提供该字段

    # Debug
    DEBUG :bool = False

    # 配置对象本身的配置
    class Config:
        case_sensitive = True  # 大小写敏感
        env_file = '.env'      # 读取 .env 文件

settings = Settings()
