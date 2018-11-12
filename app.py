import os
import flask
import argparse
import yaml

from filelock import FileLock

app = flask.Flask(__name__)
GUESTLIST = []

rsvp_filename = 'rsvps.yaml'

@app.errorhandler(404)
def not_found(e):
    return flask.render_template('404.j2'), 404

@app.errorhandler(403)
def unauthorized(e):
    return flask.render_template('403.j2'), 403

@app.route('/')
def index():
    return flask.render_template('index.j2')

@app.route('/u/<key>')
def index_with_key(key):
    username = _validate_guest(key)
    if username is None:
        return unauthorized(None)

    return flask.render_template('index.j2', user_key=key, user_name=username)

@app.route('/rsvp', methods=['POST'])
def rsvp():
    data = flask.request.json
    print(data)
    username = _validate_guest(data['userKey'])
    if username == data['userName']:
        # rsvp authorized
        del data['userKey']
        with FileLock(rsvp_filename + '.lock'):
            if os.path.exists(rsvp_filename):
                with open(rsvp_filename, 'r') as f:
                    rsvp_dict = yaml.load(f)
            else:
                rsvp_dict = {}

            rsvp_dict[username] = data

            with open(rsvp_filename, 'w') as f:
                yaml.dump(rsvp_dict, f, default_flow_style=False)

        return "RSVPed succesfully"
    else:
        return unauthorized(None)

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
