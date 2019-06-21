#! /usr/bin/env python
# coding: utf-8

from flask import Flask
from flask_cors import CORS


def create_app():
    my_app = Flask(__name__)
    my_app.config.update(
        MAX_CONTENT_LENGTH=50 * 1024 * 1024 * 1024
    )
    CORS(my_app, supports_credentials=True)
    return my_app