class MusicCastException(Exception):
    pass


class MusicCastGroupException(MusicCastException):
    pass


class MusicCastConnectionException(MusicCastException):
    pass


class MusicCastConfigurationException(MusicCastGroupException):
    pass
