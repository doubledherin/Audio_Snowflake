# -*- coding: utf-8 -*-
import model
from model import db_session
from sys import argv
# from api_calls import get_song_data



import json

values = [{"a": 640, "b": 260, "h": 19}, {"a": 300, "b": 140, "h": 175}, {"a": 100, "b": 175, "h": 175}, {"a": 475, "b": 50, "h": 50}, {"a": 490, "b": 190, "h": 90}]

values_json = json.dumps(values)

def add_to_db(session, song_data):
    # songs = [(artist, title)]

    # for song in songs:

    # song_data = get_song_data(artist, title)

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
    # track.analysis_url = song_data["analysis_url"]
    # track.artist_foreign_ids = song_data["artist_foreign_ids"]
    track.patterns = values_json
    db_session.add(track)

    db_session.commit()

if __name__ == "__main__":
    # session = model.connect()
    script, artist, title = argv
    add_to_db(db_session, artist, title)
