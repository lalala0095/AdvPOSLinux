from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.bills import BillForm, PaymentMethodForm, BillerForm, populate_biller
import pandas as pd
import json
from app.scripts.log import event_logging
from werkzeug.datastructures import MultiDict

bills_blueprint = Blueprint('bills_blueprint', __name__)

@bills_blueprint.route('/bills_records', methods=['GET', 'POST'])
@login_required
def bills_records():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    # Fetch all bills records from the database
    bills_records = list(db.bills.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))
    return render_template('bills.html', bills_records=bills_records)

#------------
@bills_blueprint.route('/bills_add', methods=['GET', 'POST'])
@login_required
def bills_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    bills_records = list(db.bills.find({
        "account_id": account_id,
        "user_id": user_id
    }))
    
    form = BillForm()
    populate_biller(form)
    form_request = request.form

    if form.validate_on_submit():
        due_date = form.due_date.data
        due_date = pd.to_datetime(due_date)
        new_bill = {
            'date_inserted': datetime.now(),
            'user_id': session.get('user_id'),
            'account_id': session.get('account_id'),
            'bill_name': form.bill_name.data,
            'bill_urgency': form.bill_urgency.data,
            'due_date': due_date,
            'remarks': form.remarks.data
        }
        try:
            result = db.bills.insert_one(new_bill)
            flash("Bill successfully added.", "success")
            event_logging(
                event_var="adding bills",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=result.inserted_id,
                old_doc=None,
                new_doc=None,
                error=None
            )
        except Exception as e:
            flash("Bill not inserted. This error has been logged but you may send feedback about the issue.", "danger")
            flash(form.errors)
            print(form.errors)
            event_logging(
                event_var="adding bill error",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=None,
                old_doc=None,
                new_doc=None,
                error=e
            )
        return redirect(url_for('bills_blueprint.bills_add'))

    bills_records = list(db.bills.find({
        "account_id": account_id,
        "user_id": user_id
    }))
    for i in bills_records:
        i['due_date'] = pd.to_datetime(i['due_date']).strftime("%b. %d, %Y")

    return render_template('bills_add.html', bills_records=bills_records, form=form)

#------------


# Route to delete a bills record
@bills_blueprint.route('/bills_delete/<string:record_id>', methods=['POST'])
@login_required
def bills_delete(record_id):
    db = current_app.db
    try:
        db.bills.delete_one({"_id": ObjectId(record_id)})
        flash("Orders record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('bills_blueprint.bills_records'))
