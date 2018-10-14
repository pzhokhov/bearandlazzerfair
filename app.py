import flask
import argparse

app = flask.Flask('__name__')

@app.errorhandler(404)
def not_found(e):
    return flask.render_template('404.j2'), 404

@app.route('/')
def index():
    return flask.render_template('index.j2')

@app.route('/rsvp', methods=['POST'])
def rsvp():
    data = flask.request.json
    print(data)
    return "RSVPed"

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--debug', action='store_true')
    argparser.add_argument('--port', default=5000)
    args = argparser.parse_args()

    app.run(host='0.0.0.0', debug=args.debug, port=args.port)

if __name__ == '__main__':
    main()
