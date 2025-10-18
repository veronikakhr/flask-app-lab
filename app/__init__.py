# /app/__init__.py
from flask import Flask

app = Flask(__name__)

# Завантажуємо конфігурацію з файлу config.py, який знаходиться на рівень вище
app.config.from_pyfile('../config.py') 

# Імпортуємо маршрути (створимо цей файл наступним)
from . import views