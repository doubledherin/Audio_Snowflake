import json, random
import model as m 
from flask import Flask, jsonify, render_template, redirect, request, flash, url_for
from flask import session as browser_session
from model import db_session
from sqlalchemy import desc
from api_calls import algorithm
from seed import add_to_db

app = Flask(__name__)
app.secret_key = "ADFLKASDJF"


@app.route("/")
def index():

    # get random song from db to start 
    rand = random.randrange(0, db_session.query(m.Track).count()) 
    track = db_session.query(m.Track)[rand]

    return render_template("index.html", track=track)

@app.route("/get_patterns")
def get_pattern():

    title = request.args.get("title")
    artist_name = request.args.get("artist_name")
    
    # check to see if song is in database. 
    track = m.search(artist_name, title)

    if track:
        return render_template("index.html", track=track)

    # If it is not in the db yet, call Echonest to get it
    else:
        song_data = algorithm(artist_name, title)
        add_to_db(db_session, song_data)
        track = m.search(artist_name, title)
        
        return render_template("index.html", track=track) 


@app.route("/about")
def about_page():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


