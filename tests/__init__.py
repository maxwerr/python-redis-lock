# -*- coding: utf-8 -*-

import unittest
from redis import Redis
from redislock.lock import Lock, lock


class TestRedisLock(unittest.TestCase):

    def setUp(self):
        self.r = Redis(db=1)
        self.name = "mylockname"

    def tearDown(self):
        self.r.flushdb()

    def test_exceptions_in_block(self):
        """Test the lock is released after an exception is raised."""
        try:
            with lock(self.name, self.r) as l:
                raise RuntimeError
        except:
            pass
        l = Lock(self.name, self.r)
        self.assertEqual(self.r.llen(l.mutex_key), 1)

    def test_second_lock_should_timeout(self):
        """Test the second lock timeout in context of the first."""
        reached = False
        try:
            with lock(self.name, self.r) as l1:
                with lock(self.name, self.r, timeout=.1) as l2:
                    # this shouldn't occur
                    reached = True
        except:
            pass
        self.assertEqual(reached, False)


if __name__ == '__main__':
    unittest.main()
