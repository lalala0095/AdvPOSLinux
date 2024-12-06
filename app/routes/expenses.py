from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.expenses import ExpensesForm, ExpensesUpdateForm
import pandas as pd
from app.scripts.log import event_logging
from werkzeug.datastructures import MultiDict

expenses_blueprint = Blueprint('expenses_blueprint', __name__)

@expenses_blueprint.route('/expenses_records', methods=['GET', 'POST'])
@login_required
def expenses_records():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db
    # Fetch all expense records from the database
    expenses_records = list(db.expense.find({
        'user_id': user_id,
        'account_id': account_id
    }))
    for cog in expenses_records:
        cog['date_updated'] = cog['date_updated'].strftime("%Y-%m-%d")
    return render_template('expenses.html', expenses_records=expenses_records)

@expenses_blueprint.route('/expenses_add', methods=['GET', 'POST'])
@login_required
def expenses_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db
    expenses_records = list(db.expense.find({
        'user_id': user_id,
        'account_id': account_id
    }))
    for cog in expenses_records:
        cog['date_updated'] = pd.to_datetime(cog['date_updated']).strftime("%Y-%m-%d")
    form = ExpensesForm()

    if session.get('user_id'):
        user_id = session['user_id']
        account_id = session['account_id']
    else:
        user_id = None
        account_id = session['account_id']

    if request.method == 'POST':
        date_inserted = datetime.now()

        fields = [
            'date_of_transaction',
            'description',
            'price',
            'type_of_expense',
            'store',
            'remarks',
            'payment_method'
        ]

        new_record = {}
        for field in fields:
            if field == 'price':
                field_value = float(request.form.get(field))
            else:
                field_value = request.form.get(field)
            new_record[field] = field_value

        primary_fields = {
            'date_inserted': date_inserted,
            'account_id': account_id,
            'user_id': user_id,
            'date_updated': date_inserted            
        }

        new_record.update(primary_fields)

        try:
            result = db.expense.insert_one(new_record)
            result_id = result.inserted_id
            new_record['_id'] = result_id
            event_logging(event_var="expense add",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=result_id,
                        old_doc=None,
                        new_doc=None,
                        error=None)
            flash("Cost of Goods record added successfully!", "success")
        except Exception as e:
            event_logging(event_var="expense add error",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=None,
                        old_doc=None,
                        new_doc=None,
                        error=e)
            flash(f"Error deleting record: {e}", "danger")

        return redirect(url_for('expenses_blueprint.expenses_add'))  # Stay on the same page to show updated records

    return render_template('expenses_add.html', form=form, expenses_records=expenses_records)


# Route to delete a expense record
@expenses_blueprint.route('/expenses_delete/<string:record_id>', methods=['POST'])
@login_required
def expenses_delete(record_id):
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db
    record = db.expense.find_one({"_id": ObjectId(record_id)})
    try:
        db.expense.delete_one({"_id": ObjectId(record_id)})
        event_logging(event_var="expense delete",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=record_id,
                    old_doc=record,
                    new_doc=None,
                    error=None)
        flash("expense record deleted successfully!", "success")
    except Exception as e:
        event_logging(event_var="expense delete",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=record_id,
                    old_doc=record,
                    new_doc=None,
                    error=e)
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('expenses_blueprint.expenses_records'))


@expenses_blueprint.route('/expenses_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def expenses_edit(record_id):
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db
    record = db.expense.find_one({"_id": ObjectId(record_id)})
    expenses_records = list(db.expense.find({
        'user_id': user_id,
        'account_id': account_id
    }))

    fields = [
            'date_of_transaction',
            'description',
            'price',
            'type_of_expense',
            'platform',
            'store',
            'remarks',
            'payment_method'
        ]

    if not record:
        flash("Cost of goods record not found!", "danger")
        return redirect(url_for('expenses_blueprint.expenses_records'))

    date_inserted = datetime.now()
    primary_fields = {
        'date_inserted': date_inserted,
        'account_id': session.get('account_id'),
        'user_id': session.get('user_id'),
        'date_updated': date_inserted            
    }

    data = {}
    for field in fields:
        data[field] = record.get(field)

    data['date_of_transaction'] = pd.to_datetime(data['date_of_transaction'], format="%Y-%m-%d")

    primary_fields.update(data)
    print(primary_fields)

    formdata = MultiDict(primary_fields)
    form = ExpensesUpdateForm(data=formdata)

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
        price = float(form.price.data)
        platform = form.platform.data
        store = form.store.data
        type_of_expense = form.type_of_expense.data
        remarks = form.remarks.data

        updated_record = {
            'date_inserted': date_inserted,
            'account_id': account_id,
            'user_id': user_id,
            'date_of_transaction': date_of_transaction.strftime("%Y-%m-%d"),
            'description': description,
            'price': price,
            'type_of_expense': type_of_expense,
            'platform': platform,
            'store': store,
            'remarks': remarks,
            'date_updated': datetime.now()
        }

        try:
            db.expense.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
            new_doc = db.expense.find_one({"_id": ObjectId(record_id)})
            event_logging(event_var="expense edit",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=record_id,
                        old_doc=record,
                        new_doc=new_doc,
                        error=None)
            flash("User record updated successfully!", "success")
        except Exception as e:
            new_doc = db.expense.find_one({"_id": ObjectId(record_id)})
            event_logging(event_var="expense edit error",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=record_id,
                        old_doc=record,
                        new_doc=new_doc,
                        error=e)
            flash(f"Error updating record: {e}", "danger")
        return redirect(url_for('expenses_blueprint.expenses_records'))

    # Display errors if validation fails
    if request.method == 'POST':
        flash("Please correct the errors in the form.", "danger")

    return render_template('expenses_edit.html', form=form, record=record, expenses_records=expenses_records)
