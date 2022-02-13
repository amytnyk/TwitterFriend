from flask import Flask
from twitter import get_friends
from mapbuilder import build_map

app = Flask(__name__, static_url_path='/static/', static_folder='static')


@app.route('/map/<username>')
def login(username):
    try:
        return build_map(get_friends(username)).get_root().render()
    except KeyError:
        return app.send_static_file('error.html')


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(port=80)
