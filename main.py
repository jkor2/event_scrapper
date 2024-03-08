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
        self._event_dates = None
        self.output = {
            "Headline/Tournament Name:": None,
            "Event Dates:" : None,
            "Facility/Field Name:": None, 
            "Location:": None,
            "Age Group:" : None, 
            "Specific Benefits/Callouts:": None, 
            "Link for event:": None
        }
    
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
            soup = BeautifulSoup(webpage.content, features="lxml")                   # Create Soup Object
            pattern = re.compile(r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblEventDate.+') # Regex to find needed ID 
            event_dates = soup.find_all(id=pattern)           # Search 
            self._event_dates = event_dates                 # Assign the data to private variable 
            
            
            
            
            return self.find_data()                       # Run the find data method

        except:
            print("WARNING: URL INVALID")
        
        # Request 
        # Turn website in soup object 
        # Assign soup object to a variable 
        pass

    def find_data(self):
 

        for date in self._event_dates:
            # Loop through event dates, compare dates to grab the largest and assign if needed
            if self.output["Event Dates:"] is None or int(self.output["Event Dates:"][-1] )< int(date.get_text()[-1]):
                 self.output["Event Dates:"] = date.get_text()


        print(self.output)


        # for parent in soupObject:
        #     print(parent.get_text())


        #Else find all correct elements
        pass

    def _format_data(self, data):
        # Convert the data into easy copy and pastable format 
        # Output
        pass



event = Grouped("https://www.perfectgame.org/Schedule/GroupedEvents.aspx?gid=8122")
event._http_request()