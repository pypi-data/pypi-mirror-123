import pandas as pd

class jhu_extract:

    def __init__(self, kind):
        self.kind = kind
    
    def extract_data(self) -> pd.DataFrame:
        if self.kind == "cases":
            data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
            # generate daily data
            dailies = data.iloc[:, 11:].T.diff()[1:].T
            daily_colnames = {col_name:col_name+" Daily" for col_name in dailies.columns.to_list()}
            dailies = dailies.rename(daily_colnames, axis=1)
            for col in dailies:
                data[col] = dailies[col]
            return data
        elif self.kind == "deaths":
            data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv")
            # generate daily data
            dailies = data.iloc[:, 11:].T.diff()[1:].T
            daily_colnames = {col_name:col_name+" Daily" for col_name in dailies.columns.to_list()}
            dailies = dailies.rename(daily_colnames, axis=1)
            for col in dailies:
                data[col] = dailies[col]
            return data
        else:
            print("must select either cases or deaths when instantiating extraction object...")