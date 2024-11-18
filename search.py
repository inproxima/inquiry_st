from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

class SearchEngine:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("SERPAPI_API_KEY")

    def search(self, term):
        params = {
            "api_key": self.api_key,
            "engine": "google",
            "q": term,
            "location": "Canada",
            "google_domain": "google.ca",
            "gl": "ca",
            "hl": "en",
            "safe": "active"
        }

        search = GoogleSearch(params)
        return search.get_dict()