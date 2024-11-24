from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required

sales_blueprint = Blueprint('sales_blueprint', __name__)

@sales_blueprint.route('/sales_records', methods=['GET', 'POST'])
@login_required
def sales():
    db = current_app.db

    sales_records = list(db.sales.find())
    products = list(db.products.find())

    # Fetch all sales records from the database
    sales_records = list(db.sales.find())
    return render_template('sales.html', sales_records=sales_records, products=products)

@sales_blueprint.route('/sales_add', methods=['GET', 'POST'])
@login_required
def sales_add():
    db = current_app.db
    products = list(db.products.find())
    sales = list(db.sales.find())  # Fetch all sales records

    if request.method == 'POST':
        # Handle form submission for adding sale
        date_inserted = datetime.now()
        date_of_sale = request.form.get('sale_date')
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_type = request.form.get('product_type')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        if product_name and quantity and price:
            new_record = {
                "date_inserted": date_inserted,
                "date_of_sale": date_of_sale,
                "product_id": product_id,
                "product_name": product_name,
                "quantity": int(quantity),
                "product_type": product_type,
                "price": float(price),
                "total": int(quantity) * float(price)
            }
            db.sales.insert_one(new_record)
            flash("Sales record added successfully!", "success")
            return redirect(url_for('sales_blueprint.sales_add'))  # Stay on the same page to show updated records

        flash("All fields are required!", "danger")

    return render_template('sales_add.html', products=products, sales=sales)

# Route to delete a sales record
@sales_blueprint.route('/sales_delete/<string:record_id>', methods=['POST'])
@login_required
def sales_delete(record_id):
    db = current_app.db
    try:
        db.sales.delete_one({"_id": ObjectId(record_id)})
        flash("Sales record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('sales_blueprint.sales'))

@sales_blueprint.route('/sales_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def sales_edit(record_id):
    db = current_app.db
    record = db.sales.find_one({"_id": ObjectId(record_id)})
    products = list(db.products.find())

    if not record:
        flash("Sales record not found!", "danger")
        return redirect(url_for('sales_blueprint.sales'))

    if request.method == 'POST':
        date_of_sale = request.form.get('sale_date')
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        product_type = request.form.get('product_type')
        quantity = request.form.get('quantity')
        price = request.form.get('price')

        if product_name and quantity and price:
            updated_record = {
                "date_of_sale": date_of_sale,
                "product_id": product_id,
                "product_name": product_name,
                "quantity": int(quantity),
                "product_type": product_type,
                "price": float(price),
                "total": int(quantity) * float(price),
            }
            try:
                db.sales.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
                flash("Sales record updated successfully!", "success")
            except Exception as e:
                flash(f"Error updating record: {e}", "danger")
            return redirect(url_for('sales_blueprint.sales'))

        flash("All fields are required!", "danger")

    return render_template('sales_edit.html', record=record, products=products)
