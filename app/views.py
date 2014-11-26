import base64, json, os, random

from flask import Flask, render_template, redirect, request

from werkzeug import secure_filename

import model as m 
from model import db_session
from api_calls import algorithm
from add_to_db import add_song_to_db, add_image_to_db

app = Flask(__name__)

# Does not use form entry
@app.route("/")
def index():

    # Get a random song from the database to start with 
    rand = random.randrange(0, db_session.query(m.Track).count()) 
    track = db_session.query(m.Track)[rand]

    return redirect("/render_template?song_id=%s" % track.song_id)

# Uses form entry
@app.route("/get_patterns")
def get_pattern():

    # Get the song title and artist name from the web form
    title = request.args.get("title").lower()
    artist_name = request.args.get("artist_name").lower()
    
    # If nothing entered into form
    if not artist_name and not title:
        return redirect("/")

    # If only title entered
    elif not artist_name:
        track = db_session.query(m.Track).filter_by(title=title).first()

    # If only artist name entered
    elif not title:
        track = db_session.query(m.Track).filter_by(artist_name=artist_name).first()

    # If both artist and title entered
    else:
        track = db_session.query(m.Track).filter_by(artist_name=artist_name).filter_by(title=title).first()

    if track:

        return redirect("/render_template?song_id=%s" % track.song_id)
    
    # If not in database, call Echo Nest
    else:

        song_data = algorithm(artist_name, title)
        
        # HTML prints message to screen saying sorry, no go
        if not song_data:
            return render_template("index.html", track=None, patterns=None, sections=None)


        # Use song_id to see if song is already in the database
        # (This avoids problems if user doesn't use accents or gives a partial entry [e.g., skips "the"])
        song_id = song_data["song_id"]

        track = db_session.query(m.Track).filter_by(song_id=song_id).first()

        # If song id is in the database
        if track:
            return redirect("/render_template?song_id=%s" % track.song_id)

        # If song id is not in the database
        else:

            # Add it to the database
            add_song_to_db(db_session, song_data)

            # Get it from the database (using song id)
            track = db_session.query(m.Track).filter_by(song_id=song_id).first()
            
            return redirect("/render_template?song_id=%s" % track.song_id)

# Uses song id to query database and get data needed for index.html
@app.route("/render_template")
def render():

    song_id=request.args.get('song_id')

    track = db_session.query(m.Track).filter_by(song_id=song_id).first()

    patterns = track.patterns
    json_patterns = json.loads(patterns)

    sections = track.sections
    json_sections = json.loads(sections) 

    return render_template("index.html", track=track, patterns=json_patterns, sections=json_sections)

# Takes snapshot of canvas
@app.route("/add_snowflake", methods=["POST"])
def add_snowflake():
    filename = request.form["song_id"] + ".png"
    image = request.form["img"]
    artist_name = request.form["artist_name"].title()
    title = request.form["title"].title()

    if image:

        # Decode base64
        img_type, img_b64data = image.split(",", 1)
        image_data = base64.b64decode(img_b64data)

        # Write to a file using the song id as the filename
        fout = open(os.path.join("static/uploads", filename), "wb")
        fout.write(image_data)
        fout.close()

        # Store in database
        add_image_to_db(db_session, filename, artist_name, title)

    return "OK"


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/gallery")
def gallery_page():

    images = db_session.query(m.Image).all()

    return render_template("gallery.html", images=images)    


if __name__ == "__main__":
    app.run(debug=True)


