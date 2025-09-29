#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from functools import lru_cache
from typing import Any, Literal, Pattern

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BASE_PATH


class Settings(BaseSettings):
    """全局配置"""

    model_config = SettingsConfigDict(
        env_file=f"{BASE_PATH}/.env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    # FastAPI
    FASTAPI_API_V1_PATH: str = "/api/v1"
    FASTAPI_TITLE: str = "FastAPP"
    FASTAPI_DESCRIPTION: str = "FastAPP"
    FASTAPI_DOCS_URL: str = "/docs"
    FASTAPI_REDOC_URL: str = "/redoc"
    FASTAPI_OPENAPI_URL: str | None = "/openapi"
    FASTAPI_STATIC_FILES: bool = False

    # .env 环境
    ENVIRONMENT: Literal["dev", "prod"]

    # .env 数据库
    DATABASE_TYPE: Literal["mysql", "postgresql"]
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    # 数据库
    DATABASE_ECHO: bool | Literal["debug"] = False
    DATABASE_POOL_ECHO: bool | Literal["debug"] = False
    DATABASE_SCHEMA: str = "fastapp"
    DATABASE_CHARSET: str = "utf8mb4"

    # .env Redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int

    # Redis
    REDIS_TIMEOUT: int = 5

    # .env Token
    TOKEN_SECRET_KEY: str  # 密钥 secrets.token_urlsafe(32)

    # Token
    TOKEN_ALGORITHM: str = "HS256"  # 算法
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # 过期时间，单位：秒
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 天
    TOKEN_REDIS_PREFIX: str = "fastapp:token"
    TOKEN_EXTRA_INFO_REDIS_PREFIX: str = "fastapp:token_extra_info"
    TOKEN_ONLINE_REDIS_PREFIX: str = "fastapp:token_online"
    TOKEN_REFRESH_REDIS_PREFIX: str = "fastapp:refresh_token"
    TOKEN_REQUEST_PATH_EXCLUDE: list[str] = [  # JWT / RBAC 路由白名单
        f"{FASTAPI_API_V1_PATH}/auth/login",
    ]
    TOKEN_REQUEST_PATH_EXCLUDE_PATTERN: list[Pattern[str]] = [  # JWT / RBAC 路由白名单（正则）
        re.compile(rf"^{FASTAPI_API_V1_PATH}/monitors/(redis|server)$"),
    ]
    TOKEN_URL_SWAGGER: str = f"{FASTAPI_API_V1_PATH}/auth/login/swagger"

    # JWT
    JWT_USER_REDIS_PREFIX: str = "fastapp:jwt:admin"

    # RBAC
    RBAC_ROLE_MENU_MODE: bool = True
    RBAC_ROLE_MENU_EXCLUDE: list[str] = [
        "sys:monitor:redis",
        "sys:monitor:server",
    ]

    # Cookie
    COOKIE_REFRESH_TOKEN_KEY: str = "fastapp_refresh_token"
    COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # 7 天

    # 验证码
    CAPTCHA_LOGIN_REDIS_PREFIX: str = "fastapp:login:captcha"
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 5  # 3 分钟

    # 数据权限
    DATA_PERMISSION_MODELS: dict[str, str] = {  # 允许进行数据过滤的 SQLA 模型，它必须以模块字符串的方式定义
        "部门": "backend.app.admin.model.Dept",
    }
    DATA_PERMISSION_COLUMN_EXCLUDE: list[str] = [  # 排除允许进行数据过滤的 SQLA 模型列
        "id",
        "sort",
        "del_flag",
        "created_time",
        "updated_time",
    ]

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = [  # 末尾不带斜杠
        "http://127.0.0.1:8000",
        "http://localhost:5173",
    ]
    CORS_EXPOSE_HEADERS: list[str] = [
        "X-Request-ID",
    ]

    # 中间件配置
    MIDDLEWARE_CORS: bool = True

    # 请求限制配置
    REQUEST_LIMITER_REDIS_PREFIX: str = "fastapp:limiter"

    # 时间配置
    DATETIME_TIMEZONE: str = "Asia/Shanghai"
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # 文件上传
    UPLOAD_READ_SIZE: int = 1024
    UPLOAD_IMAGE_EXT_INCLUDE: list[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    UPLOAD_IMAGE_SIZE_MAX: int = 5 * 1024 * 1024  # 5 MB
    UPLOAD_VIDEO_EXT_INCLUDE: list[str] = ["mp4", "mov", "avi", "flv"]
    UPLOAD_VIDEO_SIZE_MAX: int = 20 * 1024 * 1024  # 20 MB

    # 演示模式配置
    DEMO_MODE: bool = False
    DEMO_MODE_EXCLUDE: set[tuple[str, str]] = {
        ("POST", f"{FASTAPI_API_V1_PATH}/auth/login"),
        ("POST", f"{FASTAPI_API_V1_PATH}/auth/logout"),
        ("GET", f"{FASTAPI_API_V1_PATH}/auth/captcha"),
    }

    # IP 定位配置
    IP_LOCATION_PARSE: Literal["online", "offline", "false"] = "offline"
    IP_LOCATION_REDIS_PREFIX: str = "fba:ip:location"
    IP_LOCATION_EXPIRE_SECONDS: int = 60 * 60 * 24  # 1 天

    # Trace ID
    TRACE_ID_REQUEST_HEADER_KEY: str = "X-Request-ID"
    TRACE_ID_LOG_LENGTH: int = 32  # UUID 长度，必须小于等于 32
    TRACE_ID_LOG_DEFAULT_VALUE: str = "-"

    # 日志
    LOG_FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | <cyan>{correlation_id}</> | <lvl>{message}</>"
    )

    # 日志（控制台）
    LOG_STD_LEVEL: str = "INFO"

    # 日志（文件）
    LOG_FILE_ACCESS_LEVEL: str = "INFO"
    LOG_FILE_ERROR_LEVEL: str = "ERROR"
    LOG_ACCESS_FILENAME: str = "fastapp_access.log"
    LOG_ERROR_FILENAME: str = "fastapp_error.log"

    # .env 操作日志
    OPERA_LOG_ENCRYPT_SECRET_KEY: str  # 密钥 os.urandom(32), 需使用 bytes.hex() 方法转换为 str

    # 操作日志
    OPERA_LOG_PATH_EXCLUDE: list[str] = [
        "/favicon.ico",
        "/docs",
        "/redoc",
        "/openapi",
        f"{FASTAPI_API_V1_PATH}/auth/login/swagger",
        f"{FASTAPI_API_V1_PATH}/oauth2/github/callback",
        f"{FASTAPI_API_V1_PATH}/oauth2/linux-do/callback",
    ]
    OPERA_LOG_ENCRYPT_TYPE: int = 1  # 0: AES (性能损耗); 1: md5; 2: ItsDangerous; 3: 不加密, others: 替换为 ******
    OPERA_LOG_ENCRYPT_KEY_INCLUDE: list[str] = [  # 将加密接口入参参数对应的值
        "password",
        "old_password",
        "new_password",
        "confirm_password",
    ]
    OPERA_LOG_QUEUE_BATCH_CONSUME_SIZE: int = 100
    OPERA_LOG_QUEUE_TIMEOUT: int = 60  # 1 分钟

    # I18n 配置
    I18N_DEFAULT_LANGUAGE: str = "zh-CN"

    # 基础配置
    EMAIL_CAPTCHA_REDIS_PREFIX: str = "fastapp:email:captcha"
    EMAIL_CAPTCHA_EXPIRE_SECONDS: int = 60 * 3  # 3 分钟

    @model_validator(mode="before")
    @classmethod
    def _prepare_settings(cls, values: dict[str, Any]) -> dict[str, Any]:
        """在 Pydantic 模型验证前预处理和准备配置项"""

        # 检查环境变量
        if values.get("ENVIRONMENT") == "prod":
            # FastAPI
            values["FASTAPI_OPENAPI_URL"] = None
            values["FASTAPI_STATIC_FILES"] = False

        return values


@lru_cache
def get_settings() -> Settings:
    """读取配置优化写法"""
    return Settings()  # type: ignore


settings = get_settings()
