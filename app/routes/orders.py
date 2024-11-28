from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.orders import OrderForm, OrderEditForm
import pandas as pd
import json
from app.scripts.log import event_logging
from werkzeug.datastructures import MultiDict

orders_blueprint = Blueprint('orders_blueprint', __name__)

@orders_blueprint.route('/orders_records', methods=['GET', 'POST'])
@login_required
def orders():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    products = list(db.products.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))

    # Fetch all orders records from the database
    raw_orders = list(db.orders.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))

    # Transform the raw orders into the desired structure
    orders_records = []
    for order in raw_orders:
        # Extract order fields
        order_data = {
            "_id": str(order["_id"]),  # Convert ObjectId to string for template compatibility
            "date_of_order": order.get("date_of_order"),
            "customer": order.get("customer", "N/A"),
            "status": order.get('status', None),
            "custom_status": order.get('custom_status', None),
            "date_sold": order.get('date_sold', None),
            "date_cancelled": order.get('date_cancelled', None),
            "date_of_payment": order.get('date_of_payment', None),
            "total_products_price": order.get("total_products_price", 0),
            "total_charges": order.get("total_charges", 0),
            "total_deductions": order.get("total_deductions", 0),
            "products": order.get("products", []),
            "charges": order.get("charges", []),
            "deductions": order.get("deductions", [])
        }

        # Append the processed order to the list
        orders_records.append(order_data)
    return render_template('orders.html', orders_records=orders_records, products=products)


