from flask import Flask
from database import db

app = Flask(__name__)
app.config.from_pyfile('settings.py')
db.init_app(app)


@app.route('/hello-world', methods=['GET'])
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True)
