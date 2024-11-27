from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField, SelectField, FormField, IntegerField, DecimalField, DateField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, InputRequired

class CustomerForm(FlaskForm):
    customer_name = StringField("Customer Name", validators=[Optional()])
    address = StringField('Customer Address', validators=[Optional()])
    shipping_address = StringField('Shipping Address', validators=[Optional()])
    company_name = StringField('Company Name', validators=[Optional()])
    contact_number = StringField('Contact Number', validators=[Optional()])
    email = StringField('Email', validators=[Optional()])

class Deductions(FlaskForm):
    deduction_name = StringField("Deduction Name", validators=[Optional()])
    quantity = IntegerField("Quantity", validators=[Optional()])
    price = DecimalField("Price", validators=[Optional()])

class OtherChargesToCustomer(FlaskForm):
    charge_name = StringField("Charge to Customer Name", validators=[Optional()])
    quantity = IntegerField("Quantity", validators=[Optional()])
    price = DecimalField("Price", validators=[Optional()])

class ProductForm(FlaskForm):
    product_name = StringField("Product Name", validators=[InputRequired()])
    product_type = StringField("Product Type")
    quantity = IntegerField("Quantity", validators=[InputRequired()])
    price = FloatField("Price", validators=[InputRequired()])
    total = FloatField("Total", validators=[InputRequired()])
    class Meta:
        csrf = False
    def calculate_total(self):
        return self.quantity.data * self.price.data

class OrderForm(FlaskForm):
    date_of_order = DateField("Date Ordered", validators=[DataRequired()])
    products = FieldList(FormField(ProductForm), min_entries=1)
    customer_name = StringField("Customer", validators=[Optional()])
    submit = SubmitField("Submit Order")
