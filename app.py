import flask

app = flask.Flask('__name__')

@app.errorhandler(404)
def not_found(e):
    return flask.render_template('404.j2'), 404

@app.route('/')
def index():
    return flask.render_template('index.j2')


def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
