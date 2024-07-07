import requests
from typing import Any, Dict

class CATExplore:
    def __init__(self, domain: str):
        self.domain = domain

    def fetch_sample(self, num_rows=1) -> dict:
        try:
            return self.fetch_ckan_sample(num_rows)
        except requests.exceptions.RequestException:
            try:
                return self.fetch_dcat_sample()
            except requests.exceptions.RequestException as error:
                print(f"An error occurred: {error}")
                raise error

    def fetch_ckan_sample(self, num_rows=1) -> dict:
        url = f"https://{self.domain}/api/3/action/package_search"
        params = {"rows": num_rows}
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if 'result' in data:
            if 'results' in data['result'] and data['result']['results']:
                return data['result']['results'][0]
            elif 'result' in data['result'] and data['result']['result']:
                return data['result']['result'][0]
        raise KeyError("Expected data structure not found in CKAN response")

    def fetch_dcat_sample(self) -> dict:
        url = f"https://{self.domain}/api/feed/dcat-ap/2.1.1.json"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if 'dcat:dataset' in data and isinstance(data['dcat:dataset'], list):
            return data['dcat:dataset'][0]
        raise KeyError("Expected data structure not found in DCAT-AP response")

    @staticmethod
    def print_structure(data: Dict[str, Any], indent: int = 0, key: str = "root"):
        if isinstance(data, dict):
            print(f"{' ' * indent}{key}:")
            for k, v in data.items():
                CATExplore.print_structure(v, indent + 1, k)
        elif isinstance(data, list):
            print(f"{' ' * indent}{key}: (list of {len(data)} items)")
            if data:
                CATExplore.print_structure(data[0], indent + 1, f"{key}[0]")
        else:
            value_type = type(data).__name__
            value_preview = str(data)[:50] + "..." if len(str(data)) > 50 else str(data)
            print(f"{' ' * indent}{key}: ({value_type}) {value_preview}")

if __name__ == "__main__":
    explorer = CATExplore("opendata.bristol.gov.uk")
    result = explorer.fetch_sample()
    explorer.print_structure(result)