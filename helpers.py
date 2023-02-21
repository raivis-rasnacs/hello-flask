from flask import render_template

def error_page(error_code):
    return render_template("404.html")