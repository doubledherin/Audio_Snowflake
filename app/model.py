import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://coder@localhost/audiosnowflake2")

engine = create_engine(DATABASE_URL, echo=False)

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
    artist_name = Column(String(100))
    mode = Column(Integer)
    time_signature = Column(Integer)
    duration = Column(Float)
    loudness = Column(Float)
    artist_id = Column(String(50))
    valence = Column(Float) 
    audio_md5 = Column(String(50))
    spotify_track_uri = Column(String(50))
    patterns = Column(Text)
    sections = Column(Text)
    rotation_duration = Column(Float)

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key = True)
    filename = Column(String(50))
    artist_name = Column(String(100))
    title = Column(String(100))


