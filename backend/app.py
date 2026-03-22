from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

from chatbot_model import generate_response, get_db_connection, is_mysql, placeholder

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = os.getenv('SECRET_KEY', 'ltce_secret_key_dev_change_me')

# ---------------- HOME ----------------
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session['username'])

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        try:
            conn = get_db_connection()
        except Exception as e:
            print("DB Connection Error:", e)
            flash("Database connection error. Please try again.")
            return redirect(url_for('login'))

        ph = placeholder()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username={ph}", (username,))
        user_row = cursor.fetchone()
        conn.close()

        if user_row:
            user = {'id': user_row[0], 'username': user_row[1], 'password_hash': user_row[2]}
            if check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['history'] = []
                return redirect(url_for('index'))

        flash("Invalid username or password")

    return render_template('login.html')

# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        try:
            conn = get_db_connection()
        except Exception as e:
            print("DB Connection Error:", e)
            flash("Database connection error. Please try again.")
            return redirect(url_for('signup'))

        ph = placeholder()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM users WHERE username={ph}", (username,))
        if cursor.fetchone():
            flash("Username already exists. Please choose another.")
            conn.close()
            return redirect(url_for('signup'))

        hashed = generate_password_hash(password)
        cursor.execute(
            f"INSERT INTO users (username, password_hash) VALUES ({ph}, {ph})",
            (username, hashed)
        )
        conn.commit()
        conn.close()

        flash("Account created! Please login.")
        return redirect(url_for('login'))

    return render_template('signup.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- CHAT ----------------
@app.route('/chat', methods=['POST'])
def chat():
    if 'user_id' not in session:
        return jsonify({'reply': 'Login first'})

    data = request.get_json()
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'reply': 'Empty message'})

    if "history" not in session:
        session["history"] = []

    session["history"].append(user_message)

    try:
        reply = generate_response(user_message, session["history"])
    except Exception as e:
        print("CHAT ERROR:", e)
        return jsonify({'reply': 'Server error, try again'})

    try:
        ph = placeholder()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO chat_history (user_id, role, content) VALUES ({ph}, {ph}, {ph})",
            (session['user_id'], 'user', user_message)
        )
        cursor.execute(
            f"INSERT INTO chat_history (user_id, role, content) VALUES ({ph}, {ph}, {ph})",
            (session['user_id'], 'bot', reply)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Chat history save error:", e)

    return jsonify({'reply': reply})

# ---------------- HISTORY ----------------
@app.route('/get_history')
def get_history():
    if 'user_id' not in session:
        return jsonify([])

    try:
        ph = placeholder()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT role, content FROM chat_history WHERE user_id={ph} ORDER BY id ASC",
            (session['user_id'],)
        )
        rows = cursor.fetchall()
        data = [{'role': row[0], 'content': row[1]} for row in rows]
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("History error:", e)
        return jsonify([])

# ---------------- DELETE ----------------
@app.route('/delete_history', methods=['POST'])
def delete_history():
    try:
        ph = placeholder()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"DELETE FROM chat_history WHERE user_id={ph}",
            (session['user_id'],)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Delete history error:", e)

    return jsonify({'success': True})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)