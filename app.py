from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import platform
import pymysql

app = Flask(__name__, template_folder='templates')

# Configure MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Monalisa@2001#'
app.config['MYSQL_DB'] = 'user_login_info'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/.netlify/functions/app", methods=["GET"])
def hello():
    return jsonify({"message": "Hello from Netlify Function!"})

@app.route('/login', methods=['POST'])
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
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO login_history (username, browser, os, device, ip_address, is_mobile) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, browser, os, device, ip_address, is_mobile))
    mysql.connection.commit()
    cur.close()

def log_user_info(username, browser, os, device, ip_address, is_mobile):
    print(f"User {username} logged in from {ip_address} using {browser}. OS: {os}. Device: {device}. Is Mobile: {is_mobile}")

def get_login_history(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM login_history WHERE username = %s ORDER BY login_time DESC", (username,))
    login_history = cur.fetchall()
    cur.close()
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
    app.run(debug=True)
