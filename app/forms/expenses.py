from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField, DateField, FloatField
from wtforms.validators import DataRequired, Optional

class ExpensesForm(FlaskForm):
    date_of_transaction = DateField("Date of Transaction", validators=[DataRequired()])
    description = StringField("Items or Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    type_of_expense = SelectField("Type", choices=[
        ('', 'Select an option'),
        ("Needs", "Needs"),
        ("Wants", "Wants")
    ], validators=[DataRequired()])
    platform = SelectField("Platform", choices=[
        ('', 'Select an option'),
        ("Shopee", "Shopee"),
        ("Tiktok", "Tiktok"),
        ("Lazada", "Lazada"),
        ("Physical Store", "Physical Store"),
        ("Others", "Others")
    ], validators=[Optional()])
    store = StringField("Store")
    payment_method = StringField("Payment Method")
    remarks = StringField("Remarks")
    submit = SubmitField("Submit")

class ExpensesUpdateForm(FlaskForm):
    date_of_transaction = DateField("Date of Transaction")
    description = StringField("Items or Description")
    price = FloatField("Price")
    type_of_expense = SelectField("Type", choices=[
        ('', 'Select Type'),
        ("Needs", "Needs"),
        ("Wants", "Wants")
    ], validators=[Optional()])
    platform = SelectField("Platform", choices=[
        ('', 'Select a Platform'),
        ("Shopee", "Shopee"),
        ("Tiktok", "Tiktok"),
        ("Lazada", "Lazada"),
        ("Physical Store", "Physical Store"),
        ("Others", "Others")
    ], validators=[Optional()])
    store = StringField("Store")
    payment_method = StringField("Payment Method")
    remarks = StringField("Remarks")
    submit = SubmitField("Submit")
