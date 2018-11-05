import os
import flask
import argparse

app = flask.Flask(__name__)

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

    ssl_cert = os.environ.get('SSL_CERT')
    ssl_key = os.environ.get('SSL_KEY')

    ssl_context=None
    # if ssl_cert is not None and ssl_key is not None:
    #    print('Using ssl cert from {}'.format(ssl_cert))
    #    ssl_context = (ssl_cert, ssl_key)
    
    app.run(host='localhost', debug=args.debug, port=args.port, ssl_context=ssl_context)

if __name__ == '__main__':
    main()
