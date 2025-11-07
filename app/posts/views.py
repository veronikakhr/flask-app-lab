from flask import render_template, redirect, url_for, flash, session, request
from app import db
from . import posts_bp
from .models import Post, CategoryEnum
from .forms import PostForm


@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    
    if form.validate_on_submit():
        author = session.get('user', 'Anonymous')
        
        post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.enabled.data,
            posted=form.publish_date.data,
            category=CategoryEnum[form.category.data],
            author=author
        )
        
        db.session.add(post)
        db.session.commit()
        
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.list_posts'))
    
    return render_template('posts/add_post.html', form=form, title='Створити пост')


@posts_bp.route('/', methods=['GET'])
def list_posts():
    stmt = db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    
    return render_template('posts/posts.html', posts=posts, title='Всі пости')


@posts_bp.route('/<int:id>', methods=['GET'])
def detail_post(id):
    post = db.get_or_404(Post, id)
    
    return render_template('posts/detail_post.html', post=post, title=post.title)


@posts_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    """Редагування існуючого поста"""
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        post.category = CategoryEnum[form.category.data]
        
        db.session.commit()
        
        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))
    
    form.publish_date.data = post.posted
    form.category.data = post.category.value
    form.enabled.data = post.is_active
    
    return render_template('posts/add_post.html', form=form, post=post, title='Редагувати пост')


@posts_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        
        flash('Пост успішно видалено!', 'success')
        return redirect(url_for('posts.list_posts'))
    
    return render_template('posts/delete_confirm.html', post=post, title='Видалити пост')