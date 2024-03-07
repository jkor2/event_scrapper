import requests

class Grouped:
    """
    Class to handle events that are grouped
    Initial arg is the url
    """

    def __init__(self, url):
        self._url = url
        self._soup_object = None
    
    def _http_request(self):
        if not self._url:
            return "Error - invalid url"
        
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



    