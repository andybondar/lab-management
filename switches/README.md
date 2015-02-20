Requirements:
'Python virtual environment creator' package

sudo apt-get install python-virtualenv

for Ubuntu:


Create Python virtual environment:

virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt
