"""Load anime-titles.xml into database and search for id by title"""

import xml.etree.ElementTree as ET
import os.path
import zlib
from datetime import datetime, timedelta
from . import AnidbModel, Anime, AnimeTitle

class AnidbIDSearch:
    """Load anime-titles.xml into database and search for id by title"""

    def __init__(self):
        self.model = AnidbModel()

    def get_anime_titles_by_substring(self, substring):
        """ Return list of anime titles that match partial title.
            Used for selecting the proper anime id from list.
            Preference is given to the english official title,
            if not available then x-jat main title is returned.
        """
        titles = []
        for id in self.model.get_id_by_title(substring):
             otitle = self.model.get_title(id, 'en', 'official')
             if otitle != None:
                 titles.append(otitle)
             else:
                 mtitle = self.model.get_title(id, 'x-jat', 'main')
                 if mtitle != None:
                     titles.append(mtitle)
        return titles

    def load_anime_titles_xml(self):
        """ retrieve anime_titles_xml from anidb and save in database
            This makes searching for anime much faster and reduces load
            on anidb servers.  This should only be needed a few times at the
            start of the anime season.  
            Slow operation, should be run off hours if possible.
        """
        try:
            last_load = self.model.get_setting('last_title_load').strptime('%m/%d/%Y %H:%M')
            if last_load > datetime.now() - timedelta(days = 1):
                return
        except:
            # Never loaded, so go ahead
            pass
        url = 'http://anidb.net/api/anime-titles.xml.gz'
#        with open(os.path.dirname(__file__) + '/anime-titles.xml.gz', 'rb') as response:
        with urllib.request.urlopen(url) as response:
            data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS).decode()

        for child in ET.fromstring(data):
            aid = child.attrib['aid']
            for t in child:
                if t.attrib['{http://www.w3.org/XML/1998/namespace}lang'] in ('en', 'x-jat'):
                    anime_title = AnimeTitle(anidbid = aid, 
                        language = t.attrib['{http://www.w3.org/XML/1998/namespace}lang'],
                        type = t.attrib['type'],
                        title = t.text)
                    print ("Adding: ", anime_title.anidbid, anime_title.title, 
                           anime_title.language, anime_title.type)
                    self.model.add_title(anime_title)
        self.model.add_setting('last_title_load', datetime.now().strftime('%m/%d/%Y %H:%M'))
