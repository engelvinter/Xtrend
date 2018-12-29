
from re import match


class FilterName:
    def __init__(self, regexp):
        self._regexp = regexp
    
    def execute(self, df):
        def fund_match(x):
            return match(self._regexp, x) is not None
        
        matches = df.apply(axis=1, func=lambda x: fund_match(x.name))
        filtered_df = df[matches]
        filtered_df.name = df.name
        
        return filtered_df