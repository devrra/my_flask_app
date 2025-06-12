# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 12:02:50 2025

@author: Admin
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from Render!</h1>"
