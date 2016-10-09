""" run using "python app.py" """
from flask import Flask, render_template
app = Flask('BusyBee')
app.config["DEBUG"] = True

@app.route("/")
def index():
    """ home page"""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
