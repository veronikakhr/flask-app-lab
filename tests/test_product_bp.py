import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app 

class ProductBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування."""
        self.app = create_app('testing') 
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        """Очищення після тесту."""
        self.app_context.pop()

    def test_product_list_page(self):
        """Тест маршруту /products/list."""
        response = self.client.get("/products/list")
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук".encode('utf-8'), response.data)
        self.assertIn("Наші Товари".encode('utf-8'), response.data)

if __name__ == "__main__":
    unittest.main()