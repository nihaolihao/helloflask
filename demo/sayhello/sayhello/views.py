from flask import Flask, render_template,redirect,flash, url_for

from sayhello import app, db
from sayhello.models import Message
from sayhello.forms import HelloForm

@app.route('/',methods=['GET', 'POST'])
def index():
    # 加载所有的记录
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent to the world!')
        return redirect(url_for('index'))
    return render_template('index.html', messages=messages, form=form)