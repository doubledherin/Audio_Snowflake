from flask import Flask, render_template, redirect, request, flash
from flask import session as browser_session
import model as m 

from sqlalchemy import desc

track_id = "5u1la2hnzQOpWYdT0Vyegn"
app = Flask(__name__)
app.secret_key = "ADFLKASDJF"

@app.route("/")
def index():
    # TO DO add code to randomly generate an image
    return render_template("index.html", track_id=track_id)

@app.route("/new_song")
def get_new_song():
    
    title = request.args.get("title")
    artist_name = request.args.get("artist_name")

    print title
    print artist_name

    # check to see if song is in database. 
    song = m.session.query(m.Track).filter_by(title=title).filter_by(artist_name=artist_name).first()


    if song:
        md5 = song.audio_md5

        print "Song in database!"
    else:
        print "Song not in database!"

    return render_template("index.html", track_id=track_id)


if __name__ == "__main__":
    app.run(debug=True)
