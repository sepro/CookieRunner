CookieRunner Readme
===================

Installation
------------

Python >= 3.3 and pip3 are required

    sudo apt-get install python3
    sudo apt-get install pip3

Install virtualenv

    sudo pip3 install virtualenv


Clone the repository into a directory CookieRunner

    git clone https://github.com/sepro/CookieRunner.git CookieRunner

Set up the virtual environment
  
    virtualenv --python=python3 CookieRunner/

Activate the virtual environment

    cd CookieRunner/
    source bin/activate

Install the requirements

    pip3 install -r requirements.txt

Copy the configuration template to config.py

    cp config.template.py config.py

Change settings in config.py

Running the app
---------------

After configuring the app it can be run as any flask app. 

    python run.py
