from flask import Flask
from flask_cors import CORS
from app import image

def manageApp():
    app = Flask(__name__)
    app.register_blueprint(image, url_prefix='/')
    CORS(app)

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)

manageApp()