from flask import Flask, render_template, jsonify, request, abort, redirect, g


app = Flask(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/fib/<int:number>')
def fibonacci_method(number):
    fibonacci = []
    x = 0
    y = 1
    num = number
    for n in range(num):
        fibonacci.append(x + y)
        aux = x + y
        x = y
        y = aux
    return 'Sucesion = %s' % fibonacci

@app.route('/fib/<int:number>/json')
def fibonacci_json(number):
    fibonacci = []
    x = 0
    y = 1
    num = number
    for n in range(num):
        fibonacci.append(x + y)
        aux = x + y
        x = y
        y = aux
    return jsonify(fibonacci)

if __name__ == '__main__':
    app.run()
