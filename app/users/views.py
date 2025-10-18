# /app/users/views.py
from flask import request, redirect, url_for, render_template
from . import users_bp # Імпортуємо наш blueprint з __init__.py

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name_upper = name.upper() 
    age = request.args.get("age", None)
    # Шлях "users/hi.html" Flask буде шукати у /app/users/templates/
    return render_template("users/hi.html", name=name_upper, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)