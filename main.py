from flask import Flask, jsonify
from twitter import get_friends
from mapbuilder import build_map

app = Flask(__name__, static_url_path='/static/', static_folder='static')


@app.route('/map/<username>')
def login(username):
    try:
        return build_map(get_friends(username)).get_root().render()
    except KeyError:
        return jsonify({'ok': False, 'error': "Username not found"}), 400
    except ConnectionError:
        return jsonify({'ok': False, 'error': "Connection error"}), 400
    except Exception:
        return jsonify({'ok': False, 'error': 'Unknown error'}), 400


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(port=80)
