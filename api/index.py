from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    password = request.form.get('password')

    # Case-insensitive check for password using .lower()
    if user == "Admn" and password.lower() == "letmein123":
        return redirect(url_for('completed'))
    else:
        return render_template('login.html', error="Invalid credentials")

@app.route('/completed')
def completed():
    return render_template('success.html')

# Essential for Vercel
app.debug = True
