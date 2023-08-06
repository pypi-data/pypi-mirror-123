import hashlib

import codefast as cf
import redis
from flask import Flask, redirect, request
from hashids import Hashids

from dofast._flask.config import AUTH_KEY
from dofast._flask.utils import authenticate_flask
from dofast.network import Twitter
from dofast.security._hmac import certify_token
from dofast.toolkits.telegram import Channel
from dofast.config import CHANNEL_MESSALERT

app = Flask(__name__)
authenticate_flask(app)


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    return 'InternalError'


@app.route('/tweet', methods=['GET', 'POST'])
def tweet():
    msg = request.get_json()
    text = cf.utils.decipher(AUTH_KEY, msg.get('text'))
    media = [f'/tmp/{e}' for e in msg.get('media')]
    cf.info(f'Input tweet: {text} / ' + ''.join(media))
    Twitter().post([text] + media)
    return 'SUCCESS'


@app.route('/messalert', methods=['GET', 'POST'])
def msg():
    js = request.get_json()
    Channel(CHANNEL_MESSALERT).post(js['text'])
    return 'SUCCESS'


@app.route('/nsq', methods=['GET', 'POST'])
def nsq():
    msg = request.get_json()
    topic = msg.get('topic')
    channel = msg.get('channel')
    data = msg.get('data')
    cf.net.post(f'http://127.0.0.1:4151/pub?topic={topic}&channel={channel}',
                json={'data': data})
    print(topic, channel, data)
    return 'SUCCESS'


@app.route('/hello')
def hello_world():
    return 'SUCCESS!'


r = redis.Redis(host='localhost', port='6379')


@app.route('/s', methods=['GET', 'POST'])
def shorten() -> str:
    data = request.get_json(force=True)
    if not data: return 'SUCCESS'
    url = data.get('url', '')
    md5 = hashlib.md5(url.encode()).hexdigest()
    hid = Hashids(salt=md5, min_length=6)
    uniq_id = hid.encode(42)
    r.hset('shorten', mapping={uniq_id: url})
    return request.host_url + 's/' + uniq_id


@app.route('/<path:path>')
def all_other(path):
    path_str = str(path)
    if not path_str.startswith('s/'):
        return ''
    cache = r.hgetall('shorten')
    _code = path_str.replace('s/', '').encode()
    cf.info(cache, _code)
    if _code in cache:
        url = cache[_code].decode()
        return redirect(url)
    else:
        return redirect('https://www.google.com')


def run():
    app.run(host='0.0.0.0', port=6363, debug=True)
    # app.run(host='0.0.0.0', port=6363, ssl_context=('path_to.cer', 'path_to.key'), debug=True)


if __name__ == '__main__':
    run()
