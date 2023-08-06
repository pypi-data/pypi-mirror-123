import pandas as pd
import requests

class hhs_extract:

    # initialize with api_key
    def __init__(self, bearer_token):
        self.api_key = bearer_token
    
    # extract HHS data
    def extract_data(self) -> pd.DataFrame:
        # read data from Socrata HHS API for county level hospitalizations at CMS registered hospitals
        hhs_return_size = 1
        hhs_total_size = 0
        hhs_df_list = list()
        while (hhs_return_size > 0):
            payload = {'$$app_token': self.api_key, '$limit':50000, '$offset':hhs_total_size}
            hhs_res = requests.get("https://healthdata.gov/resource/anag-cw7u.json", params=payload)
            temp_results_df = pd.DataFrame.from_records(hhs_res.json())
            hhs_return_size = len(temp_results_df)
            hhs_total_size += hhs_return_size
            hhs_df_list.append(temp_results_df)
        hhs_results_df = pd.concat(hhs_df_list)
        return hhs_results_df

class cdc_extract:

    # initialize with api_key
    def __init__(self, bearer_token):
        self.api_key = bearer_token
    
    # extract cdc data
    def extract_data(self) -> pd.DataFrame:
        # read data from Socrata CDC API for county level vaccinations across all dates
        vax_return_size = 1
        vax_total_size = 0
        vax_df_list = list()
        while (vax_return_size > 0):
            payload = {'$$app_token': self.api_key, '$limit':50000, '$offset':vax_total_size}
            vax_res = requests.get("https://data.cdc.gov/resource/8xkx-amqh.json", params=payload)
            temp_results_df = pd.DataFrame.from_records(vax_res.json())
            vax_return_size = len(temp_results_df)
            vax_total_size += vax_return_size
            vax_df_list.append(temp_results_df)
        vax_results_df = pd.concat(vax_df_list)
        return vax_results_df