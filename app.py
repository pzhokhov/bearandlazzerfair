import os
import flask
import argparse
import yaml

app = flask.Flask(__name__)
GUESTLIST = []

@app.errorhandler(404)
def not_found(e):
    return flask.render_template('404.j2'), 404

@app.route('/')
def index():
    return flask.render_template('index.j2')

@app.route('/u/<key>')
def index_with_key(key):
    username = _validate_guest(key)
    if username is None:
        return not_found(None)

    return flask.render_template('index.j2', user_key=key, user_name=username)

@app.route('/rsvp', methods=['POST'])
def rsvp():
    data = flask.request.json
    print(data)
    return "RSVPed"


def _validate_guest(key):
    for g in GUESTLIST:
        if g['key'] == key:
            return g['name']


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--debug', action='store_true')
    argparser.add_argument('--port', default=5000)
    argparser.add_argument('--guests', default='guests.yaml')
    args = argparser.parse_args()

    with open(args.guests) as f:
        for g in yaml.load(f):
            GUESTLIST.append(g)

    app.run(host='localhost', debug=args.debug, port=args.port)

if __name__ == '__main__':
    main()
