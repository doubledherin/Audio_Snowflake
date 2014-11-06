from flask import Flask, render_template, redirect, request, flash
from flask import session as browser_session
import model
from sqlalchemy import desc


app = Flask(__name__)
app.secret_key = "ADFLKASDJF"

@app.route("/")
def index():
    # TO DO add code to randomly generate an image
    return render_template("index.html")


@app.route("/signup")
def signup_view():
    pass
    # return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_complete():
    pass

if __name__ == "__main__":
    app.run(debug=True)