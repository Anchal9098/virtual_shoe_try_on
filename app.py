from flask import Flask, render_template, request, redirect, url_for, flash, session
import subprocess
import threading

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Mock database (for simplicity)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Simple login validation (using mock database)
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('foot_tracking_page'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users:
            flash('Username already exists')
        else:
            users[username] = password
            flash('Account created successfully!')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/foot_tracking')
def foot_tracking_page():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('foot_tracking.html')

@app.route('/start-tryon')
def start_tryon():
    # Start the foot_tracking.py in a separate thread
    threading.Thread(target=start_camera).start()
    return "Try-on started!"

def start_camera():
    # Call your foot_tracking.py script here
    subprocess.call(["python", "foot_tracking.py"])

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
