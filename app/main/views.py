from flask import Flask, redirect, render_template, request, url_for

from . import main


@main.route("/")
@main.route("/index")
def index():
    return render_template("index.html")
