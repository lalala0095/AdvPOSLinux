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
    class Meta:
        csrf = False

class Deductions(FlaskForm):
    deduction_name = StringField("Deduction Name", validators=[Optional()])
    quantity = IntegerField("Quantity", validators=[Optional()])
    price = DecimalField("Price", validators=[Optional()])
    class Meta:
        csrf = False
    def calculate_total(self):
        return self.quantity.data * self.price.data

class OtherChargesToCustomer(FlaskForm):
    charge_name = StringField("Charge to Customer Name", validators=[Optional()])
    quantity = IntegerField("Quantity", validators=[Optional()])
    price = DecimalField("Price", validators=[Optional()])
    class Meta:
        csrf = False

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


class OrderForm(FlaskForm):
    date_of_order = DateField("Date Ordered", validators=[DataRequired()])
    products = FieldList(FormField(ProductForm), min_entries=1)
    customer = FormField(CustomerForm, label="Customer Information (Optional)")    
    deductions = FieldList(FormField(Deductions), min_entries=0, label="Deductions (Optional)")
    charges = FieldList(FormField(OtherChargesToCustomer), min_entries=0, label="Charges to Customer (Optional)")
    total_price = DecimalField("Total Price", validators=[Optional()])
    submit = SubmitField("Submit Order")
    status = SelectField("Order Status", choices=[("", "Select Status"),
                                            ("Active", "Active"),     
                                            ("Awaiting Payment", "Awaiting Payment"),
                                            ("Sold", "Sold"),
                                            ("Cancelled", "Cancelled")], validators=[Optional()])
    custom_status = StringField("Custom Status", validators=[Optional()])
    date_sold = DateField("Date Sold", validators=[Optional()])
    date_cancelled = DateField("Date Cancelled", validators=[Optional()])
    date_of_payment = DateField("Date Of Payment", validators=[Optional()])

class OrderEditForm(FlaskForm):
    date_of_order = DateField("Date Ordered")
    products = FieldList(FormField(ProductForm), min_entries=1)
    customer = FormField(CustomerForm, label="Customer Information (Optional)")    
    deductions = FieldList(FormField(Deductions), min_entries=0, label="Deductions (Optional)")
    charges = FieldList(FormField(OtherChargesToCustomer), min_entries=0, label="Charges to Customer (Optional)")
    total_price = DecimalField("Total Price", validators=[Optional()])
    submit = SubmitField("Submit Order")
    status = SelectField("Order Status", choices=[("", "Select Status"),
                                            ("Active", "Active"),     
                                            ("Awaiting Payment", "Awaiting Payment"),
                                            ("Sold", "Sold"),
                                            ("Cancelled", "Cancelled")], validators=[Optional()])
    custom_status = StringField("Custom Status", validators=[Optional()])
    date_sold = DateField("Date Sold", validators=[Optional()])
    date_cancelled = DateField("Date Cancelled", validators=[Optional()])
    date_of_payment = DateField("Date Of Payment", validators=[Optional()])
