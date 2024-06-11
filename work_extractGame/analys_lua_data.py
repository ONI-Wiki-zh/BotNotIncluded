"""解析Module:Data页面的lua表格，导出json文件或schema规范文件"""
import json
from slpp import slpp
from genson import SchemaBuilder


def load_lua2schema(lua_table):
    # 解析Lua表
    lua_table = lua_table.removeprefix("return ")
    lua_table = slpp.decode(lua_table)

    # 读取表中每一个对象
    list_item = []
    for key, item in lua_table.items():
        list_item.append(item)

    # 使用genson库生成JSON Schema
    builder = SchemaBuilder()
    builder.add_object(list_item)
    schema = builder.to_schema()
    return schema.get('items')


def lua_2_schema(lua_file_path, json_file_path):
    # 读取Lua文件
    with open(lua_file_path, 'r', encoding='utf-8') as file:
        lua_table = file.read()

    schema = load_lua2schema(lua_table)

    # 将Lua表转换为JSON
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
        pass


def lua_to_json(lua_file_path, json_file_path):
    # 读取Lua文件
    with open(lua_file_path, 'r', encoding='utf-8') as file:
        lua_table = file.read()
        lua_table = lua_table.removeprefix("return ")

    # 解析Lua表
    lua_table = slpp.decode(lua_table)

    # 将Lua表转换为JSON
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(lua_table, file)


if __name__ == '__main__':
    lua_2_schema("input.lua", "schema.json")
    lua_to_json("input.lua", "output.json")
    pass