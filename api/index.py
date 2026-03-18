import os
import redis
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

# Redis Setup - Vercel automatically loads .env variables
r = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=os.getenv('REDIS_PORT'),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True
)

BASE_STYLE = """
<style>
    :root { --primary: #6366f1; --bg: #f8fafc; --text: #1e293b; }
    body { font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .card { background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); width: 100%; max-width: 320px; text-align: center; }
    input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #e2e8f0; border-radius: 8px; box-sizing: border-box; font-size: 1rem; }
    button { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; margin-top: 10px; }
    .error { color: #ef4444; background: #fee2e2; padding: 8px; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem; }
    .success { color: #10b981; background: #ecfdf5; padding: 8px; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem; }
</style>
"""

# Template for Login/Register
FORM_PAGE = BASE_STYLE + """
<div class="card">
    <h2>{{ title }}</h2>
    {% if msg %}<div class="{{ msg_type }}">{{ msg }}</div>{% endif %}
    <form method="POST">
        <input type="text" name="u" placeholder="Username" required>
        <input type="password" name="p" placeholder="Password" required>
        <button type="submit">{{ btn }}</button>
    </form>
    <p style="margin-top:15px; font-size:0.9rem;">
        {{ link_text }} <a href="{{ link_url }}" style="color:var(--primary)">Click here</a>
    </p>
</div>
"""

SUCCESS_PAGE = BASE_STYLE + """
<div class="card">
    <h1 style="color:#10b981">✅ Success</h1>
    <p>Completed demo. You are logged in!</p>
    <a href="/" style="color:var(--primary); text-decoration:none;">Logout</a>
</div>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('u')
        pw = request.form.get('p')
        # Check Redis for the user
        stored_pw = r.get(f"user:{user}")
        
        if stored_pw and stored_pw.lower() == pw.lower():
            return render_template_string(SUCCESS_PAGE)
        return render_template_string(FORM_PAGE, title="Login", btn="Sign In", msg="Invalid credentials", msg_type="error", link_text="New here?", link_url="/register")
    
    return render_template_string(FORM_PAGE, title="Login", btn="Sign In", link_text="New here?", link_url="/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('u')
        pw = request.form.get('p')
        
        if r.exists(f"user:{user}"):
            return render_template_string(FORM_PAGE, title="Register", btn="Create Account", msg="User already exists", msg_type="error", link_text="Have an account?", link_url="/")
        
        # Save to Redis
        r.set(f"user:{user}", pw)
        return render_template_string(FORM_PAGE, title="Login", btn="Sign In", msg="Account created! Please login.", msg_type="success", link_text="New here?", link_url="/register")
    
    return render_template_string(FORM_PAGE, title="Register", btn="Create Account", link_text="Have an account?", link_url="/")
