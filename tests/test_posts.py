import unittest
from app import create_app, db
from app.posts.models import Post, CategoryEnum
from datetime import datetime


class PostsTestCase(unittest.TestCase):
    """Тести для функціоналу постів"""
    
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()
    
    def tearDown(self):
        """Очищення після кожного тесту"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_create_post_model(self):
        """Тест створення моделі поста"""
        post = Post(
            title="Test Post",
            content="Test Content",
            category=CategoryEnum.tech
        )
        db.session.add(post)
        db.session.commit()
        
        self.assertIsNotNone(post.id)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.author, "Anonymous")
        self.assertTrue(post.is_active)
    
    def test_create_post_route(self):
        """Тест маршруту створення поста"""
        response = self.client.get('/post/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'form', response.data)
    
    def test_create_post_submit(self):
        """Тест відправки форми створення поста"""
        with self.client:
            response = self.client.post('/post/create', data={
                'title': 'New Post',
                'content': 'New Content',
                'category': 'tech',
                'enabled': True,
                'publish_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M')
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            
            post = db.session.scalars(
                db.select(Post).where(Post.title == 'New Post')
            ).first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, 'New Content')
    
    def test_list_posts(self):
        """Тест списку постів"""
        post1 = Post(title="Post 1", content="Content 1", category=CategoryEnum.news)
        post2 = Post(title="Post 2", content="Content 2", category=CategoryEnum.tech)
        db.session.add_all([post1, post2])
        db.session.commit()
        
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post 1', response.data)
        self.assertIn(b'Post 2', response.data)
    
    def test_detail_post(self):
        """Тест перегляду деталей поста"""
        post = Post(title="Detail Post", content="Detail Content", category=CategoryEnum.other)
        db.session.add(post)
        db.session.commit()
        
        response = self.client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Post', response.data)
        self.assertIn(b'Detail Content', response.data)
    
    def test_detail_post_not_found(self):
        """Тест перегляду неіснуючого поста"""
        response = self.client.get('/post/9999')
        self.assertEqual(response.status_code, 404)
    
    def test_update_post(self):
        """Тест оновлення поста"""
        post = Post(title="Old Title", content="Old Content", category=CategoryEnum.tech)
        db.session.add(post)
        db.session.commit()
        
        with self.client:
            response = self.client.post(f'/post/{post.id}/update', data={
                'title': 'Updated Title',
                'content': 'Updated Content',
                'category': 'news',
                'enabled': True,
                'publish_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M')
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            
            updated_post = db.get_or_404(Post, post.id)
            self.assertEqual(updated_post.title, 'Updated Title')
            self.assertEqual(updated_post.content, 'Updated Content')
    
    def test_delete_post_confirmation(self):
        """Тест сторінки підтвердження видалення"""
        post = Post(title="To Delete", content="Delete Content", category=CategoryEnum.other)
        db.session.add(post)
        db.session.commit()
        
        response = self.client.get(f'/post/{post.id}/delete')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'To Delete', response.data)
    
    def test_delete_post(self):
        """Тест видалення поста"""
        post = Post(title="To Delete", content="Delete Content", category=CategoryEnum.other)
        db.session.add(post)
        db.session.commit()
        post_id = post.id
        
        with self.client:
            response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            deleted_post = db.session.get(Post, post_id)
            self.assertIsNone(deleted_post)
    
    def test_only_active_posts_shown(self):
        """Тест відображення тільки активних постів"""
        active_post = Post(title="Active", content="Content", is_active=True, category=CategoryEnum.tech)
        inactive_post = Post(title="Inactive", content="Content", is_active=False, category=CategoryEnum.tech)
        db.session.add_all([active_post, inactive_post])
        db.session.commit()
        
        response = self.client.get('/post/')
        self.assertIn(b'Active', response.data)
        self.assertNotIn(b'Inactive', response.data)
    
    def test_post_with_user_in_session(self):
        """Тест створення поста авторизованим користувачем"""
        with self.client.session_transaction() as sess:
            sess['user'] = 'testuser'
        
        with self.client:
            response = self.client.post('/post/create', data={
                'title': 'User Post',
                'content': 'User Content',
                'category': 'tech',
                'enabled': True,
                'publish_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M')
            }, follow_redirects=True)
            
            post = db.session.scalars(
                db.select(Post).where(Post.title == 'User Post')
            ).first()
            self.assertEqual(post.author, 'testuser')


if __name__ == '__main__':
    unittest.main()