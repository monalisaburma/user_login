from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import platform
import os

app = Flask(__name__, template_folder='templates')

clever_cloud_db_uri = "mysql+pymysql://ujmpxoqqhngyt0gb:1OIbryg4bnDgFbT34umw@bpvu52ygesedno1kez8l-mysql.services.clever-cloud.com:3306/bpvu52ygesedno1kez8l"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or clever_cloud_db_uri
print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}") 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    browser = db.Column(db.String(255), nullable=False)
    os = db.Column(db.String(255), nullable=False)
    device = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    is_mobile = db.Column(db.Boolean, nullable=False)
    login_time = db.Column(db.DateTime, default=db.func.now(), nullable=False)

with app.app_context():
    # Create database tables if they don't exist
    db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/.netlify/functions/app", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Netlify Function!"})

@app.route('/', methods=['POST'])
def process_login():
    username = request.form['username']
    user_agent = request.user_agent.string

    # Extract browser information from the user agent string
    browser = get_browser_from_user_agent(user_agent)

    # Extract OS information using the platform library
    os = platform.system()

    device = request.user_agent.string
    ip_address = request.remote_addr

    is_mobile = 'Mobi' in (request.user_agent.platform or '')

    # Store information in the database
    store_login_info(username, browser, os, device, ip_address, is_mobile)

    # Log user information
    log_user_info(username, browser, os, device, ip_address, is_mobile)

    # Display login history to the user
    login_history = get_login_history(username)
    return render_template('dashboard.html', username=username, login_history=login_history)

def store_login_info(username, browser, os, device, ip_address, is_mobile):
    new_login = LoginHistory(
        username=username,
        browser=browser,
        os=os,
        device=device,
        ip_address=ip_address,
        is_mobile=is_mobile
    )
    db.session.add(new_login)
    db.session.commit()

def log_user_info(username, browser, os, device, ip_address, is_mobile):
    print(f"User {username} logged in from {ip_address} using {browser}. OS: {os}. Device: {device}. Is Mobile: {is_mobile}")

def get_login_history(username):
    login_history = LoginHistory.query.filter_by(username=username).order_by(LoginHistory.login_time.desc()).all()
    return login_history

def get_browser_from_user_agent(user_agent):
    # Extract browser information from the user agent string
    if 'Firefox' in user_agent:
        return 'Firefox'
    elif 'Chrome' in user_agent:
        return 'Chrome'
    elif 'Safari' in user_agent:
        return 'Safari'
    elif 'Edge' in user_agent:
        return 'Edge'
    elif 'IE' in user_agent:
        return 'Internet Explorer'
    else:
        return 'Unknown'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

