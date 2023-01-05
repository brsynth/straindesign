from __future__ import absolute_import, print_function

import os
import multiprocessing
import warnings

import pytest
from cameobrs.parallel import SequentialView

views = [SequentialView()]

try:
    from cameobrs.parallel import MultiprocessingView

    views.append(MultiprocessingView())
except ImportError:
    MultiprocessingView = None

try:
    from cameobrs.parallel import RedisQueue
except ImportError:
    RedisQueue = None
isRedisQueue = False

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from IPython.parallel import Client, interactive
except ImportError:
    try:
        from ipyparallel import Client, interactive
    except ImportError:

        def interactive(f):
            return f


SOLUTION = [x**2 for x in range(100)]


if os.getenv("REDIS_PORT_6379_TCP_ADDR"):
    REDIS_HOST = os.getenv("REDIS_PORT_6379_TCP_ADDR")  # wercker
else:
    REDIS_HOST = "localhost"


@interactive
def to_the_power_of_2_interactive(arg):
    return arg**2


def to_the_power_of_2(arg):
    return arg**2


class TestView:
    @pytest.mark.parametrize("view", views)
    def test_map(self, view):
        assert view.map(to_the_power_of_2, list(range(100))) == SOLUTION

    @pytest.mark.parametrize("view", views)
    def test_apply(self, view):
        for i in range(100):
            assert view.apply(to_the_power_of_2, i) == SOLUTION[i]

    @pytest.mark.skipif(not MultiprocessingView, reason="no multiprocessing available")
    def test_length(self):
        view = MultiprocessingView()
        assert len(view) == multiprocessing.cpu_count()

        view = MultiprocessingView(4)
        assert len(view) == 4

        view = MultiprocessingView(processes=3)
        assert len(view) == 3


@pytest.mark.skipif(not isRedisQueue, reason="no redis queue available")
class TestRedisQueue:
    def test_queue_size(self):
        print(REDIS_HOST)
        print(os.getenv("REDIS_PORT_6379_TCP_ADDR"))
        queue = RedisQueue("test-queue-size-1", maxsize=1, host=REDIS_HOST)
        queue.put(1)
        with pytest.raises(multiprocessing.queues.Full):
            queue.put(1)

        queue = RedisQueue("test-queue-size-2", maxsize=2, host=REDIS_HOST)
        queue.put(1)
        queue.put(1)
        with pytest.raises(multiprocessing.queues.Full):
            queue.put(1)
        queue.get()
        queue.get()
        with pytest.raises(multiprocessing.queues.Empty):
            queue.get_nowait()

    def test_queue_objects(self):
        queue = RedisQueue("test-queue", maxsize=100, host=REDIS_HOST)
        # put int
        queue.put(1)
        v = queue.get_nowait()
        assert v == 1
        assert isinstance(v, int)

        # put str
        queue.put("a")
        v = queue.get_nowait()
        assert v == "a"
        assert isinstance(v, str)

        # put float
        queue.put(1.0)

        v = queue.get_nowait()
        assert v == 1.0
        assert isinstance(v, float)

        # put list
        queue.put([1, 3, 4, 5, "a", "b", "c", 1.0, 2.0, 3.0])
        v = queue.get_nowait()
        assert v == [1, 3, 4, 5, "a", "b", "c", 1.0, 2.0, 3.0]
        assert isinstance(v, list)

        # put dict
        queue.put({"x": "y"})
        v = queue.get_nowait()
        assert v == {"x": "y"}
        assert isinstance(v, dict)

    def test_queue_len(self):
        queue = RedisQueue("test-queue-len", maxsize=100, host=REDIS_HOST)
        assert queue.length == 0
        queue.put(1)
        assert queue.length == 1
        queue.put(1)
        assert queue.length == 2
        queue.put(1)
        assert queue.length == 3
        queue.get_nowait()
        assert queue.length == 2
        queue.get_nowait()
        assert queue.length == 1
        queue.get_nowait()
        assert queue.length == 0
