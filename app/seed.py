# -*- coding: utf-8 -*-
import model
from model import db_session
from api_calls import get_song_data

def main(session):
    songs = [("Cyndi Lauper", "True Colors")]

    for song in songs:

        song_data = get_song_data(song[0], song[1])

        print 0, song_data.keys(), "\n\n\n"
        #TO DO check to see if song is already in db
        track = model.Track()

        track.song_id = song_data["song_id"]
        track.key = song_data["key"]
        track.title = song_data["title"]
        track.tempo = song_data["tempo"]
        track.energy = song_data["energy"]
        track.liveness = song_data["liveness"]
        track.speechiness = song_data["speechiness"]
        track.artist_name = song_data["artist_name"]
        track.mode = song_data["mode"]
        track.acousticness = song_data["acousticness"]
        track.danceability = song_data["danceability"]
        track.time_signature = song_data["time_signature"]
        track.duration = song_data["duration"]
        track.loudness = song_data["loudness"]
        track.artist_id = song_data["artist_id"]
        track.valence = song_data["valence"]    
        track.audio_md5 = song_data["audio_md5"]
        track.instrumentalness = song_data["instrumentalness"]
        #track.echonest_track_id = song_data["echonest_track_id"]
        track.spotify_track_uri = song_data["spotify_track_uri"]
        track.analysis_url = song_data["analysis_url"]
        track.artist_foreign_ids = song_data["artist_foreign_ids"]

        db_session.add(track)

    db_session.commit()

if __name__ == "__main__":
    # session = model.connect()
    main(db_session)
