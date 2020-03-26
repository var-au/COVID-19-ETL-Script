import csv
import requests
import datetime
from bs4 import BeautifulSoup

utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
url = "https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-current-situation-and-case-numbers"

class covid_data:

    site_content = ''
    parsed_content = ''
    cases = {}

    def get_sitecontent(self, web_uri):
        self.site_content = requests.get(web_uri)
        return

    def parse_sitecontent(self):
        self.parsed_content = BeautifulSoup(
            self.site_content.content, 'html.parser')
        return

    def extract_tabledata(self):
        v = self.parsed_content.find_all('tbody')[0]
        self.cases['Generated Timestamp'] = utc_timestamp
        self.cases['Australian Capital Territory'] = v.find_all('tr')[1].find_all('td')[1].p.string
        self.cases['New South Wales'] = v.find_all('tr')[2].find_all('td')[1].string
        self.cases['Northern Territory'] = v.find_all('tr')[3].find_all('td')[1].string
        self.cases['Queensland'] = v.find_all('tr')[4].find_all('td')[1].string
        self.cases['South Australia'] = v.find_all('tr')[5].find_all('td')[1].string
        self.cases['Tasmania'] = v.find_all('tr')[6].find_all('td')[1].string
        self.cases['Victoria'] = v.find_all('tr')[7].find_all('td')[1].string
        self.cases['Western Australia'] = v.find_all('tr')[8].find_all('td')[1].string
        return self.cases

    def update_csvfile(self):
        with open('output.csv', 'a', newline='') as f:
            w = csv.DictWriter(f, self.cases.keys())
            w.writerow(self.cases)
            f.close()

    def __init__(self, web_uri):
        self.get_sitecontent(web_uri)
        self.parse_sitecontent()
        self.extract_tabledata()
        self.update_csvfile()

if __name__ == "__main__":
    covid_data(url)