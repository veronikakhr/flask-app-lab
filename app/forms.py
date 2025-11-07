from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp, Optional

class ContactForm(FlaskForm):
    name = StringField('Ім\'я', 
                       validators=[DataRequired(message="Це поле обов'язкове."), 
                                   Length(min=4, max=10, message="Ім'я повинно бути від 4 до 10 символів.")])
    
    email = StringField('Email', 
                        validators=[DataRequired(message="Це поле обов'язкове."), 
                                    Email(message="Введіть коректний email.")])
    
    phone = StringField('Телефон', 
                        validators=[Optional(),  
                                    Regexp(r'^\+380\d{9}$', 
                                           message="Формат телефону має бути +380XXXXXXXXX.")])
    
    subject = SelectField('Тема', 
                          validators=[DataRequired(message="Будь ласка, оберіть тему.")],
                          choices=[
                              ('', 'Оберіть тему...'),
                              ('general', 'Загальне питання'),
                              ('support', 'Технічна підтримка'),
                              ('feedback', 'Відгук')
                          ])
    
    message = TextAreaField('Повідомлення', 
                            validators=[DataRequired(message="Це поле обов'язкове."), 
                                        Length(max=500, message="Повідомлення не повинно перевищувати 500 символів.")])
    
    submit = SubmitField('Відправити')


class LoginForm(FlaskForm):
    username = StringField('Ім\'я користувача', 
                           validators=[DataRequired(message="Це поле обов'язкове.")])
    
    password = PasswordField('Пароль', 
                             validators=[DataRequired(message="Це поле обов'язкове."), 
                                         Length(min=4, max=10, message="Пароль має бути від 4 до 10 символів.")])
    
    remember = BooleanField('Запам\'ятати мене')
    
    submit = SubmitField('Увійти')

