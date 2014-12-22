# -*- coding: utf-8 -*-

import unittest
from redis import Redis
from redislock.lock import Lock, lock


class TestRedisLock(unittest.TestCase):

    def setUp(self):
        self.r = Redis(db=1)

    def tearDown(self):
        self.r.flushdb()

    def test_exceptions_in_block(self):
        """Test the lock is released after an exception is raised."""
        n = "mylockname"
        try:
            with lock(n, self.r) as l:
                raise RuntimeError
        except:
            pass
        l = Lock(n, self.r)
        self.assertEqual(self.r.llen(l.mutex_key), 1)

if __name__ == '__main__':
    unittest.main()
