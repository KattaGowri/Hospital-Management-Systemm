from flask import Flask, render_template, request, redirect, url_for, session
from twilio.rest import Client
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample storage
doctors = {}  # For simplicity; replace with a database in production
otp_storage = {}

# Twilio Configuration (Replace with your credentials)
TWILIO_SID = 'your_twilio_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in doctors and doctors[username]['password'] == password:
        session['user'] = username
        return redirect(url_for('dashboard'))
    return "Invalid Credentials", 401

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    phone = request.form['phone']
    otp = str(random.randint(1000, 9999))
    otp_storage[username] = otp

    # Send OTP via SMS
    message = client.messages.create(
        body=f"Your OTP is {otp}",
        from_=TWILIO_PHONE_NUMBER,
        to=phone
    )
    session['temp_user'] = {'username': username, 'password': password, 'phone': phone}
    return render_template('otp_verification.html')

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    otp = request.form['otp']
    temp_user = session.get('temp_user', {})
    if temp_user and otp_storage.get(temp_user['username']) == otp:
        # Save doctor data
        doctors[temp_user['username']] = {
            'password': temp_user['password'],
            'phone': temp_user['phone']
        }
        session['user'] = temp_user['username']
        otp_storage.pop(temp_user['username'], None)
        session.pop('temp_user', None)
        return redirect(url_for('dashboard'))
    return "Invalid OTP", 401

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome to the doctor dashboard, {session['user']}!"
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
