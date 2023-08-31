from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo

#registation form deployment
class RegisterForm(FlaskForm):
    email = EmailField(label='email',validators=[DataRequired(),Email()])
    name = StringField(label='username',validators=[DataRequired()])
    passwrd = PasswordField(label='password', validators=[DataRequired(),Length(min=6)])
    confirm = PasswordField(label='confirm password', validators=[EqualTo(fieldname='passwrd'),DataRequired(),])
    submit = SubmitField(label='register')


class LoginForm(FlaskForm):
    email = EmailField(label='email',validators=[DataRequired(),Email()])
    passwrd = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='login')