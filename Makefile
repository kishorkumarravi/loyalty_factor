dev-env:
	rm -rf ../env/
	cd ..
	python3 -m venv env
	. ./env/bin/activate
	pip3 install --upgrade pip

init:
	pip install -r requirements.txt

run:
	python3 app.py