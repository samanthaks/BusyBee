# BusyBee

## First-Time Setup
Follow these steps to get BusyBee up and running:
1. Ensure that you have Python 3.5. If not, update python.
2. Install [MongoDB](https://www.mongodb.com/) ([Ubuntu Linux](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/), [OSX](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/#install-mongodb-with-homebrew))
3. Set up your virtual environment and download [Flask](http://flask.pocoo.org/). See tutorial [here](http://flask.pocoo.org/docs/0.11/installation/)


## Developing using Sublime
1. Download Sublime Text
... [Sublime Text](https://www.sublimetext.com/)
2. Install Appropriate Packages in Sublime
..1. Open Package Control 
...>ctrl+shift+p (Win, Linux) or cmd+shift+p (OS X)
..2. Select Package Control: Install Package --> Install Jedi (this is for python autocompletion)
..3. Select Package Control: Install Package --> Install SublimeLinter
..4. Select Package Control: Install Package --> Install SublimeLinter-pylint
 (this is for static analysis)
3. Follow the intructions at [https://github.com/SublimeLinter/SublimeLinter-pylint](https://github.com/SublimeLinter/SublimeLinter-pylint) to set up pylint


## About BusyBee
* Built in [Flask](http://flask.pocoo.org/)
* Flask-Mongoengine and Mongoengine are used to interface with MongoDB
