from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, sessionmaker
from lib.py3utils import ModelHelper
import sys

Base = declarative_base()
class Anime(Base):
    __tablename__ = 'anime'
    anidbid = Column(Integer, primary_key = True) 
    title = Column(String(250), nullable = False) 

class AnimeTitle(Base):
    __tablename__ = 'anime_title'
    anidbid = Column(Integer, primary_key = True) 
    language = Column(String(10), primary_key = True) 
    type = Column(String(10), primary_key = True) 
    title = Column(String(250), primary_key = True) 

    def __repr__(self):
        return "<AnimeTitle (anidbid = %d, language = '%s', type = '%s', title = '%s')>" % \
            self.anidbid, self.language, self.type, self.title

class Setting(Base):
    __tablename__ = 'setting'
    key = Column(String(20), primary_key = True) 
    value = Column(String(250), nullable = False) 

    def __repr__(self):
        return "<Setting (key = '%s', value = '%s')>" % \
            self.key, self.value

class AnidbModel():
    def __init__(self):
        self.engine = create_engine(ModelHelper().getenginestring('anidb'))
        self.DBSession = sessionmaker(bind = self.engine)
        self.db = self.DBSession()

    def update_database(self):
        print("Updating Database")

        Base.metadata.create_all(self.engine)
        # todo Create/Update tables

        self.update_setting('version', __version__)
        self.db.commit()

    def get_version(self):
        try:
            version = self.db.query(Setting).filter(Setting.key == 'version').one().value
            return version
        except:
            print("Unable to load version", sys.exc_info())
            return None

    def get_session(self):
        return self.db

#### Anime Operations
    def get_anime_by_substring(self, substring):
        anime = []
        for anidbid in self.get_id_by_title(title):
           a = get_anime_by_id(anidbid)
           if a != None:
               anime.append(a)
        return anime

    def get_anime_by_id(self, anidbid):
        anime = self.db.query(Anime).filter(Anime.anidbid == anidbid).one()
# refresh anime if it's over a week/day old?
        if anime == None:
            anime = anidb_lookup_anime(anidbid)
        return anime

    def add_anime(self, anime):
        self.db.merge(Anime)

    def anidb_lookup_anime(self, anidbid):
# todo add upd module to do actual lookup
# add_anime to cache
        return None

#### Episode Operations

#### Group Operations

#### Title Operations
    def add_title(self, anime_title):
        try:
            self.db.add(anime_title)
            self.db.commit()
        except(IntegrityError):
            self.db.rollback()
            print("Duplicate Entry: ", anime_title.anidbid, 
                   anime_title.language, anime_title.type, anime_title.title)

    def get_titles(self):
        return self.db.query(AnimeTitle).all()

    def get_id_by_title(self, title):
        titles = self.db.query(AnimeTitle).filter(AnimeTitle.title.ilike('%' + title + '%')).all()
        anidbids = []
        for title in titles:
            anidbids.append(title.anidbid)
        return sorted(set(anidbids))

    def get_title(self, anidbid, language, type):
        return self.db.query(AnimeTitle).filter(AnimeTitle.anidbid == anidbid,
                                                AnimeTitle.language == language,
                                                AnimeTitle.type == type).first()

#### Setting Operations
    def get_setting(self, key):
        return self.db.query(Setting).filter(Settings.key == key).one()

    def add_setting(self, new_key, new_value):
        self.db.merge(Setting(key = new_key, value = new_value))

