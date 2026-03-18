import os
from flask import Flask, render_template, request, redirect, url_for

# This tells Flask exactly where to find the templates folder
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    # Password check is NOT case sensitive
    if user == "Admn" and password.lower() == "letmein123":
        return redirect(url_for('completed'))
    else:
        return render_template('login.html', error="Invalid credentials")

@app.route('/completed')
def completed():
    return render_template('success.html')

# This is required for Vercel to treat this as a function
app.debug = True
