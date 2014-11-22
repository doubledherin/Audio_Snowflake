from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, PickleType
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///audiosnowflake.db", echo=False)
db_session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = db_session.query_property()

class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key = True)
    song_id = Column(String(50))
    key = Column(Integer)
    title = Column(String(100))
    tempo = Column(Float)
    energy = Column(Float)
    liveness = Column(Float)
    speechiness = Column(Float)
    artist_name = Column(String(100))
    mode = Column(Integer)
    acousticness = Column(Float)
    danceability = Column(Float)
    time_signature = Column(Integer)
    duration = Column(Float)
    loudness = Column(Float)
    artist_id = Column(String(50))
    valence = Column(Float) 
    audio_md5 = Column(String(50))
    instrumentalness = Column(Float)
    spotify_track_uri = Column(String(50))
    patterns = Column(String(300))
    rotation_speed = Column(Float)

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key = True)
    filename = Column(String(50))
    artist_name = Column(String(100))
    title = Column(String(100))


