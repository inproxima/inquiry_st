from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

class SearchEngine:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("SERPAPI_API_KEY", "")

    def search(self, query, engine="google"):
        """
        Searches using SerpApi. The default engine is Google, 
        but can also switch to YouTube if specified.
        """
        if engine == "youtube":
            params = {
                "engine": "youtube",
                "search_query": query,
                "api_key": self.api_key,
            }
        else:
            # Default to Google
            params = {
                "engine": "google",
                "q": query,
                "api_key": self.api_key,
            }
        search = GoogleSearch(params)
        return search.get_dict()