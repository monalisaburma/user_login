#!/bin/bash

# Install MySQL development headers and libraries
# apt-get update
# apt-get install -y python3-dev default-libmysqlclient-dev build-essential
echo "Installation Starting........."
#sudo apt-get update && apt-get upgrade python-pip
#sudo yum install python-pip
#sudo yum update python-pip
# Install Python dependencies, including mysqlclient
#pip3 install --upgrade pip
#python -m pip install --upgrade pip
#python3 -m pip install --upgrade pip
# pip3 install git+https://github.com/PyMySQL/mysqlclient-python
export DATABASE_URL=mysql://ujmpxoqqhngyt0gb:1OIbryg4bnDgFbT34umw@bpvu52ygesedno1kez8l-mysql.services.clever-cloud.com:3306/bpvu52ygesedno1kez8l
pip3 install -r requirements.txt  # or however you manage your dependencies
python app.py
printenv


# Add any other deployment steps here
# ...

# Example: Build your site or start your server
# npm run build  # replace with your build command
