class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[
                        DataRequired(), Email(), Length(1, 254)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('')
