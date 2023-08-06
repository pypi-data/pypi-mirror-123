from bs4 import BeautifulSoup as bs
import requests
from datetime import datetime
import json
import pandas as pd

class Requester():
    def __init__(self):
        # need to pull a sneaky by pretending I am an actual computer
        self.headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
        self.permit_info = {
                "middle_fork" : (234623, 377),
                "deso_gray" : (233393, 282),
                }

    def api_request(self, permit_name, date_range, commercial_acct=False, is_lottery=False):
        # need to convert dates to match javascript API
        date_range = [date.strftime('%Y-%m-%dT%H:%M:%SZ') for date in date_range]
        request_url = 'https://www.recreation.gov/api/permits/{}/divisions/{}/availability?start_date={}&end_date={}&commercial_acct={}&is_lottery={}'.format(*self.permit_info[permit_name], *date_range, commercial_acct, is_lottery)
        
        # make reuqest and process
        response = requests.get(request_url, headers=self.headers)
        assert response.status_code == 200, f"request failed, got code {response.status_code}"
        return self.response_process(response)

    def response_process(self, response):
        json_response = json.loads(response.text)
        return pd.DataFrame(json_response["payload"]["date_availability"]).transpose()

    def list_permit_names(self):
        print(self.permit_info.keys())

if __name__ == '__main__':
    r = Requester()
    date_range = datetime(2021, 10, 12), datetime(2021, 12, 12)
    request_df = r.api_request("middle_fork", date_range)
    print(request_df)



