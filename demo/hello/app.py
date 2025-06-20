import click    # 添加click命令
from flask import Flask # flask程序

app = Flask(__name__) # 程序实例,Python会根据所处的模块来赋予__name__变量相应的值

@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'

@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'

@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return f'<h1>Hello, {name}!</h1>'


# 新增flask cli命令
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')


if __name__ == '__main__':
    app.run(debug=True)