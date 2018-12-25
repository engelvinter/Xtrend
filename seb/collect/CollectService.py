
from common.assign_date import assign_date
from datetime import datetime, timedelta

import os


class CollectService:
    def __init__(self, last_updated, factory):
        self._last_updated = assign_date(last_updated)
        self._factory = factory

    def execute(self):                    
        today = datetime.now().date()
        one_day = timedelta(days=1)

        if self._last_updated == today:
            return

        start_date = self._last_updated + one_day
        stop_date = today

        funds = {}
        c = self._factory.create_collector(funds)
        c.execute(start_date, stop_date)

        s = self._factory.create_storer(funds)
        s.execute()