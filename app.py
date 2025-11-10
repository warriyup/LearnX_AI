
from flask import Flask, request, redirect, render_template
import re
from full_version.app import blueprint as full_bp
from light_version.app import blueprint as lite_bp

app = Flask(__name__)

def is_mobile(ua):
    if not ua: return False
    ua=ua.lower()
    return bool(re.search(r"iphone|android|mobile|ipad|ipod|opera mini|mobi", ua))

app.register_blueprint(full_bp, url_prefix="/full")
app.register_blueprint(lite_bp, url_prefix="/lite")

@app.route("/")
def root():
    mode = request.cookies.get("mode", "auto")
    if mode=="lite":
        return redirect("/lite/")
    ua=request.headers.get("User-Agent","")
    if is_mobile(ua):
        return redirect("/lite/")
    return redirect("/full/")

@app.route("/settings")
def settings():
    return render_template("settings.html")
