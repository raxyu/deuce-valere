"""
Deuce Valere - API - System
"""
import contextlib
import datetime


class TimeManager(contextlib.ContextDecorator):

    def __init__(self, name):
        super().__init__()
        self.__name = name
        self.__start = None
        self.__end = None

    @property
    def name(self):
        return self.__name

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    def reset(self):
        self.__start = None
        self.__end = None

    @property
    def elapsed(self):
        if self.start is None:
            return 0

        elif self.end is None:
            return TimeManager.__get_time() - self.start

        else:
            return self.end - self.start

    @staticmethod
    def __get_time():
        return datetime.datetime.utcnow()

    def __enter__(self):
        self.__start = TimeManager.__get_time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__end = TimeManager.__get_time()
        # We do not surpress anything here
        return False


class CounterManager(object):

    def __init__(self, name):
        self.__name = name
        self.__count = 0
        self.__byte_count = 0

    @property
    def name(self):
        return self.__name

    @property
    def count(self):
        return self.__count

    @property
    def size(self):
        return self.__byte_count

    def add(self, count, byte_count):
        self.__count = self.__count + count
        self.__byte_count = self.__byte_count + byte_count

    def reset(self):
        self.__count = 0
        self.__byte_count = 0


class ListManager(object):

    def __init__(self, name):
        self.__name = name
        self.__current = None
        self.__expired = None

    @property
    def name(self):
        return self.__name

    @property
    def current(self):
        return self.__current

    @current.setter
    def current(self, value):
        self.__current = value

    @property
    def expired(self):
        return self.__expired

    @expired.setter
    def expired(self, value):
        self.__expired = value


class Manager(object):
    """
    Deuce Valere Manager
    """

    def __init__(self, marker_start=None, marker_end=None):
        self.__times = {
            'validation': TimeManager('validation'),
            'cleanup': TimeManager('cleanup')
        }
        self.__counters = {
            'expired': CounterManager('expired'),
            'missing': CounterManager('missing'),
            'orphaned': CounterManager('orphaned')
        }
        self.__lists = {
            'metadata': ListManager('metadata'),
            'storage': ListManager('storage')
        }
        self.__markers = {
            'start': marker_start,
            'end': marker_end
        }

    @property
    def start_block(self):
        return self.__markers['start']

    @property
    def end_block(self):
        return self.__markers['end']

    @property
    def validation_timer(self):
        return self.__times['validation']

    @property
    def cleanup_timer(self):
        return self.__times['cleanup']

    @property
    def expired_counter(self):
        return self.__counters['expired']

    @property
    def missing_counter(self):
        return self.__counters['missing']

    @property
    def orphaned_counter(self):
        return self.__counters['orphaned']

    @property
    def metadata(self):
        return self.__lists['metadata']

    @property
    def storage(self):
        return self.__lists['storage']
