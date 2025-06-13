# -*- coding: utf-8 -*-
"""
Created on Thu Jun 12 12:02:50 2025

@author: Admin
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/calculator")
def calculator():
    return "<h2>Calculator coming soon!</h2>"