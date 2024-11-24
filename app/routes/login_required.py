from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_redirect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        
        # Check if the user is an admin (optional, based on your logic)
        if session.get('is_admin', False):
            # Admin logic can go here if needed
            pass
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to log in as user or admin to access this page.", "warning")
            return redirect(url_for('main.login'))
        
        # Check if the user is an admin (optional, based on your logic)
        if session.get('is_admin', False):
            # Admin logic can go here if needed
            pass
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in and is an admin
        if not session.get('is_admin', False):
            flash("You need admin privileges to access this page.", "warning")
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function
