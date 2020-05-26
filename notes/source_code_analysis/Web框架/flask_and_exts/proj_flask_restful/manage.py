import os

from app import create_app

# conf = os.getenv('FLASK_ENV', 'production')
conf = os.getenv('FLASK_ENV', 'development')
app = create_app(conf)


if __name__ == '__main__':
    print(app.url_map)
    app.run()
