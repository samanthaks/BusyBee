# BusyBee

## First-Time Setup
### To get BusyBee up and running quickly:
1. Install Fabric
	```$ pip install fabric```
2. Complete set up with 
	```$ fab first_setup```

### The long way:
1. Ensure that you have Python 2.7
2. Install your Virtual Envitonment 
	```$ pip install virtualenv ```
3. Create virtual enviornment
	```$ virtualenv . ```
4. Enter virtual environment 
	```$source bin/activate ```
5. Install all dependencies
	```(BusyBee)$ pip install -r requirements.txt ```
6. To exit virtualenv
	```$ deactivate ```

### And finally:
Run script. 
```$ fab run_local```


## Developing using Sublime
1. Download Sublime Text
	[Sublime Text](https://www.sublimetext.com/)
2. Install Appropriate Packages in Sublime
	1. Open Package Control --> ctrl+shift+p (Windows, Linux) or cmd+shift+p (OS X)
    2. Select Package Control: Install Package --> Install [Jedi](http://jedi.jedidjah.ch/en/latest/)
	3. Select Package Control: Install Package --> Install [SublimeLinter](http://www.sublimelinter.com/en/latest/)
	4. Select Package Control: Install Package --> Install [SublimeLinter-flake8](https://github.com/SublimeLinter/SublimeLinter-flake8)
3. Follow the intructions at [https://github.com/SublimeLinter/SublimeLinter-flake8](https://github.com/SublimeLinter/SublimeLinter-flake8) to set up flake-8

## Run Testing
```$ fab run_tests```

## About BusyBee
* Built in [Flask](http://flask.pocoo.org/)
* [Flask-Mongoengine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/) and [Mongoengine](http://mongoengine.org/) are used to interface with [MongoDB](https://www.mongodb.com/)
* Testing uses unittest and flask_testing
* Continuous Integration with Travis
* Branch Coverage Checking with Coverall
