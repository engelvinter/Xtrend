
from datetime import datetime
from . Factory import Factory

class LoadService:
    def __init__(self):
        pass

    def execute(self):
        factory = Factory()
        download = factory.create_downloader()
        excel_file = download.execute()
        return excel_file