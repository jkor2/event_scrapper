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
        self._event_ballparks = None
        self._event_city_state = None
        self._event_ages_and_divisions = None
        self._mulit_event_output = []
        self.output = {
            "Headline/Tournament Name:": None,
            "Event Dates:" : None,
            "Facility/Field Name:": None, 
            "Location:": None,
            "Age Group:" : {}, 
            "Specific Benefits/Callouts:": None, 
            "Link for event:": url
        }
    
    def create_url(self, url):
        """
        Create & update url
        """
        self._url = url

    def _http_request(self):
        """
        Make inital request and grab needed data 
        """
        if not self._url:
            return "Error - invalid url"
        
        try:
            # Grab webpage & create soup object
            webpage = requests.get(self._url, 'html.parser')        
            soup = BeautifulSoup(webpage.content, features="lxml")                   

            # Handle Dates 
            pattern_dates = re.compile(r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblEventDate.+') 
            event_dates = soup.find_all(id=pattern_dates)           
            self._event_dates = event_dates                 
            
            # Handle Facility Name
            pattern_ballpark = re.compile(r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblBallPark.+') 
            event_ballpark = soup.find_all(id=pattern_ballpark)           
            # Just grab last event in list's text 
            self._event_ballparks = event_ballpark[-1].get_text()             
            
            # Handle City/State
            pattern_city_state = re.compile(r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblCityState.+') 
            event_city_state = soup.find_all(id=pattern_city_state)           
            # Just grab last event in list's text 
            self._event_city_state = event_city_state[-1].get_text()   
            
            # Handle Ages and Divisions 
            pattern_age_and_division = re.compile(r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblDivision.+') 
            event_age_and_divsion = soup.find_all(id=pattern_age_and_division)           
            self._event_ages_and_divisions = event_age_and_divsion
            
            return self.clean_data()                       

        except:
            print("WARNING: URL INVALID")
        

    def clean_data(self):
        """
        Cleaning the data to be copy and pasted from console
        """
 
        # Find longest event length date and change as needed 
        for date in self._event_dates:
            if self.output["Event Dates:"] is None or int(self.output["Event Dates:"][-1] )< int(date.get_text()[-1]):
                 self.output["Event Dates:"] = date.get_text()
        
        # Append all ages 
        for age in self._event_ages_and_divisions:
            text = age.get_text()
            if text.split(" ")[0] in self.output["Age Group:"]:
                self.output["Age Group:"][text.split(" ")[0]].append(text.split(" ")[1][1:-1])
            else:
                self.output["Age Group:"][text.split(" ")[0]] = [text.split(" ")[1][1:-1]]
        

        # Set field name 
        self.output["Facility/Field Name:"] = self._event_ballparks
        
        # Set location
        self.output["Location:"] = self._event_city_state

        for i in self.output:
            print(i, self.output[i])
        






event = Grouped("https://www.perfectgame.org/Schedule/GroupedEvents.aspx?gid=8122")
event._http_request()