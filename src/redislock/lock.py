# -*- coding: utf-8 -*-

from redis import Redis


class Lock(object):
    """
    Lock implemented on top of redis.
    """

    def __init__(self, name, redis_connection, timeout=60):
        """
        Create, if necessary the lock variable in redis.

        We utilize the ``blpop`` command and its blocking behavior.

        The ``_key`` variable is used to check, whether the mutex exists or not
        while the ``_mutex`` variable is the actual mutex.
        """
        self._key = 'lock:name:%s' % name
        self._mutex = 'lock:mutex:%s' % name
        self._timeout = timeout
        self.redis_connection = redis_connection
        self._init_mutex()

    @property
    def mutex_key(self):
        return self._mutex

    def lock(self):
        """
        Lock and block.

        Raises:
            RuntimeError, in case of synchronization issues.
        """
        res = self.redis_connection.blpop(self._mutex, self._timeout)
        if res is None:
            raise RuntimeError

    def unlock(self):
        self.redis_connection.rpush(self._mutex, 1)

    def _init_mutex(self):
        """
        Initialize the mutex, if necessary.

        Use a separate key to check for the existence of the "mutex",
        so that we can utilize ``getset``, which is atomic.
        """
        exists = self.redis_connection.getset(self._key, 1)
        if exists is None:
            self.redis_connection.lpush(self._mutex, 1)


class lock():
    def __init__(self, name, redis_connection, timeout=60):
        self.l = Lock(name, redis_connection, timeout)
    def __enter__(self):
        self.l.lock()
        return self.l
    def __exit__(self, type, value, traceback):
        self.l.unlock()
