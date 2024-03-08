import requests
from bs4 import BeautifulSoup
import pprint as pp
import re


class Grouped:
    """
    Class to handle events that are grouped ( Event Length > 1 )
    Initial arg is the url
    """

    def __init__(self):
        self._url = None
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
            "Link for event:": None
        }
        self._age_groups = ["6U", "7U","8U", "9U", "10U", "11U", "12U", "13U", "14U", "15U", "16U", "17U", "18U"]
    
    def create_url(self, url):
        """
        Create & update url
        """
        self._url = url
        self._http_request()

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

            # Set event url 
            self.output["Link for event:"] = self._url

            # Find groupname 
            pattern_group_name = re.compile(r'ContentTopLevel_ContentPlaceHolder1_lblGroupname')
            event_group_name = soup.find(id=pattern_group_name)
            self.output["Headline/Tournament Name:"] = event_group_name.get_text()
            
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
            # Reformat

            if text.split(" ")[0] in self.output["Age Group:"]:
                if text.split(" ")[-1][1:-1] == "60/90" or text.split(" ")[-1][1:-1]  == "54/80":
                    # Checking for instances of (OPEN) (60/90) or (54/80)
                    s1 = text.split(" ")[1][1:-1]
                    s2 = text.split(" ")[2][1:-1]
                    joined_string = str(s1) + " " + str(s2)  
                    self.output["Age Group:"][text.split(" ")[0]] = [joined_string]
                else:
                    self.output["Age Group:"][text.split(" ")[0]].append(text.split(" ")[1][1:-1])

            else:
                if len(text.split(" ")) == 1:
                    self.output["Age Group:"][text.split(" ")[0]] = []
                    continue
                else:
                    if text.split(" ")[-1][1:-1] == "60/90" or text.split(" ")[-1][1:-1]  == "54/80":
                        # Checking for instances of (OPEN) (60/90) or (54/80)
                        s1 = text.split(" ")[1][1:-1]
                        s2 = text.split(" ")[2][1:-1]
                        joined_string = str(s1) + " " + str(s2)  
                        self.output["Age Group:"][text.split(" ")[0]] = [joined_string]
                    else:
                        self.output["Age Group:"][text.split(" ")[0]] = [text.split(" ")[1][1:-1]]
        

        # Set field name 
        self.output["Facility/Field Name:"] = self._event_ballparks
        
        # Set location
        self.output["Location:"] = self._event_city_state
        self.format_ages()
        self._mulit_event_output.append(self.output)

        # Reset output for next event
        self.reset_output()

        
    def reset_output(self):
        """
        Resets output object
        """
        self.output = {
            "Headline/Tournament Name:": None,
            "Event Dates:" : None,
            "Facility/Field Name:": None, 
            "Location:": None,
            "Age Group:" : {}, 
            "Specific Benefits/Callouts:": None, 
            "Link for event:": None
        }        
    
    def return_all(self):
        """
        Returns all events stored
        """
        return self._mulit_event_output


    def format_ages(self):
        """
        Format age groups to an easy copy and paste string
        """
        temp_list = []
        data =self.output['Age Group:']
        
        # To confrim age and divisions in console
        print()
        print("AGE/Divisions for", self.output["Headline/Tournament Name:"])
        print(data)
        print()

        for i in self._age_groups:
            if i in data:
                temp_hold = "%s " % i
                for j in data[i]:
                    if len(data[i]) > 1:
                        temp_hold += "%s/" % j
                    else:
                        temp_hold += "%s " % j
                temp_list.append(temp_hold[:-1] + ",")

        self.output["Age Group:"] = " ".join(temp_list)[:-1]

        

event = Grouped()

# event.create_url("https://www.perfectgame.org/Schedule/GroupedEvents.aspx?gid=8389")
# pp.pprint(event.return_all())

print("Grouped Events -------------> 1")
print("Individual Event -----------> 2")
print("Exit -----------------------> 3")
selection = int(input("Please Select an Option > "))

if selection == 1:
    try:
        event_amount = int(input("Enter the number of events >"))
        count = event_amount 
        while count > 0:
            url = str(input("Please enter the URL (remove all surrounding whitespace) > "))
            event.create_url(url)
            count -= 1
    

        print()
        print("----------------PRINTING----------------DATA----------------")
        print()

        all_data = event.return_all()
        event_count = 1
        for event in all_data:
            print("EVENT #%s" % event_count)
            print("Headline/Tournament Name:" + " " + str(event["Headline/Tournament Name:"]))
            print("Event Dates:" + " " + str(event["Event Dates:"]))
            print("Facility/Field Name:" + " " + str(event["Facility/Field Name:"]))
            print("Location:" + " " + str(event["Location:"]))
            print("Age Group:" + " " + str(event["Age Group:"]))
            print("Link for event:" + " " + str(event["Link for event:"]))
            print("Specific Benefits/Callouts:" + " " + str(event["Specific Benefits/Callouts:"]))
            print()
            
            event_count += 1

    except:
        exit()
