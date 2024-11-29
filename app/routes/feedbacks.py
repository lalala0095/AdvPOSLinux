from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.feedbacks import FeedbackForm
import pandas as pd
import json
from app.scripts.log import event_logging
from werkzeug.datastructures import MultiDict

feedbacks_blueprint = Blueprint('feedbacks_blueprint', __name__)

@feedbacks_blueprint.route('/feedbacks_records', methods=['GET', 'POST'])
@login_required
def feedbacks_records():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    # Fetch all feedbacks records from the database
    feedbacks_records = list(db.feedbacks.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))
    return render_template('feedbacks.html', feedbacks_records=feedbacks_records)

#------------
@feedbacks_blueprint.route('/feedbacks_add', methods=['GET', 'POST'])
@login_required
def feedbacks_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    feedbacks_records = list(db.feedbacks.find({
        "account_id": account_id,
        "user_id": user_id
    }))
    
    form = FeedbackForm()

    form_request = request.form

    if request.method == 'POST':
        print("form validated")        
        new_feedback = {
            'date_inserted': datetime.now(),
            'user_id': session.get('user_id'),
            'account_id': session.get('account_id'),
            'client_name': form_request.get('client_name'),
            'email': form_request.get('email'),
            'contact_number': form_request.get('contact_number'),
            'feedback_type': form_request.get('feedback_type'),
            'feedback_urgency': form_request.get('feedback_urgency'),
            'details': form_request.get('details'),
            'status': "Open"
        }
        print(f"new feedback: {new_feedback}")
        try:
            result = db.feedbacks.insert_one(new_feedback)
            flash("Feedback successfully added.", "success")
            event_logging(
                event_var="adding feedbacks",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=result.inserted_id,
                old_doc=None,
                new_doc=None,
                error=None
            )
        except Exception as e:
            flash("Feedback not sent. Try to send again.", "danger")
            flash(form.errors)
            print(form.errors)
            event_logging(
                event_var="adding feedback error",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=None,
                old_doc=None,
                new_doc=None,
                error=e
            )

        # create ticket id
        db.feedbacks.update_many(
            {},  # Match all documents
            [
                {
                    "$set": {
                        "feedback_id": {"$toString": "$_id"}
                    }
                }
            ]
        )
        return redirect(url_for('products_blueprint.products_add'))

    feedbacks_records = list(db.feedbacks.find({
        "account_id": account_id,
        "user_id": user_id
    }))

    return render_template('feedbacks_add.html', feedbacks_records=feedbacks_records, form=form)

#------------


# Route to delete a feedbacks record
@feedbacks_blueprint.route('/feedbacks_delete/<string:record_id>', methods=['POST'])
@login_required
def feedbacks_delete(record_id):
    db = current_app.db
    try:
        db.feedbacks.delete_one({"_id": ObjectId(record_id)})
        flash("Orders record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('feedbacks_blueprint.feedbacks_records'))
