# -*- coding: utf-8 -*-

from marshmallow import fields, ValidationError

from docparser.config.excel.enums import BlockType


class CustomFields:
    """
    自定义字段类型
    """

    class BlockTypeField(fields.Field):
        """
        块类型枚举字段
        """

        def _serialize(self, value, attr, obj, **kwargs):
            try:
                if value is None:
                    return BlockType.text.name
                return value.name

            except ValueError as error:
                raise ValidationError("指定的类型值不在[text,table]范围内!") from error

        def _deserialize(self, value, attr, data, **kwargs):
            try:
                return BlockType[value]
            except ValueError as error:
                raise ValidationError("指定的类型值不在[0-1]范围内!") from error

    class TableModeField(fields.Field):
        """
        表格模式
        """

        def _serialize(self, value, attr, obj, **kwargs):
            if value is None:
                return TableMode.standard.name
            return value.name

        def _deserialize(self, value, attr, data, **kwargs):
            try:
                return TableMode[value]
            except ValueError as error:
                raise ValidationError("指定的类型值不在[standard,promiscuous,custom]范围内!") from error

    class HorizontalAlignModeField(fields.Field):
        """
        水平对齐方式
        """

        def _serialize(self, value, attr, obj, **kwargs):
            if value is None:
                return HorizontalAlignMode.right.name
            return value.name

        def _deserialize(self, value, attr, data, **kwargs):
            try:
                return HorizontalAlignMode[value]
            except ValueError as error:
                raise ValidationError("指定的类型值不在[left,center,right]范围内!") from error

    class VerticalAlignModeField(fields.Field):
        """
        水平对齐方式
        """

        def _serialize(self, value, attr, obj, **kwargs):
            if value is None:
                return VerticalAlignMode.middle.name
            return value.name

        def _deserialize(self, value, attr, data, **kwargs):
            try:
                return VerticalAlignMode[value]
            except ValueError as error:
                raise ValidationError("指定的类型值不在[top,middle,bottom]范围内!") from error
