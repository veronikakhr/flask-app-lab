from app import app  
from flask import render_template 

@app.route('/')
def home():
    return render_template('resume.html', title="Резюме Вероніки")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Контакти")
