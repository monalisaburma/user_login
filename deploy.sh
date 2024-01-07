#!/bin/bash

# Install MySQL development headers and libraries
apt-get update
apt-get install -y libmysqlclient-dev
echo "Installation Starting........."
# Install Python dependencies, including mysqlclient
pip3 install --upgrade pip
pip3 install git+https://github.com/PyMySQL/mysqlclient-python
pip3 install -r requirements.txt  # or however you manage your dependencies
python app.py

# Add any other deployment steps here
# ...

# Example: Build your site or start your server
# npm run build  # replace with your build command