#------------
@orders_blueprint.route('/orders_add', methods=['GET', 'POST'])
@login_required
def orders_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db
    products_db = list(db.products.find(
        {
            "account_id": account_id,
            "user_id": user_id
        }
    ))  # Get products from the database
    orders = list(db.orders.find({
        "account_id": account_id,
        "user_id": user_id
    }))  # Fetch all orders records
    form = OrderForm()

    if request.method == 'POST':
        print("form validated")        
        products_data = request.form.get('products')
        deductions_data = request.form.get('deductions')
        charges_data = request.form.get('charges')

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

        try:
            charges_count = charges_data.count('charges_name')
        except Exception as e:
            print(e)
            charges_count = 0
        charges_data_final = []
        for i in range(0, charges_count):  # Loop through the charge fields
            charge = {
                'charge_name': request.form.get(f'charges[{i}][charges_name]'),
                'quantity': request.form.get(f'charges[{i}][quantity]'),
                'price': request.form.get(f'charges[{i}][price]'),
                'total': request.form.get(f'charges[{i}][total]'),
            }
            charges_data_final.append(charge)
        try:
            deductions_count = deductions_data.count('deductions_name')
        except Exception as e:
            print(e)
            deductions_count = 0

        deductions_data_final = []
        for i in range(0, deductions_count):  # Loop through the deduction fields
            deduction = {
                'deduction_name': request.form.get(f'deductions[{i}][deductions_name]'),
                'quantity': request.form.get(f'deductions[{i}][quantity]'),
                'price': request.form.get(f'deductions[{i}][price]'),
                'total': request.form.get(f'deductions[{i}][total]'),
            }
            deductions_data_final.append(deduction)

        # Ensure you have products data before proceeding
        if not products_data_final:
            flash("Please add at least one product.", "danger")
        else:
            total_price = []
            total_deductions = []
            total_charges = []

            for p in products_data_final:
                total_price.append(float(p['total']))
            total_price = sum(total_price)

            for p in deductions_data_final:
                total_deductions.append(float(p['total']))
            total_deductions = sum(total_deductions)

            for p in charges_data_final:
                total_charges.append(float(p['total']))
            total_charges = sum(total_charges)

            new_order = {
                'date_inserted': datetime.now(),
                'user_id': session.get('user_id'),
                'account_id': session.get('account_id'),
                'date_of_order': request.form.get('date_of_order'),
                'products': products_data_final,
                'total_products_price': total_price,
                'customer': {
                    'customer_name': request.form.get('customer-customer_name'),
                    'address': request.form.get('customer-address'),
                    'shipping_address': request.form.get('customer-shipping_address'),
                    'company_name': request.form.get('customer-company_name'),
                    'contact_number': request.form.get('customer-contact_number'),
                    'email': request.form.get('customer-email'),

                },
                'deductions': deductions_data_final,
                'total_deductions': total_deductions,
                'charges': charges_data_final,
                'total_charges': total_charges,
                'status': request.form.get('status'),
                'custom_status': request.form.get('custom_status'),
                'date_sold': request.form.get('date_sold'),
                'date_cancelled': request.form.get('date_cancelled'),
                'date_of_payment': request.form.get('date_of_payment'),
                'net_price': (total_price + total_charges) - total_deductions
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
    account_id = session['account_id']
    user_id = session['user_id']

    db = current_app.db
    record = db.orders.find_one({"_id": ObjectId(record_id)})
    products_db = list(db.products.find(
        {
            "account_id": account_id,
            "user_id": user_id
        }
    ))  # Fetch available products for dropdowns

    fields = [
            'date_of_order',
            'products',
            'customer',    
            'deductions',
            'charges',
            'total_price',
            'status',
            'custom_status'
            'date_sold',
            'date_cancelled',
            'date_of_payment' 
    ]

    if not record:
        flash("Order record not found!", "danger")
        return redirect(url_for('orders_blueprint.orders'))

    date_inserted = datetime.now()
    primary_fields = {
        'date_inserted': record.get('date_inserted'),
        'account_id': session.get('account_id'),
        'user_id': session.get('user_id'),
        'date_updated': datetime.now()     
    }

    data = {}
    products_len = len(record.get('products'))

    for field in fields:
        data[field] = record.get(field)

    try:
        data['date_of_order'] = pd.to_datetime(data['date_of_order'], format="%Y-%m-%d")
    except Exception as e:
        print(f"date_of_transaction error: {e}")
    if record.get('date_sold'):
        data['date_sold'] = pd.to_datetime(record.get('date_sold'), format="%Y-%m-%d")
    else:
        data['date_sold'] = None
        print(f"date_sold error")
    if record.get('date_cancelled'):
        data['date_cancelled'] = pd.to_datetime(record.get('date_cancelled'), format="%Y-%m-%d")
    else:
        data['date_cancelled'] = None
        print(f"date_cancelled error")
    if record.get('date_of_payment'):
        data['date_of_payment'] = pd.to_datetime(record.get('date_of_payment'), format="%Y-%m-%d")
    else:
        data['date_of_payment'] = None
        print(f"date_of_payment error")

    data['custom_status'] = record.get('custom_status')


    primary_fields.update(data)

    formdata = MultiDict(primary_fields)
    form = OrderEditForm(data=formdata)

    # save data from edits
    if request.method == 'POST':
        print("form validated")        
        products_data = request.form.get('products')
        deductions_data = request.form.get('deductions')
        print(deductions_data)
        print(type(deductions_data))
        charges_data = request.form.get('charges')
        print(charges_data)
        print(type(charges_data))
        
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

        try:
            charges_count = charges_data.count('charge_name')
        except Exception as e:
            print(e)
            charges_count = 0
        charges_data_final = []
        for i in range(0, charges_count):  # Loop through the charge fields
            charge = {
                'charge_name': request.form.get(f'charges[{i}][charge_name]'),
                'quantity': request.form.get(f'charges[{i}][quantity]'),
                'price': request.form.get(f'charges[{i}][price]'),
                'total': request.form.get(f'charges[{i}][total]'),
            }
            charges_data_final.append(charge)
        try:
            deductions_count = deductions_data.count('deduction_name')
        except Exception as e:
            print(e)
            deductions_count = 0

        deductions_data_final = []
        for i in range(0, deductions_count):  # Loop through the deduction fields
            deduction = {
                'deduction_name': request.form.get(f'deductions[{i}][deduction_name]'),
                'quantity': request.form.get(f'deductions[{i}][quantity]'),
                'price': request.form.get(f'deductions[{i}][price]'),
                'total': request.form.get(f'deductions[{i}][total]'),
            }
            deductions_data_final.append(deduction)

        # Ensure you have products data before proceeding
        if not products_data_final:
            flash("Please add at least one product.", "danger")
        else:
            total_price = []
            total_deductions = []
            total_charges = []

            for p in products_data_final:
                total_price.append(float(p['total']))
            total_price = sum(total_price)

            for p in deductions_data_final:
                total_deductions.append(float(p['total']))
            total_deductions = sum(total_deductions)

            for p in charges_data_final:
                total_charges.append(float(p['total']))
            total_charges = sum(total_charges)

            new_order = {
                'date_inserted': record.get('date_inserted'),
                'user_id': session.get('user_id'),
                'account_id': session.get('account_id'),
                'date_of_order': request.form.get('date_of_order'),
                'products': products_data_final,
                'total_products_price': total_price,
                'customer': {
                    'customer_name': request.form.get('customer-customer_name'),
                    'address': request.form.get('customer-address'),
                    'shipping_address': request.form.get('customer-shipping_address'),
                    'company_name': request.form.get('customer-company_name'),
                    'contact_number': request.form.get('customer-contact_number'),
                    'email': request.form.get('customer-email'),

                },
                'deductions': deductions_data_final,
                'total_deductions': total_deductions,
                'charges': charges_data_final,
                'total_charges': total_charges,
                'status': request.form.get('status'),
                'custom_status': request.form.get('custom_status'),
                'date_sold': request.form.get('date_sold'),
                'date_cancelled': request.form.get('date_cancelled'),
                'date_of_payment': request.form.get('date_of_payment'),
                'net_price': (total_price + total_charges) - total_deductions,
                'date_updated': datetime.now()
            }
            print(f"new order: {new_order}")
            try:
                result = db.orders.update_one({"_id": ObjectId(record_id)}, {"$set": new_order})
                flash("Order successfully modified.", "success")
                event_logging(
                    event_var="update orders",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=ObjectId(record_id),
                    old_doc=record,
                    new_doc=new_order,
                    error=None
                )
                # return redirect(url_for('orders_blueprint.orders_add'))
            except Exception as e:
                flash("Order not saved", "danger")
                flash(form.errors)
                print(form.errors)
                event_logging(
                    event_var="updating order error",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=ObjectId(record_id),
                    old_doc=record,
                    new_doc=None,
                    error=e
                )
            return redirect(url_for('orders_blueprint.orders'))

    return render_template(
        'orders_edit.html',
        record=record,
        products_db=products_db,
        form=form,
        products_len=products_len
    )
