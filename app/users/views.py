from flask import request, redirect, url_for, render_template, flash, session, make_response
from . import users_bp
from app.forms import LoginForm  

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name_upper = name.upper() 
    age = request.args.get("age", None)
    return render_template("users/hi.html", name=name_upper, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('users.profile'))

    form = LoginForm() 
   
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data  

        if username == 'admin' and password == '12345':
            session['user'] = username
            
            remember_message = " (з опцією 'Запам'ятати мене')" if remember else ""
            flash(f'Ви успішно увійшли як {username}{remember_message}!', 'success') 
            
            return redirect(url_for('users.profile'))
        else:
            flash('Неправильне ім\'я користувача або пароль! Спробуйте ще раз.', 'danger') 
            return redirect(url_for('users.login'))

    return render_template('users/login.html', form=form)

@users_bp.route('/profile')
def profile():
    if 'user' in session:
        username = session['user']
        cookies = request.cookies
        return render_template('users/profile.html', user=username, cookies=cookies)
    else:
        flash('Будь ласка, увійдіть, щоб побачити цю сторінку.', 'warning')
        return redirect(url_for('users.login'))

@users_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Ви успішно вийшли з системи.', 'info')
    return redirect(url_for('users.login'))

@users_bp.route('/add_cookie', methods=['POST'])
def add_cookie():
    if 'user' not in session:
        flash('Ви не авторизовані для цієї дії.', 'danger')
        return redirect(url_for('users.login'))

    key = request.form.get('key')
    value = request.form.get('value')
    expiry = request.form.get('expiry') 

    if key and value and expiry:
        resp = make_response(redirect(url_for('users.profile')))
        try:
            resp.set_cookie(key, value, max_age=int(expiry))
            flash(f'Кукі "{key}" успішно додано!', 'success') 
        except ValueError:
            flash('Термін дії має бути цілим числом (у секундах).', 'danger')
        return resp
    
    flash('Необхідно вказати ключ, значення та термін дії.', 'warning')
    return redirect(url_for('users.profile'))

@users_bp.route('/delete_cookie_key', methods=['POST'])
def delete_cookie_key():
    if 'user' not in session:
        flash('Ви не авторизовані для цієї дії.', 'danger')
        return redirect(url_for('users.login'))

    key_to_delete = request.form.get('key_to_delete') 
    if key_to_delete:
        resp = make_response(redirect(url_for('users.profile')))
        resp.delete_cookie(key_to_delete)
        flash(f'Кукі "{key_to_delete}" видалено.', 'success') 
        return resp
    
    flash('Необхідно вказати ключ для видалення.', 'warning')
    return redirect(url_for('users.profile'))

@users_bp.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    if 'user' not in session:
        flash('Ви не авторизовані для цієї дії.', 'danger')
        return redirect(url_for('users.login'))

    resp = make_response(redirect(url_for('users.profile')))
    for key in request.cookies:
        if key != 'session':
            resp.delete_cookie(key)
    flash('Всі кукі (крім сесії) видалено.', 'success') 
    return resp

@users_bp.route('/change_theme')
def change_theme():
    current_theme = request.cookies.get('theme', 'light')
    
    new_theme = 'dark' if current_theme == 'light' else 'light'

    resp = make_response(redirect(url_for('users.profile')))
    
    resp.set_cookie('theme', new_theme, max_age=31536000)
    flash(f'Тему успішно змінено на {new_theme}!', 'info')
    return resp