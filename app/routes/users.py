from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app, session
from datetime import datetime
from bson.objectid import ObjectId
from app.routes.login_required import login_required, admin_required
from app.forms.forms import UserForm, UserFormUpdate
from werkzeug.security import generate_password_hash

users_blueprint = Blueprint('users_blueprint', __name__)

@users_blueprint.route('/users_records', methods=['GET', 'POST'])
@login_required
def users():
    db = current_app.db
   
    # Fetch all users records from the database
    users_records = list(db.users.find())
    return render_template('users.html', users_records=users_records)


@users_blueprint.route('/users_add', methods=['GET', 'POST'])
@admin_required
def users_add():
    
    db = current_app.db
    users_records = list(db.users.find())
    form = UserForm()

    if form.validate_on_submit():
        # Check if the username or email already exists
        existing_user = db.users.find_one({'username': form.username.data})
        if existing_user:
            flash("Username already exists. Please choose a different one.", "danger")
            return redirect(url_for('users_blueprint.users_add'))
        else:
            existing_user = db.users.find_one({'username': form.username.data})
        
        hashed_password = generate_password_hash(form.password.data)
        is_admin = form.is_admin.data == 'True'
        db_count = db['users'].count_documents({})
    
    if request.method == 'POST':
        # Handle form submission for adding user
        date_inserted = datetime.now()
        username = request.form.get('username')
        if username:
            new_record = {
                'user_id': db_count,
                'date_inserted': datetime.now(),
                'account_id': session['account_id'],
                'username': form.username.data.strip(),
                'password': hashed_password,
                'name': form.name.data.strip().title(),
                'email': form.email.data.strip().lower(),
                'is_admin': is_admin
            }
            db.users.insert_one(new_record)
            flash("users record added successfully!", "success")
            
            return redirect(url_for('users_blueprint.users_add'))  # Stay on the same page to show updated records

        flash("All fields are required!", "danger")

    return render_template('users_add.html', form=form, users_records=users_records)

# Route to delete a users record
@users_blueprint.route('/users_delete/<string:record_id>', methods=['POST'])
@admin_required
def users_delete(record_id):
    db = current_app.db
    try:
        db.users.delete_one({"_id": ObjectId(record_id)})
        flash("User record deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting record: {e}", "danger")
    return redirect(url_for('users_blueprint.users'))

@users_blueprint.route('/users_edit/<string:record_id>', methods=['GET', 'POST'])
@admin_required
def users_edit(record_id):
    db = current_app.db
    record = db.users.find_one({"_id": ObjectId(record_id)})
    print(record)
    users_records = list(db.users.find())

    if not record:
        flash("User record not found!", "danger")
        return redirect(url_for('users_blueprint.users'))

    form = UserFormUpdate(obj=record)

    if form.validate_on_submit():
        password = form.password.data
        if password:
            hashed_password = generate_password_hash(password)
        else:
            hashed_password = record.get('password')

        date_inserted = record.get('date_inserted')
        user_id = record['user_id']
        account_id = session['account_id']
        username = record['username']  # Username is not editable
        name = form.name.data
        email = form.email.data
        date_updated = datetime.now()

        # Update the record
        updated_record = {
            "date_inserted": date_inserted,
            "user_id": user_id,
            "account_id": account_id,
            "username": username,
            "password": hashed_password,
            "name": name,
            "email": email,
            "date_updated": date_updated
        }

        try:
            db.users.update_one({"_id": ObjectId(record_id)}, {"$set": updated_record})
            flash("User record updated successfully!", "success")
        except Exception as e:
            flash(f"Error updating record: {e}", "danger")
        return redirect(url_for('users_blueprint.users'))

    # Display errors if validation fails
    if request.method == 'POST':
        flash("Please correct the errors in the form.", "danger")

    return render_template('users_edit.html', form=form, record=record, users_records=users_records)
