
from . Download import Download
import calendar
from datetime import datetime


class Factory:
    def __init__(self):
        pass

    def create_downloader(self, month):
        link = "https://www.pensionsmyndigheten.se/content/dam/pensionsmyndigheten/blanketter---broschyrer---faktablad/statistik/premiepension/m%C3%A5nadsstatistik/%C3%A4ldre-m%C3%A5nadsstatistik-%C3%B6ver-fondhandel"  # noqa: E501
        now = datetime.now()
        day = calendar.monthrange(now.year, month)[1]
        return Download(link, datetime(now.year, month, day))
