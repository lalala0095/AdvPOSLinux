from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.bills import BillerForm
import pandas as pd
import json
from app.scripts.log import event_logging
from werkzeug.datastructures import MultiDict

billers_blueprint = Blueprint('billers_blueprint', __name__)

@billers_blueprint.route('/billers_records', methods=['GET', 'POST'])
@login_required
def billers_records():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    # Fetch all billers records from the database
    billers_records = list(db.billers.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))
    return render_template('billers.html', billers_records=billers_records)

#------------
@billers_blueprint.route('/billers_add', methods=['GET', 'POST'])
@login_required
def billers_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    billers_records = list(db.billers.find({
        "account_id": account_id,
        "user_id": user_id
    }))
    
    form = BillerForm()

    if form.validate_on_submit():
        new_biller = {
            'date_inserted': datetime.now(),
            'user_id': session.get('user_id'),
            'account_id': session.get('account_id'),
            'biller_name': form.biller_name.data,
            'biller_type': form.biller_type.data,
            'custom_type': form.custom_type.data,
            'usual_due_day': form.usual_due_day.data,
            'remarks': form.remarks.data
        }
        try:
            result = db.billers.insert_one(new_biller)
            flash("Biller successfully added.", "success")
            event_logging(
                event_var="adding billers",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=result.inserted_id,
                old_doc=None,
                new_doc=None,
                error=None
            )
        except Exception as e:
            flash("Biller not inserted. This error has been logged but you may send feedback about the issue.", "danger")
            flash(form.errors)
            print(form.errors)
            event_logging(
                event_var="adding biller error",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=None,
                old_doc=None,
                new_doc=None,
                error=e
            )
        return redirect(url_for('billers_blueprint.billers_add'))

    billers_records = list(db.billers.find({
        "account_id": account_id,
        "user_id": user_id
    }))

    return render_template('billers_add.html', billers_records=billers_records, form=form)

#------------


# Route to delete a billers record
@billers_blueprint.route('/billers_delete/<string:record_id>', methods=['POST'])
@login_required
def billers_delete(record_id):
    db = current_app.db
    try:
        db.billers.delete_one({"_id": ObjectId(record_id)})
        flash("Orders record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('billers_blueprint.billers_records'))
