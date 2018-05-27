from seb.collect.CollectService import CollectService

from seb.load import LoadService as ls

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