from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.cogs import COGsForm, COGsUpdateForm
import pandas as pd
from app.scripts.log import event_logging

cogs_blueprint = Blueprint('cogs_blueprint', __name__)

@cogs_blueprint.route('/cogs_records', methods=['GET', 'POST'])
@login_required
def cogs_records():
    db = current_app.db
   
    # Fetch all cogs records from the database
    cogs_records = list(db.cogs.find())
    return render_template('cogs.html', cogs_records=cogs_records)

@cogs_blueprint.route('/cogs_add', methods=['GET', 'POST'])
@login_required
def cogs_add():
    
    db = current_app.db
    cogs_records = list(db.cogs.find())
    form = COGsForm()

    if session.get('user_id'):
        user_id = session['user_id']
        account_id = session['account_id']
    else:
        user_id = None
        account_id = session['account_id']

    if form.validate_on_submit():
        db_count = db['cogs'].count_documents({})

    if request.method == 'POST':
        date_inserted = datetime.now()
        date_of_transaction = request.form.get('date_of_transaction')
        description = request.form.get('description')
        price = request.form.get('price')
        type_of_goods = request.form.get('type_of_goods')
        remarks = request.form.get('remarks ')

        new_record = {
            'date_inserted': date_inserted,
            'account_id': account_id,
            'user_id': user_id,
            'date_of_transaction': date_of_transaction,
            'description': description,
            'price': price,
            'type_of_goods': type_of_goods,
            'remarks': remarks
        }
        try:
            result = db.cogs.insert_one(new_record)
            result_id = result.inserted_id
            new_record['_id'] = result_id
            event_logging(event_var="cogs add",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=result_id,
                        old_doc=None,
                        new_doc=new_record,
                        error=None)
            flash("Cost of Goods record added successfully!", "success")
        except Exception as e:
            event_logging(event_var="cogs add",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=None,
                        old_doc=None,
                        new_doc=None,
                        error=e)
            flash(f"Error deleting record: {e}", "danger")

        return redirect(url_for('cogs_blueprint.cogs_add'))  # Stay on the same page to show updated records

    return render_template('cogs_add.html', form=form, cogs_records=cogs_records)


# Route to delete a cogs record
@cogs_blueprint.route('/cogs_delete/<string:record_id>', methods=['POST'])
@login_required
def cogs_delete(record_id):
    db = current_app.db
    record = db.cogs.find_one({"_id": ObjectId(record_id)})
    try:
        db.cogs.delete_one({"_id": ObjectId(record_id)})
        event_logging("cogs delete", session.get('user_id'), session.get('account_id'), record_id, record, None, None)
        flash("cogs record deleted successfully!", "success")
    except Exception as e:
        event_logging("cogs delete", session.get('user_id'), session.get('account_id'), record_id, record, record, e)
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('cogs_blueprint.cogs_records'))


@cogs_blueprint.route('/cogs_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def cogs_edit(record_id):
    db = current_app.db
    record = db.cogs.find_one({"_id": ObjectId(record_id)})
    cogs_records = list(db.cogs.find())

    if not record:
        flash("Cost of goods record not found!", "danger")
        return redirect(url_for('cogs_blueprint.cogs_records'))

    date_of_transaction = record.get('date_of_transaction')
    date_of_transaction = pd.to_datetime(date_of_transaction, format="%Y-%m-%d")
    print(type(date_of_transaction))

    form = COGsUpdateForm(data={
        'date_of_transaction': date_of_transaction,
        'description': record.get('description'),
        'price': record.get('price'),
        'type_of_goods': record.get('type_of_goods'),
        'remarks': record.get('remarks'),
    })

    if form.validate_on_submit():
        if session.get('user_id'):
            user_id = session['user_id']
            account_id = session['account_id']
        else:
            user_id = None
            account_id = session['account_id']

        
        # if request.method == 'POST':
        date_inserted = datetime.now()
        date_of_transaction = form.date_of_transaction.data
        description = form.description.data
        price = form.price.data
        type_of_goods = form.type_of_goods.data
        remarks = form.remarks.data

        updated_record = {
            'date_inserted': date_inserted,
            'account_id': account_id,
            'user_id': user_id,
            'date_of_transaction': date_of_transaction.strftime("%Y-%m-%d"),
            'description': description,
            'price': price,
            'type_of_goods': type_of_goods,
            'remarks': remarks,
            'date_updated': datetime.now()
        }

        try:
            db.cogs.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
            new_doc = db.cogs.find_one({"_id": ObjectId(record_id)})
            event_logging("cogs edit", session.get('user_id'), session.get('account_id'), record_id, record, new_doc, None)
            flash("User record updated successfully!", "success")
        except Exception as e:
            new_doc = db.cogs.find_one({"_id": ObjectId(record_id)})
            event_logging("cogs edit", session.get('user_id'), session.get('account_id'), record_id, record, new_doc, e)
            flash(f"Error updating record: {e}", "danger")
        return redirect(url_for('cogs_blueprint.cogs_records'))

    # Display errors if validation fails
    if request.method == 'POST':
        flash("Please correct the errors in the form.", "danger")

    return render_template('cogs_edit.html', form=form, record=record, cogs_records=cogs_records)
