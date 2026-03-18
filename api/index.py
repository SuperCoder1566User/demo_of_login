from flask import Flask, request, render_template_string

app = Flask(__name__)

# CSS for that "Vewy Cwean" UI
BASE_STYLE = """
<style>
    :root { --primary: #6366f1; --bg: #f8fafc; --text: #1e293b; }
    body { font-family: -apple-system, system-ui, sans-serif; background: var(--bg); color: var(--text); display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .card { background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); width: 100%; max-width: 320px; text-align: center; }
    h2 { margin: 0 0 1.5rem; font-size: 1.5rem; }
    input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #e2e8f0; border-radius: 8px; box-sizing: border-box; font-size: 1rem; }
    button { width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; margin-top: 10px; transition: 0.2s; }
    button:hover { opacity: 0.9; }
    .error { color: #ef4444; background: #fee2e2; padding: 8px; border-radius: 6px; font-size: 0.85rem; margin-bottom: 1rem; }
    .success-icon { font-size: 4rem; margin-bottom: 1rem; display: block; }
    h1 { color: #0f172a; margin: 0; font-size: 1.75rem; }
</style>
"""

LOGIN_PAGE = BASE_STYLE + """
<div class="card">
    <h2>Welcome</h2>
    {% if error %}<div class="error">{{ error }}</div>{% endif %}
    <form method="POST">
        <input type="text" name="u" placeholder="Username" required>
        <input type="password" name="p" placeholder="Password" required>
        <button type="submit">Sign In</button>
    </form>
</div>
"""

SUCCESS_PAGE = BASE_STYLE + """
<div class="card">
    <span class="success-icon">✅</span>
    <h1>Completed demo</h1>
    <p style="color: #64748b">You have logged in successfully.</p>
    <a href="/" style="color: var(--primary); text-decoration: none; font-size: 0.9rem;">Back to login</a>
</div>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user = request.form.get('u')
        pw = request.form.get('p')
        # User: Admn | Password: letmein123 (Not case sensitive)
        if user == "Admn" and pw.lower() == "letmein123":
            return render_template_string(SUCCESS_PAGE)
        return render_template_string(LOGIN_PAGE, error="Invalid credentials")
    return render_template_string(LOGIN_PAGE)

# Required for Vercel
app.debug = True
