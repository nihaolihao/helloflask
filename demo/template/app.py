import os
from flask import Flask, flash, redirect, render_template, url_for
from markupsafe import Markup

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY','secret string')
# app.jinja_env.variable_start_string = '[['
# app.jinja_env.variable_end_string = ']]'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)

@app.route('/')
def index():
    return render_template('index.html')

@app.context_processor
def inject_info():
    foo = 'I am foo.'
    return dict(foo=foo)

@app.template_global()
def bar():
    return 'I am bar.'

@app.template_filter()
def musical(s):
    return s + Markup(' &#9835;')

@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False

@app.route('/watchlist2')
def watchlist_with_static():
    return render_template('watchlist_with_static.html',user=user,movies=movies)

@app.route('/flash')
def just_flash():
    flash('I am flash, who is looking for me?')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)