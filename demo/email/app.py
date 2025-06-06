import os
from threading import Thread

import sendgrid
from sendgrid.helpers.mail import Email as SGEmail, Content, Mail as SGMail
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask import Flask, flash, render_template, request, redirect, url_for

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY', 'secret string'),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_USE_SSL=True,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
)

mail = Mail(app)

# send over SMTP
def send_smtp_mail(subject, to ,body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)

# send over SengGrid Web API
def send_api_mail(subject, to, body):
    sg = sendgrid.SengGridAPIClient(os.getenv('SENGGRID_API_KEY'))
    from_email = os.getenv('MAIL_DEFAULT_SENDER')
    to_email = SGEmail(to)
    content = Content('text/plain', body)
    email = SGMail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=email.get())

# send email asynchronously
def _send_async_email(app, message):
    with app.app_context():
        mail.send(message)

def send_async_mail(subject, to, body):
    # app = current_app._get_current_object()
    message = Message(subject, recipients=[to], body=body)
    thr = Thread(target=_send_async_email, args=[app, message])
    thr.start()
    return thr

# send email with HTML body
def send_subscribe_mail(subject, to, **kwargs):
    message = Message(subject, recipients=[to], sender='Flask Weekly <%s>' % os.getenv('MAIL_USERNAME'))
    message.body = render_template('emails/subscribe.txt',**kwargs)
    message.html = render_template('emails/subscribe.html',**kwargs)
    mail.send(message)

class EmailForm(FlaskForm):
    to = StringField('To', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit_smtp = SubmitField('Send with SMTP')
    submit_api = SubmitField('Send with SengGrid API')
    submit_async = SubmitField('Send with SMTP asynchronously')

class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if form.validate_on_submit():
        to = form.to.data
        subject = form.subject.data
        body = form.body.data
        if form.submit_smtp.data:
            send_smtp_mail(subject, to, body)
            method = request.form.get('submit_smtp')
        elif form.submit_api.data:
            send_api_mail(subject, to, body)
            method = request.form.get('submit_api')
        else:
            send_async_mail(subject, to, body)
            method = request.form.get('submit_async')

        flash('Email sent %s! Check your inbox.' % ' '.join(method.split()[1:]))
        return redirect(url_for('index'))
    form.subject.data = 'Hello World!'
    form.body.data = 'Across the Great Wall we can reach every corner in the world.'
    return render_template('index.html', form=form)

@app.route('/subscribe',methods=['GET', 'POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        send_subscribe_mail('Subscribe to Success!',email,name=name)
        flash('Confirmation email have been sent! Check your inbox.')
        return redirect(url_for('subscribe'))
    return render_template('subscribe.html', form=form)

@app.route('/unsubscribe')
def unsubscribe():
    flash('Want to unsubscribe? No Way...')
    return redirect(url_for('subscribe'))


if __name__ == '__main__':
    app.run(debug=True)