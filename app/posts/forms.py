from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length
from datetime import datetime


class PostForm(FlaskForm):
    """Форма для створення та редагування поста"""
    
    title = StringField('Заголовок', 
                        validators=[
                            DataRequired(message="Заголовок обов'язковий"),
                            Length(max=150, message="Заголовок не може перевищувати 150 символів")
                        ])
    
    content = TextAreaField('Контент', 
                            validators=[
                                DataRequired(message="Контент обов'язковий")
                            ])
    
    enabled = BooleanField('Активний пост', default=True)
    
    publish_date = DateTimeLocalField('Дата публікації', 
                                      format='%Y-%m-%dT%H:%M',
                                      default=datetime.utcnow)
    
    category = SelectField('Категорія',
                           choices=[
                               ('news', 'Новини'),
                               ('publication', 'Публікація'),
                               ('tech', 'Технології'),
                               ('other', 'Інше')
                           ],
                           validators=[DataRequired(message="Оберіть категорію")])
    
    submit = SubmitField('Зберегти')