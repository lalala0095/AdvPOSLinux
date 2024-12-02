from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session, jsonify
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.bills import BillForm, CashFlowForm, BillerForm, BillsPlannerForm, populate_biller, populate_bills, populate_cash_flows
import pandas as pd
import json
from app.scripts.log import event_logging
from werkzeug.datastructures import MultiDict

bills_blueprint = Blueprint('bills_blueprint', __name__)

# ----------------
# billers section

@bills_blueprint.route('/billers_records', methods=['GET', 'POST'])
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
@bills_blueprint.route('/billers_add', methods=['GET', 'POST'])
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
            'amount': float(form.amount.data),
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
        return redirect(url_for('bills_blueprint.billers_add'))

    billers_records = list(db.billers.find({
        "account_id": account_id,
        "user_id": user_id
    }))

    return render_template('billers_add.html', billers_records=billers_records, form=form)

#------------


# Route to delete a billers record
@bills_blueprint.route('/billers_delete/<string:record_id>', methods=['POST'])
@login_required
def billers_delete(record_id):
    db = current_app.db
    try:
        db.billers.delete_one({"_id": ObjectId(record_id)})
        flash("Orders record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('bills_blueprint.billers_records'))


# ------- bills section

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
    print(form.bill_name.choices)
    if form.validate_on_submit():
        print(form.bill_name.data)
        print(type(form.bill_name.data))
        biller_object_id = ObjectId(form.bill_name.data)
        biller_object = db.billers.find_one({"_id": biller_object_id})
        print(biller_object)

        due_date = form.due_date.data
        due_date = pd.to_datetime(due_date)
        new_bill = {
            'date_inserted': datetime.now(),
            'user_id': session.get('user_id'),
            'account_id': session.get('account_id'),
            'biller': biller_object,
            'bill_urgency': form.bill_urgency.data,
            'amount': float(form.amount.data),
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
        i['biller_name'] = i['biller']['biller_name']

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

@bills_blueprint.route('/get_amount', methods=['GET'])
@login_required
def get_amount():
    bill_name = request.args.get('bill_name')
    if not bill_name:
        return jsonify({"error": "Bill name is required"}), 400
    
    db = current_app.db
    biller = db['billers'].find_one({"_id": ObjectId(bill_name)}, {"_id": 0, "amount": 1})
    
    if not biller:
        return jsonify({"error": "Biller not found"}), 404
    
    return jsonify({"amount": biller.get('amount')})



# ----------------
# cash_flows section

@bills_blueprint.route('/cash_flows_records', methods=['GET', 'POST'])
@login_required
def cash_flows_records():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    # Fetch all cash_flows records from the database
    cash_flows_records = list(db.cash_flows.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))
    return render_template('cash_flows.html', cash_flows_records=cash_flows_records)

#------------
@bills_blueprint.route('/cash_flows_add', methods=['GET', 'POST'])
@login_required
def cash_flows_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    cash_flows_records = list(db.cash_flows.find({
        "account_id": account_id,
        "user_id": user_id
    }))
    
    form = CashFlowForm()

    if form.validate_on_submit():
        usual_income_day = form.usual_income_day.data
        if usual_income_day >= datetime.today().day:
            possible_next_month_date = datetime(
                year=datetime.today().year,
                month=datetime.today().month,
                day=usual_income_day
                )
        else:
            possible_next_month_date = datetime(
                year=datetime.today().year,
                month=datetime.today().month + 1,
                day=usual_income_day
                )

        new_cash_flow = {
            'date_inserted': datetime.now(),
            'user_id': session.get('user_id'),
            'account_id': session.get('account_id'),
            'cash_flow_name': form.cash_flow_name.data,
            'cash_flow_type': form.cash_flow_type.data,
            'custom_type': form.custom_type.data,
            'usual_income_day': usual_income_day,
            'possible_next_month_date': possible_next_month_date,
            'amount': float(form.amount.data),
            'remarks': form.remarks.data
        }
        try:
            result = db.cash_flows.insert_one(new_cash_flow)
            flash("Biller successfully added.", "success")
            event_logging(
                event_var="adding cash_flows",
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
                event_var="adding cash_flow error",
                user_id=session.get('user_id'),
                account_id=session.get('account_id'),
                object_id=None,
                old_doc=None,
                new_doc=None,
                error=e
            )
        return redirect(url_for('bills_blueprint.cash_flows_add'))

    cash_flows_records = list(db.cash_flows.find({
        "account_id": account_id,
        "user_id": user_id
    }))
    for i in cash_flows_records:
        i['possible_next_month_date'] = pd.to_datetime(i['possible_next_month_date']).strftime("%b %d, %Y") 

    return render_template('cash_flows_add.html', cash_flows_records=cash_flows_records, form=form)

#------------


# Route to delete a cash_flows record
@bills_blueprint.route('/cash_flows_delete/<string:record_id>', methods=['POST'])
@login_required
def cash_flows_delete(record_id):
    db = current_app.db
    try:
        db.cash_flows.delete_one({"_id": ObjectId(record_id)})
        flash("Orders record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('bills_blueprint.cash_flows_records'))



# ----------------
# bills_planners section

@bills_blueprint.route('/bills_planners_records', methods=['GET', 'POST'])
@login_required
def bills_planners_records():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    # Fetch all bills_planners records from the database
    bills_planners_records = list(db.bills_planners.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))
    return render_template('bills_planners.html', bills_planners_records=bills_planners_records)


#------------
@bills_blueprint.route('/bills_planners_add', methods=['GET', 'POST'])
@login_required
def bills_planners_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db

    bills_db = list(db.bills.find(
        {
            "account_id": account_id,
            "user_id": user_id
        }
    )) 

    cash_flows_db = list(db.cash_flows.find(
        {
            "account_id": account_id,
            "user_id": user_id
        }
    )) 

    form = BillsPlannerForm()
    print(form)
    print("append choices to bills")
    populate_bills(form, bills_db)

    populate_cash_flows(form, cash_flows_db)

    return render_template('bills_planners_add.html', bills_db=bills_db, cash_flows_db=cash_flows_db, form=form)

@bills_blueprint.route('/get_bills_amount', methods=['GET'])
@login_required
def get_bills_amount():
    bill_name = request.args.get('bills')
    if not bill_name:
        return jsonify({"error": "Bill name is required"}), 400
    
    db = current_app.db
    biller = db['bills'].find_one({"_id": ObjectId(bill_name)}, {"_id": 0, "amount": 1})
    
    if not biller:
        return jsonify({"error": "Biller not found"}), 404
    
    return jsonify({"amount": biller.get('amount')})

@bills_blueprint.route('/get_cash_flows_amount', methods=['GET'])
@login_required
def get_cash_flows_amount():
    cash_flows_name = request.args.get('cash_flows')
    if not cash_flows_name:
        return jsonify({"error": "Cash Flow name is required"}), 400
    
    db = current_app.db
    biller = db['cash_flows'].find_one({"_id": ObjectId(cash_flows_name)}, {"_id": 0, "amount": 1})
    
    if not biller:
        return jsonify({"error": "Cash Flow not found"}), 404
    
    return jsonify({"amount": biller.get('amount')})

#------------


# Route to delete a bills_planners record
@bills_blueprint.route('/bills_planners_delete/<string:record_id>', methods=['POST'])
@login_required
def bills_planners_delete(record_id):
    db = current_app.db
    try:
        db.bills_planners.delete_one({"_id": ObjectId(record_id)})
        flash("Orders record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('bills_blueprint.bills_planners_records'))


