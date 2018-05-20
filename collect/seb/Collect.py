import pandas as pd

class Collect:
    def __init__(self, funds, factory):
        self._is_selected = self._all_funds
        self._factory = factory
        self._funds = funds
        self._fund_names = []
        self.FILE_NOT_FOUND = 404

    def set_selected_funds(self, fund_names):
        self._fund_names = fund_names

    def _is_specified_fund(self, name):
        return name in self._fund_names

    def _all_funds(self, name):
        return True

    def _remove_garbage(self, string):
        if '?' in string:
            string = string.replace('?', ' ')

        items = string.split(' ')
        words = [item for item in items if item]
        string = " ".join(words)
        return string

    def _fund_callback(self, date, name, quote, row_id):
        name = self._remove_garbage(name)

        if not self._is_selected(name):
            return
        
        if name not in self._funds:
            self._funds[name] = pd.DataFrame(columns=['date','quote', 'id'])
        
        df = self._funds[name]
        row_index = df.shape[0]
        df.loc[row_index] = (date, quote, row_id)

    def _collect_funds(self, actual_date):
        downloader = self._factory.create_downloader(actual_date)
        content = downloader.execute()

        extractor = self._factory.create_extractor(content, self._fund_callback)
        extractor.execute()

    def _make_index(self, dataframes, col_name):
        for name in dataframes:
            df = dataframes[name]
            df.index = df[col_name]
            del df[col_name]

    def execute(self, start_date, stop_date):
        interval = pd.date_range(start_date, stop_date)
        for actual_date in interval:
            print(actual_date)
            try:
                self._collect_funds(actual_date)
            except IOError as e:
                if not e.errno == self.FILE_NOT_FOUND:
                    print(e)
                pass
            except KeyError:
                pass

        self._make_index(self._funds, 'date')