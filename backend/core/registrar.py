#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Depends
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp

from backend import __version__
from backend.app.router import route
from backend.common.exception.exception_handler import register_exception
from backend.common.log import setup_logging, set_custom_logfile
from backend.core.path_conf import STATIC_DIR
from backend.database.redis import redis_client
from backend.core.conf import settings
from backend.database.db import create_tables
from backend.utils.demo_site import demo_site
from backend.utils.health_check import http_limit_callback, ensure_unique_route_names
from backend.utils.openapi import simplify_operation_ids
from backend.utils.serializers import MsgSpecJSONResponse


@asynccontextmanager
async def register_init(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    启动初始化

    :param app: FastAPI  应用实例
    :return:
    """
    # 创建数据库表
    await create_tables()

    # 初始化 redis
    await redis_client.open()
    # 初始化 limiter
    await FastAPILimiter.init(
        redis=redis_client,
        prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
        http_callback=http_limit_callback,
    )

    yield

    # 关闭 redis 连接
    await redis_client.close()
    # 关闭 limiter
    await FastAPILimiter.close()


def register_app() -> FastAPI:
    """注册 FastAPI 应用"""

    class MyFastAPI(FastAPI):
        if settings.MIDDLEWARE_CORS:
            # Related issues
            # https://github.com/fastapi/fastapi/discussions/7847
            # https://github.com/fastapi/fastapi/discussions/8027
            def build_middleware_stack(self) -> ASGIApp:
                return CORSMiddleware(
                    super().build_middleware_stack(),
                    allow_origins=settings.CORS_ALLOWED_ORIGINS,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                    expose_headers=settings.CORS_EXPOSE_HEADERS,
                )

    app = MyFastAPI(
        title=settings.FASTAPI_TITLE,
        version=__version__,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        redoc_url=settings.FASTAPI_REDOC_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init,
    )

    # 注册组件
    register_logger()
    register_static_file(app)
    register_middleware(app)
    register_router(app)
    register_page(app)
    register_exception(app)

    return app


def register_logger() -> None:
    """注册日志"""

    setup_logging()
    set_custom_logfile()


def register_static_file(app: FastAPI) -> None:
    """
    静态文件交互开发模式, 生产将自动关闭，生产必须使用 nginx 静态资源服务

    :param app:
    :return:
    """
    if settings.FASTAPI_STATIC_FILES:
        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.makedirs(STATIC_DIR)

        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def register_middleware(app: FastAPI) -> None:
    """
    注册中间件（执行顺序从下往上）

    :param app: FastAPI 应用实例
    :return:
    """
    ...


def register_router(app: FastAPI) -> None:
    """
    注册路由

    :param app: FastAPI
    :return:
    """
    dependencies = [Depends(demo_site)] if settings.DEMO_MODE else None

    # API
    app.include_router(route, dependencies=dependencies)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)


def register_page(app: FastAPI) -> None:
    """
    注册分页查询功能

    :param app: FastAPI 应用实例
    :return:
    """
    add_pagination(app)
