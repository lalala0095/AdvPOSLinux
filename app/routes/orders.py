from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.orders import OrderForm
import pandas as pd

orders_blueprint = Blueprint('orders_blueprint', __name__)

@orders_blueprint.route('/orders_records', methods=['GET', 'POST'])
@login_required
def orders():
    db = current_app.db

    orders_records = list(db.orders.find())
    products = list(db.products.find())

    # Fetch all orders records from the database
    orders_records = list(db.orders.find())
    return render_template('orders.html', orders_records=orders_records, products=products)

@orders_blueprint.route('/orders_add', methods=['GET', 'POST'])
@login_required
def orders_add():
    db = current_app.db
    products = list(db.products.find())
    orders = list(db.orders.find())  # Fetch all orders records
    form = OrderForm()

    if not form.validate_on_submit():
        print("Form validation failed!")
        print(form.errors)  # This will show any validation errors
    else:
        if form.validate_on_submit():
            print("Form validated!")

            # Retrieve product details from the form
            products_data = []
            for product in form.products.data:
                product_data = {
                    'product_name': product.get('product_name'),
                    'product_type': product.get('product_type'),
                    'quantity': int(product.get('quantity')) ,
                    'price': float(product.get('price')),
                    'total': float(product.get('total')),
                }
                products_data.append(product_data)

            date_of_order = form.date_of_order.data
            date_of_order = pd.to_datetime(date_of_order)
            # Create the order record
            new_record = {
                'date_inserted': datetime.now(),
                'date_of_order': date_of_order,
                'products': products_data,
                'customer': form.customer_name.data,
                'total_price': sum(p['total'] for p in products_data),  # Calculate total price
            }

            try:
                db.orders.insert_one(new_record)
                flash("Order added successfully!", "success")
                return redirect(url_for('orders_blueprint.orders_add'))
            except Exception as e:
                flash(f"Database error: {str(e)}", "danger")


            
        # if request.method == 'POST':
        #     for field, errors in form.errors.items():
        #         for error in errors:
        #             flash(f"Error in {getattr(form, field).label.text}: {error}", "danger")
        # else:
        #     print(form.errors)
        #     for field, errors in form.errors.items():
        #         for error in errors:
        #             print(f"Error in {getattr(form, field).label.text}: {error}")
        #     flash("All fields are required!", "danger")


        # flash("All fields are required!", "danger")

    return render_template('orders_add.html', products=products, orders=orders, form=form)

# Route to delete a orders record
@orders_blueprint.route('/orders_delete/<string:record_id>', methods=['POST'])
@login_required
def orders_delete(record_id):
    db = current_app.db
    try:
        db.orders.delete_one({"_id": ObjectId(record_id)})
        flash("Orders record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('orders_blueprint.orders'))

@orders_blueprint.route('/orders_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def orders_edit(record_id):
    db = current_app.db
    record = db.orders.find_one({"_id": ObjectId(record_id)})
    products = list(db.products.find())

    if not record:
        flash("Orders record not found!", "danger")
        return redirect(url_for('orders_blueprint.orders'))

    if request.method == 'POST':
        date_of_order = request.form.get('order_date')
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_type = request.form.get('product_type')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if product_name and quantity and price:
            updated_record = {
                "date_of_order": date_of_order,
                "product_id": product_id,
                "product_name": product_name,
                "quantity": int(quantity),
                "product_type": product_type,
                "price": float(price),
                "total": int(quantity) * float(price),
            }
            try:
                db.orders.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
                flash("Orders record updated successfully!", "success")
            except Exception as e:
                flash(f"Error updating record: {e}", "danger")
            return redirect(url_for('orders_blueprint.orders'))

        flash("All fields are required!", "danger")

    return render_template('orders_edit.html', record=record, products=products)
