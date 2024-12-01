from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField, DateField, FloatField, FieldList
from wtforms.validators import DataRequired, EqualTo, Length, Optional, NumberRange
from datetime import datetime
from bson import ObjectId
import pandas as pd

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
    amount = FloatField("Amount", validators=[DataRequired()])
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
    custom_type = StringField("Custom Type (Optional)", validators=[Optional()])
    usual_income_day = IntegerField("Usual Income Date Day", validators=[
        Optional(), 
        NumberRange(min=1, max=31, message="The day must be between 1 and 31")])
    amount = FloatField("Amount", validators=[DataRequired(),NumberRange(message="Number must be a decimal number.")])    
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
    amount = FloatField("Amount", validators=[Optional()])
    allocation = FloatField("Allocation", default=0, validators=[Optional()])
    remarks = TextAreaField("Remarks", validators=[Optional()])
    submit = SubmitField("Submit")

def populate_biller(form):
    db = current_app.db
    coll = db['billers'].find({}, {"_id": 1, "biller_name": 1})
    choices = [("", "Select Biller")]
    choices.extend([(str(biller['_id']), biller["biller_name"]) for biller in coll]) 
    form.bill_name.choices = choices


# def populated_amount(form, object_id):
#     db = current_app.db
#     coll = db['billers']
#     record_object = coll.find({"_id": ObjectId(object_id)})
#     amount = record_object.get('amount', 0)
#     if amount:
#         form.amount.data = amount

class BillsPlannerForm(FlaskForm):
    bills_planner_name = StringField("Bills", validators=[DataRequired()])
    bills = FieldList(SelectField("Bills", choices=[], validators=[DataRequired()]), min_entries=1)
    cash_flows = FieldList(SelectField("Cash Flows", choices=[], validators=[DataRequired()]), min_entries=1)
    submit = SubmitField("Submit")

def populate_bills(form, cash_flows_db):
    choice_initial = ("", "Select one from Bills")
    choices = []
    choices.append(choice_initial)
    for bill in cash_flows_db:
        print("appending")
        bill_id = str(bill['_id'])
        bill_item = f"{bill['biller']["biller_name"]} due on {pd.to_datetime(bill["due_date"]).strftime("%b %d")}"
        bill_tuple = (bill_id, bill_item)
        print(bill_tuple)
        choices.append(bill_tuple) 
    form.bills[0].choices = choices
    print(choices)


def populate_cash_flows(form, cash_flows_db):
    choice_initial = ("", "Select one from Cash Flows")
    choices = []
    choices.append(choice_initial)
    for bill in cash_flows_db:
        bill_id = str(bill['_id'])
        bill_item = f"{bill["cash_flow_name"]} on {pd.to_datetime(bill["possible_next_month_date"]).strftime("%b %d")}"
        bill_tuple = (bill_id, bill_item)
        print(bill_tuple)
        choices.append(bill_tuple) 
    form.cash_flows[0].choices = choices
    print(choices)
    
