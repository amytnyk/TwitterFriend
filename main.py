from flask import Flask, jsonify, request

import twitter
from twitter import get_friends, TwitterException
from mapbuilder import build_map

app = Flask(__name__, static_url_path='/static/', static_folder='static')


@app.route('/map')
def get_map():
    if twitter.latest_uses == 15:
        return jsonify({'ok': False, 'error': "Too Many Requests (15 out of 15), please wait"}), 400
    try:
        if 'user' in request.args and 'count' in request.args:
            username = request.args.get('user')
            count = request.args.get('count')

            if not count.isdigit() or int(count) <= 0:
                return jsonify({'ok': False, 'error': "Count should be positive integer"}), 400

            if len(username) == 0:
                return jsonify({'ok': False, 'error': "Username should not be empty"}), 400

            html_map = build_map(get_friends(username, int(count))).get_root().render()
            return jsonify({'ok': True, 'map': html_map}), 200
        else:
            return jsonify({'ok': False, 'error': "No user or count"}), 400
    except TwitterException as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    except KeyError:
        return jsonify({'ok': False, 'error': "Username not found"}), 400
    except ConnectionError:
        return jsonify({'ok': False, 'error': "Connection error"}), 500
    except Exception:
        return jsonify({'ok': False, 'error': 'Server error'}), 500


@app.route('/latest_use')
def latest_use():
    return str(twitter.latest_uses)


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(port=8080)
