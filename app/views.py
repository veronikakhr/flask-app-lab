# /app/views.py
from app import app  # Імпортуємо екземпляр 'app' з app/__init__.py [cite: 40]
from flask import render_template # Імпортуємо render_template [cite: 41]

@app.route('/')
def home():
    return render_template('resume.html', title="Резюме Вероніки")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")

# У вас в app.py був 'from flask import url_for', 
# але ви його не використовували. Якщо він потрібен, додайте його до імпортів.