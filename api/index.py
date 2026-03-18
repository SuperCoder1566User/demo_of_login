import os
from flask import Flask, render_template, request, redirect, url_for

# Since templates is now INSIDE api/, we look in the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')
    
    # Case-insensitive password check
    if user == "Admn" and password.lower() == "letmein123":
        return redirect(url_for('completed'))
    else:
        return render_template('login.html', error="Invalid credentials")

@app.route('/completed')
def completed():
    return render_template('success.html')
