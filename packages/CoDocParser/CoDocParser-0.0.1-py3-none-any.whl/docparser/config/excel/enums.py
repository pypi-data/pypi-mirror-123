# -*- coding: utf-8 -*-

from enum import Enum


class BlockType(Enum):
    """
    Excel块类型
    """
    # 文本块
    text = 0

    # 表格块
    table = 1


class TableMode(Enum):
    """
    Excel块表格模式
    """
    # 标准
    standard = 0

    # 混杂模式
    mixed = 1,

    # 自定义
    custom = 2


class HorizontalAlignMode(Enum):
    """
    水平对齐方式
    """
    # 左
    left = 0

    # 中
    center = 1

    # 右
    right = 2


class VerticalAlignMode(Enum):
    """
    垂直对齐方式
    """
    # 上
    top = 0

    # 中
    middle = 1

    # 下
    bottom = 2

