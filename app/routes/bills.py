from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session, jsonify
from pymongo import MongoClient
from app.config import Config
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required
from app.forms.bills import BillForm, CashFlowForm, CashFlowUpdateForm, BillerForm, BillsPlannerForm, populate_biller
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

    try:
        amount = float(form.amount.data)
    except:
        amount = None

    if form.validate_on_submit():
        print("form validated")
        new_biller = {
            'date_inserted': datetime.now(),
            'user_id': session.get('user_id'),
            'account_id': session.get('account_id'),
            'biller_name': form.biller_name.data,
            'biller_type': form.biller_type.data,
            'custom_type': form.custom_type.data,
            'amount_type': form.amount_type.data,
            'amount': amount,
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
            error_messages = [msg for messages in form.errors.values() for msg in messages]
            if error_messages:  
                flash(f"Error in the response: {' '.join(error_messages)}", "danger")
                flash("Please correct the errors.", "danger")  
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
    else:
        error_messages = [msg for messages in form.errors.values() for msg in messages]
        if error_messages:  
            flash(f"Error in the response: {' '.join(error_messages)}", "danger")
            flash("Please correct the errors.", "danger")  
            print(form.errors)
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

    for i in cash_flows_records:
        try:
            i['receiving_date'] = i['receiving_date'].strftime("%b %d, %Y")
        except:
            i['receiving_date'] = None
        try:
            i['possible_next_month_date'] = i['possible_next_month_date'].strftime("%b %d, %Y")
        except:
            i['possible_next_month_date'] = None

    return render_template('cash_flows.html', cash_flows_records=cash_flows_records)

#------------
@bills_blueprint.route('/cash_flows_add', methods=['GET', 'POST'])
@login_required
def cash_flows_add():
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db
    
    form = CashFlowForm()

    if form.validate_on_submit():
        usual_income_day = form.usual_income_day.data
        if usual_income_day is None:
            possible_next_month_date = None
        elif usual_income_day >= datetime.today().day:
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
            'receiving_date': form.receiving_date.data,
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

    # Fetch all cash_flows records from the database
    cash_flows_records = list(db.cash_flows.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))

    for i in cash_flows_records:
        try:
            i['receiving_date'] = i['receiving_date'].strftime("%b %d, %Y")
        except:
            i['receiving_date'] = None
        try:
            i['possible_next_month_date'] = i['possible_next_month_date'].strftime("%b %d, %Y")
        except:
            i['possible_next_month_date'] = None

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

@bills_blueprint.route('/cash_flows_edit/<string:record_id>', methods=['GET', 'POST'])
@login_required
def cash_flows_edit(record_id):
    account_id = session.get('account_id')
    user_id = session.get('user_id')

    db = current_app.db
    record = db.cash_flows.find_one({"_id": ObjectId(record_id)})

    fields = [
            'receiving_date',
            'cash_flow_name',
            'cash_flow_type',
            'custom_type',
            'usual_income_day',
            'possible_next_month_date',
            'amount',
            'remarks'
        ]

    if not record:
        flash("Cost of goods record not found!", "danger")
        return redirect(url_for('bills_blueprint.cash_flows_records'))

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

    data['receiving_date'] = pd.to_datetime(data['receiving_date'], format="%Y-%m-%d")

    primary_fields.update(data)
    print(primary_fields)

    formdata = MultiDict(primary_fields)
    form = CashFlowUpdateForm(data=formdata)

    if form.validate_on_submit():
        if session.get('user_id'):
            user_id = session['user_id']
            account_id = session['account_id']
        else:
            user_id = None
            account_id = session['account_id']

        usual_income_day = form.usual_income_day.data
        if usual_income_day is None:
            possible_next_month_date = None
        elif usual_income_day >= datetime.today().day:
            possible_next_month_date = datetime(
                year=datetime.today().year,
                month=datetime.today().month,
                day=usual_income_day
                )
        else:
            month = datetime.today().month + 1
            if month > 12:
                month = 1
                year = datetime.today().year + 1
            possible_next_month_date = datetime(
                year=year,
                month=month,
                day=usual_income_day
                )

        # if request.method == 'POST':
        date_inserted = record['date_inserted']
        receiving_date = pd.to_datetime(form.receiving_date.data) 
        cash_flow_name = form.cash_flow_name.data
        cash_flow_type = form.cash_flow_type.data
        custom_type = form.custom_type.data
        possible_next_month_date = pd.to_datetime(possible_next_month_date)
        amount = float(form.amount.data)
        remarks = form.remarks.data

        updated_record = {
            'date_inserted': date_inserted,
            'account_id': account_id,
            'user_id': user_id,
            'receiving_date': receiving_date,
            'cash_flow_name': cash_flow_name,
            'cash_flow_type': cash_flow_type,
            'custom_type': custom_type,
            'usual_income_day': usual_income_day,
            'possible_next_month_date': possible_next_month_date,
            'amount': amount,
            'remarks': remarks,
            'date_updated': datetime.now()
        }

        try:
            db.cash_flows.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
            new_doc = db.cash_flows.find_one({"_id": ObjectId(record_id)})
            event_logging("cash_flows edit", session.get('user_id'), session.get('account_id'), record_id, record, new_doc, None)
            flash("User record updated successfully!", "success")
        except Exception as e:
            new_doc = db.cash_flows.find_one({"_id": ObjectId(record_id)})
            event_logging("cash_flows edit", session.get('user_id'), session.get('account_id'), record_id, record, new_doc, e)
            flash(f"Error updating record: {e}", "danger")
        return redirect(url_for('bills_blueprint.cash_flows_records'))

    # Display errors if validation fails
    if request.method == 'POST':
        error_messages = [msg for messages in form.errors.values() for msg in messages]
        if error_messages:  
            flash(f"Error in the response: {' '.join(error_messages)}", "danger")
            flash("Please correct the errors in the form.", "danger")

    # Fetch all cash_flows records from the database
    cash_flows_records = list(db.cash_flows.find({
        "account_id": account_id,
        "user_id": user_id
    }
    ))

    for i in cash_flows_records:
        try:
            i['receiving_date'] = i['receiving_date'].strftime("%b %d, %Y")
        except:
            i['receiving_date'] = None
        try:
            i['possible_next_month_date'] = i['possible_next_month_date'].strftime("%b %d, %Y")
        except:
            i['possible_next_month_date'] = None

    return render_template('cash_flows_edit.html', form=form, record=record, cash_flows_records=cash_flows_records)



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
    for i in bills_planners_records:
        i['bills_count'] = len(i['bills'])
        i['cash_flows_count'] = len(i['cash_flows'])
    return render_template('bills_planners.html', bills_planners_records=bills_planners_records)

