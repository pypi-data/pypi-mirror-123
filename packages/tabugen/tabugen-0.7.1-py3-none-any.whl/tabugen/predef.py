# Copyright (C) 2018-present ichenq@outlook.com. All rights reserved.
# Distributed under the terms and conditions of the Apache License.
# See accompanying files LICENSE.


PredefMetaSheet = "@meta"                    # meta sheet名称
PredefStructTypeRow = "type_row"            # 这一行描述类型
PredefStructNameRow = "name_row"            # 这一行描述名称
PredefCommentRow = "comment_row"            # 这一行描述注释蚊子
PredefDataStartRow = "data_start_row"       # 数据从这一行开始
PredefDataEndRow = "data_end_row"           # 数据从这一行结束，默认为末尾行
PredefClassName = "class_name"              # 生成的class名称
PredefClassComment = "class_comment"        # 生成的class注释
PredefTargetFileName = "target_file"        # 作用的文件
PredefTargetFileSheet = "target_sheet"      # 作用的sheet
PredefHideColumns = 'hide_value_columns'    # 对于这些列，它们的值会在hide-column选项开启的时候隐藏

PredefParseKVMode = "kv_mode"                   # 是否是KV模式
PredefKeyValueColumns = "kv_columns"            # KV模式中的key,type,value所在列，如 1，2, 3
PredefKeyColumn = "kv_key_column"               # KV模式中的key所在列，从PredefKeyValueColumn解析
PredefValueColumn = "kv_value_column"           # KV模式中的value所在列，从PredefKeyValueColumn解析
PredefValueTypeColumn = "kv_value_type_column"  # KV模式中的value类型所在列
PredefCommentColumn = "kv_comment_column"       # KV模式中的注释所在列

PredefInnerTypeRange = "inner_type_range"
PredefInnerTypeClass = "inner_type_class"
PredefInnerTypeName = "inner_type_name"

OptionAutoVector = "auto_vector"            # 自动把名称相近的字段合并为数组

OptionUniqueColumns = "unique_columns"    # 值唯一的列

#
# SQL导入器
#
OptionCamelcaseField = "camelcase_field"
OptionFieldGetterSetter = "field_getset"
OptionNamePrefix = "prefix"
