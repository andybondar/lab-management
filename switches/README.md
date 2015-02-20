### Requirements:

'Python virtual environment creator' package

For Ubuntu:

	sudo apt-get install python-virtualenv



Create Python virtual environment:

	virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt


Run script:

	./lacp.py {enable|disable}
