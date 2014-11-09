from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
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

    # the below come from get_song_data function
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
    # echonest_track_id = Column(String(50))
    spotify_track_uri = Column(String(50))
    analysis_url = Column(String(150))
    # artist_foreign_ids = Column(String (150))


    # values for the outer ring (1 per track)
    outer_a = Column(Float)
    outer_b = Column(Float)
    outer_t = Column(Float)
    outer_h = Column(Float)

    # values for the interior rings (1 per section)
    section0_a = Column(Float)
    section0_b = Column(Float)
    section0_t = Column(Float)
    section0_h = Column(Float)

    section1_a = Column(Float)
    section1_b = Column(Float)
    section1_t = Column(Float)
    section1_h = Column(Float)

    section2_a = Column(Float)
    section2_b = Column(Float)
    section2_t = Column(Float)
    section2_h = Column(Float)

    section3_a = Column(Float)
    section3_b = Column(Float)
    section3_t = Column(Float)
    section3_h = Column(Float)

    section4_a = Column(Float)
    section4_b = Column(Float)
    section4_t = Column(Float)
    section4_h = Column(Float)



