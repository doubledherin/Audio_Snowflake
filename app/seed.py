# -*- coding: utf-8 -*-


# This is meant to be run only on the command line;
# a version without a list of songs (add_song_to_db.py) is run by the app

import json
from time import sleep

from models import db_session, engine, Base, Track
from api_calls import algorithm


def create_tables(engine):
    Base.metadata.create_all(engine)


def add_song_to_db(session):

    songs = [("Radiohead", "Weird Fishes"),
             ("Elliott Smith", "Waltz #2"),
             ("Cyndi Lauper", "True Colors"),
             ("Mozart", "Symphony No. 40 in G Minor"),
             ("Madonna", "La Isla Bonita"),
             ("Jose Gonzalez", "Heartbeats"),
             ("Erik Satie", "Gymnopedie No. 1"),
             ("Radiohead", "Black Star"),
             ("Radiohead", "True Love Waits"),
             ("Christopher O'Riley", "Black Star"),
             ("Christopher O'Riley", "True Love Waits"),
             ("charles atlas", "the snow before us"),
             ("Beirut", "Elephant Gun"),
             ("Neutral Milk Hotel", "Oh Comely"),
             ("Arcade Fire", "Neighborhood #1"),
             ("Leonard Cohen", "Famous Blue Raincoat"),
             ("Pinback", "Penelope"),
             ("Sigur Rós", "Starálfur"),
             ("Excuses for Skipping", "Gravity"),
             ("Cake", "Never There"),
             ("Cake", "The Distance"),
             ("the chameleons", "silence sea and sky"),
             ("cocteau twins", "aikea-guinea"),
             ("henryk górecki", "quasi una fantasia: string quartet no. 2"),
             ("descendents", "wendy"),
             ("clint mansell", "together we will live forever"),
             ]

    for song in songs:

        song_data = algorithm(song[0], song[1])

        patterns = song_data["patterns"]
        patterns_json = json.dumps(patterns)

        sections = song_data["sections"]
        sections_json = json.dumps(sections)

        track = Track()

        track.song_id = song_data["song_id"]
        track.key = song_data["key"]
        track.title = song_data["title"]
        track.tempo = song_data["tempo"]
        track.energy = song_data["energy"]
        track.artist_name = song_data["artist_name"]
        track.mode = song_data["mode"]
        track.time_signature = song_data["time_signature"]
        track.duration = song_data["duration"]
        track.loudness = song_data["loudness"]
        track.artist_id = song_data["artist_id"]
        track.valence = song_data["valence"]
        track.audio_md5 = song_data["audio_md5"]
        track.spotify_track_uri = song_data["spotify_track_uri"]
        track.patterns = patterns_json
        track.sections = sections_json
        track.rotation_duration = song_data["rotation_duration"]
        db_session.add(track)
        db_session.commit()
        sleep(5)


if __name__ == "__main__":
    create_tables(engine)
    add_song_to_db(db_session)
