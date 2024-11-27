from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.orders import OrderForm
import pandas as pd
import json
from app.scripts.log import event_logging

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


#------------
@orders_blueprint.route('/orders_add', methods=['GET', 'POST'])
@login_required
def orders_add():
    db = current_app.db
    products_db = list(db.products.find())  # Get products from the database
    orders = list(db.orders.find())  # Fetch all orders records
    form = OrderForm()

    if request.method == 'POST':
        print("form validated")        
        products_data = request.form.get('products')

        products_count = products_data.count('product_name')
        products_data_final = []
        for i in range(0, products_count):  # Loop through the product fields
            product = {
                'product_name': request.form.get(f'products[{i}][product_name]'),
                'product_type': request.form.get(f'products[{i}][product_type]'),
                'quantity': request.form.get(f'products[{i}][quantity]'),
                'price': request.form.get(f'products[{i}][price]'),
                'total': request.form.get(f'products[{i}][total]'),
            }
            products_data_final.append(product)
        
        # Ensure you have products data before proceeding
        if not products_data_final:
            flash("Please add at least one product.", "danger")
        else:
            total_price = []
            for p in products_data_final:
                total_price.append(float(p['total']))
            total_price = sum(total_price)
            # total_price = None
            new_order = {
                'date_inserted': datetime.now(),
                'date_of_order': request.form.get('date_of_order'),
                'products': products_data_final,
                'customer': request.form.get('customer_name'),
                'total_price': total_price,
            }
            print(f"new order: {new_order}")
            try:
                result = db.orders.insert_one(new_order)  # Save the new order directly to MongoDB
                flash("Order successfully added.", "success")
                event_logging(
                    event_var="adding orders",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=result.inserted_id,
                    old_doc=None,
                    new_doc=None,
                    error=None
                )
                # return redirect(url_for('orders_blueprint.orders_add'))
            except Exception as e:
                flash("Order not saved", "danger")
                flash(form.errors)
                print(form.errors)
                event_logging(
                    event_var="adding order error",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=None,
                    old_doc=None,
                    new_doc=None,
                    error=e
                )
    return render_template('orders_add.html', products_db=products_db, orders=orders, form=form)

#------------


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
