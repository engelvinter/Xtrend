
from . Download import Download

class Factory:
    def __init__(self):
        pass

    def create_downloader(self, date):
        link = "https://www.pensionsmyndigheten.se/content/dam/pensionsmyndigheten/blanketter---broschyrer---faktablad/statistik/premiepension/m%C3%A5nadsstatistik/%C3%A4ldre-m%C3%A5nadsstatistik-%C3%B6ver-fondhandel"  # noqa: E501
        
        return Download(link, date)
