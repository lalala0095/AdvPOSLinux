from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Length, Optional, NumberRange
from datetime import datetime

class BillerForm(FlaskForm):
    biller_name = StringField("Biller Name", validators=[DataRequired()])
    biller_type = SelectField("Type", choices=[
        ("Utilities", "Utilities"),
        ("Rent", "Rent"),
        ("Loan", "Loan"),
        ("Credit Card", "Credit Card"),
        ("Investment/Insurance", "Investment/Insurance"),
        ("Insurance", "Investment"),
        ("Others", "Others")
    ], validators=[DataRequired()])
    custom_type = StringField("Custom Type (Optional)", validators=[Optional()])
    usual_due_day = IntegerField("Usual Due Date Day", validators=[
        Optional(), 
        NumberRange(min=1, max=31, message="The day must be between 1 and 31")])
    remarks = TextAreaField("Remarks", validators=[Optional()])
    submit = SubmitField("Submit")

class CashFlowForm(FlaskForm):
    cash_flow_name = StringField("Cash Flow Name", validators=[DataRequired()])
    cash_flow_type = SelectField("Type", choices=[
        ("Salary", "Salary"),
        ("Business Income", "Business Income"),
        ("Bank Balance", "Bank Balance"),
        ("Cash Balance", "Cash Balance"),
        ("Commission", "Commission"),
        ("Projection", "Projection"),
        ("Others", "Others")
    ], validators=[DataRequired()])
    usual_income_day = IntegerField("Usual Income Date Day", validators=[
        Optional(), 
        NumberRange(min=1, max=31, message="The day must be between 1 and 31")])
    custom_type = StringField("Custom Type (Optional)", validators=[Optional()])
    remarks = TextAreaField("Remarks", validators=[Optional()])
    submit = SubmitField("Submit")


class PaymentMethodForm(FlaskForm):
    payment_method_name = StringField("Payment Method Name", validators=[DataRequired()])
    payment_method_type = SelectField("Type", choices=[
        ("Bank Transfer", "Bank Transfer"),
        ("E-wallet", "E-wallet"),
        ("Cash", "Cash"),
        ("Credit Card", "Credit Card"),
        ("Cheque", "Cheque"),
        ("Others", "Others")
    ], validators=[DataRequired()])
    urgency = SelectField("Urgency", choices=[
        ("Urgent", "Urgent"),
        ("Normal", "Normal"),
        ("Low", "Low")
    ], validators=[DataRequired()])
    custom_type = StringField("Custom Type (Optional)", validators=[Optional()])
    remarks = TextAreaField("Remarks", validators=[Optional()])
    submit = SubmitField("Submit")

class BillForm(FlaskForm):
    bill_name = SelectField("Bill Name", validators=[DataRequired()], choices=[])
    bill_urgency = SelectField("Urgency", choices=[
        ("Urgent", "Urgent"),
        ("Normal", "Normal"),
        ("Low", "Low")
    ], validators=[Optional()])
    due_date = DateField("Due Date", validators=[Optional()])
    remarks = TextAreaField("Remarks", validators=[Optional()])
    submit = SubmitField("Submit")

def populate_biller(form):
    db = current_app.db
    coll = db['billers'].find({}, {"_id": 0, "biller_name": 1})
    list_of_billers = list(coll)
    print(f"collection: {list(coll)}")
    print(type(list(coll)))

    choices = []
    for biller in list_of_billers:
        print(biller)
        print(f"biller in the collection: {biller}")
        choices.append(biller['biller_name'])
    
    print(choices)
    form.bill_name.choices = choices
