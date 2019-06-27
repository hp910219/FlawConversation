# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2019/6/24 0024
__author__ = 'huohuo'
import random
import os
from jy_word.File import File

static_dir = os.path.join(os.path.dirname(__file__), 'static')
json_dir = os.path.join(static_dir, 'json')
if os.path.exists(json_dir) is False:
    os.makedirs(json_dir)
my_file = File()
auth_code_path = os.path.join(json_dir, 'auth_code.json')


def create_str(length):
    random_str = ''
    for i in range(length):
        temp = random.randrange(0, 2)
        if temp == 0:
            random_str += chr(random.randrange(ord('A'), ord('Z') + 1))
        else:
            random_str += chr(random.randrange(ord('a'), ord('z') + 1))
    return random_str


def create_strs(num, belong=None):
    items = my_file.read(auth_code_path) or []
    for i in range(len(items), num):
        item = {}
        while True:
            random_str = create_str(6)
            f_items = filter(lambda x: x['code'] == random_str, items)
            if len(f_items) == 0:
                item['code'] = random_str
                if belong:
                    item['belong'] = belong
                break
        items.append(item)
    my_file.write(auth_code_path, items)
    items.reverse()
    return items


if __name__ == "__main__":
    pass
    

