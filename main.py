import requests
from bs4 import BeautifulSoup
import pprint as pp
import re


class Grouped:
    """
    Class to handle events that are grouped
    Initial arg is the url
    """

    def __init__(self, url):
        self._url = url
        self._soup_object = None
    
    def create_url(self, url):
        """
        Create & update url
        """
        self._url = url

    def _http_request(self):
        if not self._url:
            return "Error - invalid url"
        
        try:
            webpage = requests.get(self._url, 'html.parser')        # Parse Webpage
            soup = BeautifulSoup(webpage.content)                   # Create Soup Object
            pattern = re.compile(r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lbl.+') # Regex to find needed ID 
            matching_elements = soup.find_all(id=pattern)           # Search 
            self._soup_object = matching_elements                   # Assign the data to private variable 
            self.find_data(self._soup_object)                       # Run the find data method

        except:
            print("WARNING: URL INVALID")
        
        # Request 
        # Turn website in soup object 
        # Assign soup object to a variable 
        pass

    def find_data(self, soupObject):
        if not self._soup_object:
            self._http_request()

        #Else find all correct elements
        pass

    def _format_data(self, data):
        # Convert the data into easy copy and pastable format 
        # Output
        pass



event = Grouped("https://www.perfectgame.org/Schedule/GroupedEvents.aspx?gid=8122")
event._http_request()