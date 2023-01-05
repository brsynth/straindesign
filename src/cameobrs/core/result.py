from __future__ import absolute_import, print_function

import getpass
import time
from datetime import datetime

from cameobrs import system_info


class MetaInformation(object):
    def __init__(self, *args, **kwargs):
        super(MetaInformation, self).__init__(*args, **kwargs)
        self._system_info = system_info
        self._responsible = getpass.getuser()
        self._timestamp = time.time()

    @property
    def system_info(self):
        return self._system_info

    @property
    def responsible(self):
        return self._responsible

    @property
    def timestamp(self):
        """doc string"""
        return self._timestamp

    @property
    def human_readable_timestamp(self):
        dt = datetime.fromtimestamp(self.timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


class Result(object):
    def __init__(self, *args, **kwargs):
        super(Result, self).__init__(*args, **kwargs)
        self._meta_information = MetaInformation()

    @property
    def meta_information(self):
        return self._meta_information

    @property
    def data_frame(self):
        raise NotImplementedError

    def plot(self, grid=None, width=None, height=None, title=None, *args, **kwargs):
        raise NotImplementedError
