from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message="Passwords must match.")
    ])
    name = StringField("Account Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    subscription = SelectField("Subscription Model", choices=[
        ("free", "Free"),
        ("basic", "Basic"),
        ("premium", "Premium")
    ])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[
            DataRequired(message="Username is required"), 
            Length(min=4, max=25)
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(message="Password is required")]
    )
    submit = SubmitField('Login')


class UserForm(FlaskForm):
    user_id = HiddenField()
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(), EqualTo('password', message="Passwords must match.")
    ])
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    is_admin = SelectField("Admin Privileges", choices=[
        ("True", "Yes"),
        ("False", "No")
    ], validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserFormUpdate(FlaskForm):
    user_id = HiddenField()
    username = StringField("Username")
    password = PasswordField("Password")
    confirm_password = PasswordField("Confirm Password", validators=[
        EqualTo('password', message="Passwords must match.")
    ])
    name = StringField("Full Name")
    email = StringField("Email", validators=[Email()])
    is_admin = SelectField("Admin Privileges", choices=[
        ("True", "Yes"),
        ("False", "No")
    ])
    submit = SubmitField("Submit")