import os
from app import create_app, db
from app.posts.models import Post

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Post': Post}


if __name__ == "__main__":
    app.run(debug=True)