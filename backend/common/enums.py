#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Any, Mapping, Type, cast

T = Type[Enum]


class _EnumBase:
    """枚举基类，提供通用方法"""

    @classmethod
    def _get_members(cls) -> Mapping[str, Enum]:
        """获取并转换成员"""
        return cast("T", cls).__members__

    @classmethod
    def get_member_keys(cls) -> list[str]:
        """获取枚举成员名称列表"""
        return list(cls._get_members().keys())

    @classmethod
    def get_member_values(cls) -> list[Any]:
        """获取枚举成员值列表"""
        return [member.value for member in cls._get_members().values()]

    @classmethod
    def get_member_dict(cls) -> dict[str, Any]:
        """获取枚举成员字典"""
        return {name: member.value for name, member in cls._get_members().items()}


class IntEnum(_EnumBase, SourceIntEnum):
    """整型枚举基类"""

    pass


class StrEnum(_EnumBase, str, Enum):
    """字符串枚举基类"""

    pass


class MenuType(IntEnum):
    """菜单类型"""

    directory = 0
    menu = 1
    button = 2
    embedded = 3
    link = 4


class RoleDataRuleOperatorType(IntEnum):
    """数据规则运算符"""

    AND = 0
    OR = 1


class RoleDataRuleExpressionType(IntEnum):
    """数据规则表达式"""

    eq = 0  # ==
    ne = 1  # !=
    gt = 2  # >
    ge = 3  # >=
    lt = 4  # <
    le = 5  # <=
    in_ = 6
    not_in = 7


class MethodType(StrEnum):
    """HTTP 请求方法"""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"


class LoginLogStatusType(IntEnum):
    """登录日志状态"""

    fail = 0
    success = 1


class BuildTreeType(StrEnum):
    """构建树形结构类型"""

    traversal = "traversal"
    recursive = "recursive"


class OperaLogCipherType(IntEnum):
    """操作日志加密类型"""

    aes = 0
    md5 = 1
    itsdangerous = 2
    plan = 3


class StatusType(IntEnum):
    """状态类型"""

    disable = 0
    enable = 1


class UserSocialType(StrEnum):
    """用户社交类型"""

    github = "GitHub"
    google = "Google"
    linux_do = "LinuxDo"


class FileType(StrEnum):
    """文件类型"""

    image = "image"
    video = "video"


class PluginType(StrEnum):
    """插件类型"""

    zip = "zip"
    git = "git"


class UserPermissionType(StrEnum):
    """用户权限类型"""

    superuser = "superuser"
    staff = "staff"
    status = "status"
    multi_login = "multi_login"


class DataBaseType(StrEnum):
    """数据库类型"""

    mysql = "mysql"
    postgresql = "postgresql"


class PrimaryKeyType(StrEnum):
    """主键类型"""

    autoincrement = "autoincrement"
    snowflake = "snowflake"
