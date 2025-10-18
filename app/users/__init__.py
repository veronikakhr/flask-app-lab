# /app/users/__init__.py

from flask import Blueprint

# 'users' - назва blueprint
# template_folder='templates' - вказує на папку app/users/templates/
users_bp = Blueprint('users', __name__, template_folder='templates')

# Імпортуємо маршрути для цього blueprint
from . import views

# !! БІЛЬШЕ НІЧОГО ТУТ НЕ МАЄ БУТИ !!