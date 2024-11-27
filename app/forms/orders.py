from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField, SelectField, FormField, IntegerField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class ProductForm(FlaskForm):
    product_name = StringField("Product Name", validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    price = DecimalField('Price', validators=[Optional()])
    product_type = StringField("Product Type")
    total = DecimalField("Total Price", default=0, validators=[Optional ()])
    class Meta:
        csrf = False
    def calculate_total(self):
        return self.quantity.data * self.price.data

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
    # total = price * quantity

class OtherChargesToCustomer(FlaskForm):
    charge_name = StringField("Charge to Customer Name", validators=[Optional()])
    quantity = IntegerField("Quantity", validators=[Optional()])
    price = DecimalField("Price", validators=[Optional()])
    # total = price * quantity

class OrderForm(FlaskForm):
    date_of_order = DateField("Date Ordered", validators=[DataRequired()])
    products = FieldList(FormField(ProductForm), min_entries=1)
    customer_name = StringField("Customer", validators=[Optional()])
    # customer = FormField(CustomerForm)    
    # deductions = FieldList(FormField(Deductions), validators=[Optional()])
    # charges_to_customer = FieldList(FormField(OtherChargesToCustomer), validators=[Optional()])
    # total_price = DecimalField("Total Price", validators=[Optional()])
    submit = SubmitField("Submit Order")
    # status = SelectField("Order Status", choices=[("", "Select Status"),
    #                                         "Active",     
    #                                         "Awaiting Payment",
    #                                         "Sold",
    #                                         "Cancelled"], validators=[Optional()])
    # custom_status = StringField("Custom Status", validators=[Optional()])
    # date_sold = DateField("Date Sold", validators=[Optional()])
    # date_cancelled = DateField("Date Cancelled", validators=[Optional()])
    # date_of_payment = DateField("Date Of Payment", validators=[Optional()])

    # def validate(self, extra_validators=True):
    #     if not super().validate():
    #         return False
        
    #     # Validate products (e.g., ensure they have valid data)
    #     for product in self.products:
    #         if not product.product_name.data or not product.quantity.data or not product.price.data:
    #             self.products.errors.append("Product name, quantity, and price are required.")
    #             return False

    #     return True