echo "Installation Starting........."
export DATABASE_URL=mysql+pymysql://ujmpxoqqhngyt0gb:1OIbryg4bnDgFbT34umw@bpvu52ygesedno1kez8l-mysql.services.clever-cloud.com:3306/bpvu52ygesedno1kez8l

# Install dependencies
pip3 install -r requirements.txt

# Install Waitress
pip3 install waitress

# Start the Flask app using Waitress
waitress-serve --port=$PORT app:app