@bills_blueprint.route('/bills_planners_view/<string:record_id>', methods=['GET', 'POST'])
@login_required
def bills_planners_view(record_id):
    try:
        account_id = session.get('account_id')
        user_id = session.get('user_id')

        db = current_app.db

        print(record_id)
        print(type(record_id))
        bills_planner_object = db.bills_planners.find_one({"_id": ObjectId(record_id)})
    except Exception as e:
        print(e)

    return render_template('bills_planners_view.html', bills_planner_object=bills_planner_object)


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
    for i in bills_db:
        i['bill_id'] = str(i['_id'])
    cash_flows_db = list(db.cash_flows.find(
        {
            "account_id": account_id,
            "user_id": user_id
        }
    ))
    for i in cash_flows_db:
        i['cash_flow_id'] = str(i['_id'])
        try:
            i['receiving_date'] = i['receiving_date'].strftime("%b %d, %Y")
        except:
            i['receiving_date'] = ""

    form = BillsPlannerForm()
    # form.bills_planner_name.data = "manual name"
    
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form)

            planner_count = len(list(db['planners'].find({"account_id": account_id, "user_id": user_id})))

            bills_objects = form.bills.data
            print(bills_objects)
            cash_flows_objects = form.cash_flows.data

            total_bills_amount = []
            for i in bills_objects:
                total_bills_amount.append(i['amount'])

            total_cash_flows_amount = []
            for i in cash_flows_objects:
                total_cash_flows_amount.append(i['amount'])

            bills_amount_final = sum(total_bills_amount)
            cash_flows_amount_final = sum(total_cash_flows_amount)
            new_data = {
                'date_inserted': datetime.now(),
                'bills_planner_name': form.bills_planner_name.data,
                'planner_count_of_the_user': planner_count,
                'account_id': account_id,
                'user_id': user_id,
                'bills': bills_objects,
                'cash_flows': cash_flows_objects,
                'total_bills_amount': bills_amount_final,
                'total_cash_flows_amount': cash_flows_amount_final,
                'bills_minus_cash_flows': bills_amount_final - cash_flows_amount_final,
                'cash_flows_minus_bills': cash_flows_amount_final - bills_amount_final
            }
            print(new_data)
            result = db.bills_planners.insert_one(new_data)

            # Redirect after successful submission
            flash("Planner saved successfully!", "success")
            event_logging(event_var="bills allocations planner add",
                            user_id=session.get('user_id'),
                            account_id=session.get('account_id'),
                            object_id=result.inserted_id,
                            old_doc=None,
                            new_doc=None,
                            error=None)
            return redirect(url_for('bills_blueprint.bills_planners_add'))
        else:
            print(form.errors)
            event_logging(event_var="bills allocations planner error",
                        user_id=session.get('user_id'),
                        account_id=session.get('account_id'),
                        object_id=None,
                        old_doc=None,
                        new_doc=None,
                        error=form.errors)
            flash(f"Error adding bills planner: {form.errors}", "danger")
            flash(f"This error has been logged, you may add a ticket in Feedbacks.", "danger")
            return render_template('bills_planners_add.html', bills_db=bills_db, cash_flows_db=cash_flows_db, form=form)
    return render_template('bills_planners_add.html', bills_db=bills_db, cash_flows_db=cash_flows_db, form=form)

                

# Route to delete a bills_planners record
@bills_blueprint.route('/bills_planners_delete/<string:record_id>', methods=['POST'])
@login_required
def bills_planners_delete(record_id):
    db = current_app.db
    try:
        object = db.bills_planners.find_one({"_id": ObjectId(record_id)})
        result = db.bills_planners.delete_one({"_id": ObjectId(record_id)})
        flash("Planner record deleted successfully!", "success")
        event_logging(event_var="bills allocations planner delete",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=record_id,
                    old_doc=object,
                    new_doc=None,
                    error=None)

    except Exception as e:
        event_logging(event_var="bills allocations planner delete error",
                    user_id=session.get('user_id'),
                    account_id=session.get('account_id'),
                    object_id=None,
                    old_doc=None,
                    new_doc=None,
                    error=e)
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('bills_blueprint.bills_planners_records'))


