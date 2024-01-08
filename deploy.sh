#!/bin/bash

# Install MySQL development headers and libraries
# Note: The following lines might not be needed on Netlify, as they manage the build environment
# apt-get update
# apt-get install -y python3-dev default-libmysqlclient-dev build-essential

echo "Installation Starting........."

# Install Python dependencies
pip3 install --upgrade pip
pip3 install -r requirements.txt  # or however you manage your dependencies

# Check if MySQL server is available
# If not available, you might need to skip this part or adjust your script accordingly
if [ -x "$(command -v mysql)" ]; then
    # MySQL server is available
    echo "MySQL server is available."
else
    # MySQL server is not available, handle accordingly
    echo "MySQL server is not available. Skipping MySQL-related steps."
fi

# Run your application
python app.py

