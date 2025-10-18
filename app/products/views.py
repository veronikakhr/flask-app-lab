from flask import render_template
from . import products_bp

@products_bp.route('/list')
def product_list():
    items = [
        {"id": 1, "name": "Ноутбук"},
        {"id": 2, "name": "Мишка"},
        {"id": 3, "name": "Клавіатура"}
    ]
    return render_template('products/list.html', items=items)