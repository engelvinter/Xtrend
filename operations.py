from collect.seb.CollectService import CollectService

from load.seb import LoadService as ls

DB_PATH = r"C:\Temp\db"

def collect():
    cs = CollectService(DB_PATH, "2018-01-01")
    cs.execute()

def load():
    names = ls.fund_names(DB_PATH)
    service = ls.LoadService(DB_PATH, 10, 10)
    funds = service.execute(names)
    
    return funds

funds = load()