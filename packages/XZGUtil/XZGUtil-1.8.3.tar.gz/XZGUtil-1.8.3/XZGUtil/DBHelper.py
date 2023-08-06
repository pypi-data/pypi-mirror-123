#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021-10-18 17:25
# @Site    :
# @File    : DBHelper.py
# @Software: PyCharm


def create_in_sql(table_name: str, data: dict):
    """
    传入字典和表名，返回组装好的sql
    sql中的插入字段为传入字典的key
    data = {'w':'d1','ew':'d2','wr':'d3','wa':'d4'}
    """
    sql = 'insert into ' + table_name + ' ('
    data_keys = [key for key in data.keys()]
    for key in data_keys:
        sql += key
        if data_keys.index(key) != len(data_keys) - 1:
            sql += ','
        else:
            sql += ')  values ( '
            for key in data_keys:
                if isinstance(data.get(key), str):
                    sql += f'"{data.get(key)}",'
                else:
                    sql += f'{data.get(key)},'
            sql = sql.rstrip(',')
            sql += ");"
    return sql
