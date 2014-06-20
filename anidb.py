"""Main class - all anidb operations are performed from here"""

from . import AnidbModel, AnidbIDSearch, Anime, AnimeTitle
from lib.py3utils import Config

class Anidb:
    """Main class - all anidb operations are performed from here"""

    def __init__(self):
        config = Config()
        config.set_default('anidb', {
            'dbtype' : 'sqlite',
            'dbport' : '3306',
            'dbhostname' : 'localhost',
            'dbuser' : 'anidb',
            'dbpassword' : 'none',
            'dbname' : 'anidb',
            'anidbhost' : 'api.anidb.net',
            'anidbport' : '9000',
            'anidblocalport' : '9876',
            'anidbdelay' : '2',
            'anidbtimeout' : '20',
            'anidbuser' : '',
            'anidbpassword' : ''})
        self.model = AnidbModel()
        self.id_search = AnidbIDSearch()

    def get_anime_titles_by_substring(self, substring):
        return self.id_search.get_anime_titles_by_substring(substring)

    def get_anime_ids_by_substring(self, substring):
        return self.model.get_id_by_substring(substring)

    def get_animes_by_substring(self, substring):
        return self.model.get_anime_by_substring(substring)
