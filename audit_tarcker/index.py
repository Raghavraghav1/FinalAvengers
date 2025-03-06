from flask import Flask ,redirect,render_template,Blueprint,request,jsonify,session,flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
from datetime import datetime, timedelta
from audit_tarcker.config import collection
from audit_tarcker.test import only_one

# Securely store admin credentials (Better to use environment variables)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'Admin@raghu')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'Raghu@1234')
#BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the directory of the current file
#AuditTrack = os.path.join(BASE_DIR, '..', 'instance', 'auditTracker.db')
permanent_session_lifetime = timedelta(seconds=10)
# Auth blueprint
auth = Blueprint('auth', __name__)

# Flask-Login setup
login_manager = LoginManager()
# User Model for Admin Only
class Users(UserMixin):
    def __init__(self, user_id,password,role):
        self.id = str(user_id)
        self.password=password
        self.role=role


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    if not user_id:
        return None

    if user_id==ADMIN_USERNAME:
        return Users(user_id=ADMIN_USERNAME,password=ADMIN_PASSWORD,role='admin')
    try:
        login_details=tuple(collection.find({"auditor_name":user_id},{"Audit_id":1,"auditor_name":1,"_id":0}))
        print(login_details)
        if user_id==login_details[0]["auditor_name"]:
            print('i am here .... auditor ' )
            return Users(user_id=login_details[0]["auditor_name"], password=login_details[0]["Audit_id"],role='auditor')  # Adjust attributes as needed
    except Exception as e:
        print(f"Database Error: {e}")

    return None  # User not found

# Admin login route
@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Only allow the admin to log in
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.permanent = True
            user = Users(user_id=ADMIN_USERNAME,password=generate_password_hash(ADMIN_PASSWORD, method="pbkdf2:sha256") ,role='admin')
            session['username'] = username
            session['islogin'] = True
            session['role']='admin'
            login_user(user)
            return redirect('/admin1')


        # fetching auditor details from database

        auditor_data=tuple(collection.find({"Audit_id":password},{"Audit_id":1,"auditor_name":1,"_id":0}))
        print(auditor_data)
        if auditor_data:
            user1=Users(user_id=auditor_data[0]["auditor_name"],password=generate_password_hash(auditor_data[0]["Audit_id"], method="pbkdf2:sha256"),role='auditor')
            session['username'] = username
            session.permanent = True
            session['islogin'] = True
            session['role']='auditor'
            session['id']=password
            login_user(user1)
            return redirect(f'/auditor_page/{username}')
    return redirect('/signup_page')

# Logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect('/')

# Admin dashboard route (restricted to admin only)
@auth.route('/admin1')
@login_required
@only_one('admin')
def admin():
    if session.get('username') == ADMIN_USERNAME:
        return redirect('/dashboard')
    return "Unauthorized", 403


#auditor_page route
@auth.route(f'/auditor_page/<username>')
@login_required

def auditor(username):
    if session.get('role') == 'auditor':
        return render_template('auditor_page.html' ,username=session['username'],id=session['id'])
    return f'error unauthorized' ,403


