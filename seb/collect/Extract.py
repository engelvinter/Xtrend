import locale
from datetime import datetime


class Extract:
    def __init__(self, content, fund_callback):
        #locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')
        locale.setlocale(locale.LC_ALL, '')
        self._content = content
        self._fund_callback = fund_callback

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d") 
        except:
            return datetime.strptime(date_str, "%y-%m-%d")
        
    def execute(self):                
        lines = self._content.splitlines()
        for line in lines:
            items = line.split(';')
            if len(items) is 4:
                try:
                    date = self._parse_date(items[0])
                    name = items[1].replace('\\', ' ').replace('/', ' ')
                    nav = locale.atof(items[2])
                    row_id = items[3] 
                    self._fund_callback(date, name, nav, row_id)
                except:
                    print(line)                    