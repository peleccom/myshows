# -*- coding: utf-8 -*-
import six
import types

class BaseObject(object):
    id = None

    def __init__(self, json_dict):
        self.set_defaults()
        self._parse(json_dict)

    def set_defaults(self):
        pass

    def _parse(self, json_dict):
        pass
        
    def _set_attr_from_dict(self, dict_obj, keys):
        for key in keys:
            if isinstance(key, six.string_types):
                setattr(self, key, dict_obj[key])
            if isinstance(key, tuple) or isinstance(key, list):
                if len(key) == 2:
                    setattr(self, key[0], dict_obj[key[1]])
                else:
                    setattr(self, key[0], key[2](dict_obj[key[1]]))



class SeriesStatus(object):
    CANCELLED = 'Canceled/Ended'

    def __init__(self, str):
        pass

class WatchStatus(object):
    
    def __init__(self, str):
        pass


class BaseSeries(BaseObject):
    def __repr__(self):
        return '<Series %s>' % (self.id if self.id else '???')
     
    def __str__(self):
        return '%s (%s)' % (self.title if self.title else '???', self.ruTitle if self.ruTitle else '???')

class ShortSeries(BaseSeries):
    def _parse(self, json_dict):
        self._set_attr_from_dict(json_dict, [
            "title",
            "ruTitle",
            ("status", "showStatus", lambda x: SeriesStatus(x)),
            "rating",
            ("id", "showId"),
            "runtime",
            "totalEpisodes",
            "watchedEpisodes",
            ("watchStatus", "watchStatus", lambda x: WatchStatus(x)),
        ])
        


class Series(BaseSeries):

    def set_default(self):
        self.title = ''
        self.ruTitle = ''
        self.status = None
        self.country = ''
        self.started = None
        self.ended = None
        self.year = 0
        self.kinopoiskId = None
        self.tvrageId = None
        self.imdbId = None
        self.watching = 0
        self.voted = 0
        self.rating = .0
        self.runtime = 0
        self.image = ''
        self.genres = []
        self.episodes = []

    def _parse(self, json_dict):
        super(Series, self)._parse(json_dict)
        self._set_attr_from_dict(json_dict, [
            "status",
            "rating",
            "genres",
            "genres",
            "title",
            "started",
            "country",
            "image",
            "watching",
            "ruTitle",
            "ended",
            "voted",
            "tvrageId",
            "year",
            "kinopoiskId",
            "runtime",
            "id",
            "imdbId"
        ])

class Episode(BaseObject):

    def set_defaults(self):
        self.title = ''
        self.airDate = None
        self.shortName = ''
        self.tvrageLink = ''
        self.image = ''
        self.seasonNumber = 0
        self.episodeNumber = 0
        self.productionNumber = 0
        self.sequenceNumber = 0

    def _parse(self, json_dict):
        pass    



