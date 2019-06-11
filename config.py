# -*- coding: utf-8 -*-
# !/usr/bin/python
# Create Date 2019/6/11 0011
__author__ = 'huohuo'
import ConfigParser
import os
dir_name = os.path.dirname(__file__)


def read_conf():
    cf = ConfigParser.ConfigParser()
    cf.read(os.path.join(dir_name, 'config.conf'))
    env = cf.get('Env', 'env')
    ports = cf.items('Ports')
    if cf.has_section(env):
        items = dict(cf.items(env))
        data = {
            'ports': dict(ports),
            'env': env
        }
        data.update(items)
        return data
    return 'No such env %s' % env


if __name__ == "__main__":
    print read_conf()
    pass
    

