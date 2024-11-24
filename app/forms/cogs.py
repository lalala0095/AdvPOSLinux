from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField, DateField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class COGsForm(FlaskForm):
    date_of_transaction = DateField("Date of Transaction", validators=[DataRequired()])
    description = StringField("Items or Description", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    type_of_goods = SelectField("Type of Goods", choices=[
        "Raw Materials",
        "Packaging",
        "Transportation Expense",
        "Courier Service",
        "Others"
    ])
    remarks = StringField("Remarks")
    submit = SubmitField("Submit")

class COGsUpdateForm(FlaskForm):
    date_of_transaction = DateField("Date of Transaction")
    description = StringField("Items or Description")
    price = FloatField("Price")
    type_of_goods = SelectField("Type of Goods", choices=[
        "Raw Materials",
        "Packaging",
        "Transportation Expense",
        "Courier Service",
        "Others"
    ])
    remarks = StringField("Remarks")
    submit = SubmitField("Submit")
