from flask import render_template, request, flash, redirect, url_for, current_app
from app.forms import ContactForm
from loguru import logger

logger.add("logs/contact_form.log", rotation="10 MB", level="INFO", format="{time} {level} {message}")


def register_routes(app):
    
    @app.route('/')
    def home():
        return render_template('resume.html', title="Резюме Вероніки")

    @app.route('/contacts', methods=['GET', 'POST'])
    def contacts():
        form = ContactForm()
        
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            subject = form.subject.data
            message = form.message.data

            logger.info(f"Нове повідомлення з форми: Ім'я={name}, Email={email}, Телефон={phone}, Тема={subject}, Повідомлення={message}")
            
            flash(f'Дякуємо, {name}! Ваше повідомлення з email {email} було успішно відправлено.', 'success')
            
            return redirect(url_for('contacts'))
        
        return render_template('contacts.html', title="Контакти", form=form)