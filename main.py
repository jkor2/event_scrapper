# To run in terminal
# Clone or Download Repository
# Navigate to file destination
# Enter Command: Python main.py

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from openpyxl import load_workbook
import pprint as pp
import os


class DetermineEventType:
    """
    Determines the event type based on url -- error prevention
    """

    def __init__(self, url):
        self._url = url

    def determine(self, type):
        if self._url.split("https://www.perfectgame.org/")[1].split("/")[0] == 'Schedule':
            if type == 1:  # Grouped Event
                return True
            else:
                return False
        else:
            if type == 2:  # Single event
                return True
            else:
                return False


class Grouped:
    """
    Class to handle events that are grouped ( Event Length > 1 )
    Initial arg is the url
    """

    def __init__(self):
        self._event_type = 1
        self._url = None
        self._soup_object = None
        self._event_dates = None
        self._event_ballparks = None
        self._event_city_state = None
        self._event_ages_and_divisions = None
        self._mulit_event_output = []
        self.output = {
            "Headline/Tournament Name:": None,
            "Event Dates:": None,
            "Facility/Field Name:": None,
            "Location:": None,
            "Age Group:": {},
            "Specific Benefits/Callouts:": None,
            "Link for event:": None,
            "Current_ages": []
        }
        self._age_groups = ["6U", "7U", "8U", "9U", "10U",
                            "11U", "12U", "13U", "14U", "15U", "16U", "17U", "18U"]
        self._region = None
        self._state = None

    def create_url(self, url, region, state):
        """
        Create & update url
        """
        self._url = url
        check_event_type = DetermineEventType(self._url)
        self._region = region
        self._state = state

        if check_event_type.determine(1):
            self._http_request()
        else:
            single_event = IndividualEvent(self._region, self._state)

            single_event.create_url(self._url)
            self._mulit_event_output.append(single_event.output_data())

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
            pattern_group_name = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_lblGroupname')
            event_group_name = soup.find(id=pattern_group_name)
            self.output["Headline/Tournament Name:"] = event_group_name.get_text()

            # Handle Dates
            pattern_dates = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblEventDate.+')
            event_dates = soup.find_all(id=pattern_dates)
            self._event_dates = event_dates

            # Handle Facility Name
            pattern_ballpark = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblBallPark.+')
            event_ballpark = soup.find_all(id=pattern_ballpark)
            # Just grab last event in list's text
            self._event_ballparks = event_ballpark[-1].get_text()

            # Handle City/State
            pattern_city_state = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblCityState.+')
            event_city_state = soup.find_all(id=pattern_city_state)
            # Just grab last event in list's text
            self._event_city_state = event_city_state[-1].get_text()

            # Handle Ages and Divisions
            pattern_age_and_division = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_repSchedule_lblDivision.+')
            event_age_and_divsion = soup.find_all(id=pattern_age_and_division)
            self._event_ages_and_divisions = event_age_and_divsion

            return self.clean_data()

        except:
            # Main Error
            print("Please Restart, error on", pattern_group_name)
            exit()

    def clean_data(self):
        """
        Cleaning the data to be copy and pasted from console
        """
        # Find longest event length date and change as needed
        for date in self._event_dates:
            if self.output["Event Dates:"] is None or int(self.output["Event Dates:"][-1]) < int(date.get_text()[-1]):
                self.output["Event Dates:"] = date.get_text()
                # self.output["Event Dates:"] = self.output["Event Dates:"][:6]
        # Append all ages
        for age in self._event_ages_and_divisions:
            text = age.get_text()

            # Reformat

            if len(text.split(" ")) == 1:
                self.output["Age Group:"][text.split(" ")[0]] = []
            else:
                if text.split(" ")[-1][1:-1] == "60/90" or text.split(" ")[-1][1:-1] == "54/80":
                    # Checking for instances of (OPEN) (60/90) or (54/80)
                    s1 = text.split(" ")[1][1:-1]
                    s2 = text.split(" ")[2][1:-1]
                    joined_string = str(s1) + " " + str(s2)
                    self.output["Age Group:"][text.split(" ")[0]] = [
                        joined_string]
                else:
                    self.output["Age Group:"][text.split(" ")[0]] = [
                        text.split(" ")[1][1:-1]]

        # Set field name
        self.output["Facility/Field Name:"] = self._event_ballparks

        # Set location
        self.output["Location:"] = self._event_city_state
        # self.format_ages()
        self.output["Region"] = self._region
        self.output["State"] = self._state
        self._mulit_event_output.append(self.output)

        # Reset output for next event
        self.reset_output()

    def reset_output(self):
        """
        Resets output object
        """
        self.output = {
            "Headline/Tournament Name:": None,
            "Event Dates:": None,
            "Facility/Field Name:": None,
            "Location:": None,
            "Age Group:": {},
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
        data = self.output['Age Group:']

        # To confrim age and divisions in console

        print(self.output["Headline/Tournament Name:"], "complete.")

        print(data)

        for i in self._age_groups:
            if i in data:
                temp_hold = "%s " % i
                for j in data[i]:
                    if len(data[i]) > 1:
                        # Appending differntly based on unique instance of a division
                        if data[i][0][-1] == "0":
                            # Handle when a division specifies field dimensions
                            temp_hold += "%s" % j
                        else:
                            # Handle when there are no field dimensions
                            temp_hold += "%s/" % j
                    else:
                        temp_hold += "%s " % j

                if temp_hold[-1] == "0":
                    # Not removing the last letter if it ends in "0"
                    temp_list.append(temp_hold + ",")
                else:
                    temp_list.append(temp_hold[:-1] + ",")

        self.output["Age Group:"] = " ".join(temp_list)[:-1]


class IndividualEvent:
    def __init__(self, region, state) -> None:
        self._url = None
        self.output = {
            "Headline/Tournament Name:": None,
            "Event Dates:": None,
            "Facility/Field Name:": None,
            "Location:": None,
            "Age Group:": {},
            "Specific Benefits/Callouts:": None,
            "Link for event:": None
        }
        self._age_dictionary = {
            "6U": "6U", "7U": "7U", "8U": "8U", "9U": "9U", "10U": "10U", "11U": "11U", "12U": "12U", "13U": "13U", "14U": "14U", "15U": "15U", "16U": "16U", "17U": "17U", "18U": "18U"
        }
        self._region = region
        self._state = state

    def create_url(self, value):
        """
        Assign and check event type
        """
        self._url = value

        check_event_type = DetermineEventType(self._url)

        if check_event_type.determine(2):
            # Call method to handle scraping the woloe event
            self._http_request()
        else:
            return False

    def _http_request(self):
        """
        Request, scrape, and assign
        """
        try:
            # Grab webpage & create soup object
            webpage = requests.get(self._url, 'html.parser')
            soup = BeautifulSoup(webpage.content, features="lxml")

            # Set event url
            self.output["Link for event:"] = self._url

            # Find eventname
            pattern_event_name = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_EventHeader1_lblEventNameNew')
            event_name = soup.find(id=pattern_event_name)
            self.output["Headline/Tournament Name:"] = event_name.get_text()

            # Handle Facility Name -- facility and city/state are connected
            pattern_ballpark = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_EventHeader1_lblEventLocaGeneral')
            event_ballpark = soup.find_all(id=pattern_ballpark)

            # Split and assign
            self.output["Facility/Field Name:"] = event_ballpark[-1].get_text().split(" | ")[0]
            self.output["Location:"] = event_ballpark[-1].get_text().split(" | ")[1]

            # Handle Ages and Divisions -- different as age is in headline, will utilize age_group dictionary
            pattern_event_age = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_EventHeader1_lblEventNameNew')
            event_age = soup.find(id=pattern_event_age).get_text().split(" ")
            for age in event_age:
                if age.upper() in self._age_dictionary:
                    self.output["Age Group:"] = age

            # # Dates
            pattern_dates = re.compile(
                r'ContentTopLevel_ContentPlaceHolder1_EventHeader1_lblDatesNew')
            event_dates = soup.find(id=pattern_dates).get_text()
            self.output["Event Dates:"] = event_dates
            self.output["Region"] = self._region
            self.output["State"] = self._state
        except:
            print("Erorr")
            exit()

    def output_data(self):
        """
        Output of the single event object 
        Do not need to reset as new instance will be created
        """
        return self.output


event = Grouped()

# Read the user input date range
print()
print("Ensure '2025 Event Email Marketing Calendar' is the most up-to-date version.")
print()

date_range = input("Enter the week to pull events for: ")

# File path
file_path = "2025 Event Email Marketing Calendar.xlsx"  # Replace with your file path

# Load the workbook and sheet
wb = load_workbook(file_path, data_only=True)
sheet = wb.worksheets[1]  # Sheet index 1 (0-based index for second sheet)

# Load the Excel file into a DataFrame
df = pd.read_excel(file_path, sheet_name=1, engine="openpyxl")

# Display DataFrame (Optional)

# Find the starting row index where the 'Date' column matches the user input
n = df[df['Date'] == date_range].index.min()

events = []

if n is not None and not pd.isna(n):
    # Initialize data storage for rows
    row_data = {}
    current_region = None
    current_state = None

    for row_idx in range(n + 2, n + 20):  # Iterate over the rows
        # Iterate over cells in the row
        for col_idx, cell in enumerate(sheet[row_idx], start=1):
            # Check for region in column 2
            if col_idx == 2:
                if cell.value and cell.value != current_region:  # Detect a new region
                    current_region = cell.value
                    if current_region not in row_data:
                        # Initialize state data as a dictionary
                        row_data[current_region] = {}

            # Check for state in column 3
            if col_idx == 3:
                if cell.value and cell.value != current_state:  # Detect a new state
                    current_state = cell.value
                    if current_region and current_state:  # Ensure both region and state exist
                        if current_state not in row_data[current_region]:
                            # Initialize events as a dictionary
                            row_data[current_region][current_state] = {}

            # Process events with hyperlinks (limit to columns F-R, i.e., 6-18 in 1-based index)
            if 6 <= col_idx <= 18 and cell.hyperlink and cell.value:
                # Ensure nested structure for events
                if current_region and current_state:
                    row_data[current_region][current_state][cell.value] = cell.hyperlink.target
                    events.append(
                        [current_region, current_state, cell.hyperlink.target])


# Debug output to validate
print()
print("Events Found:")
print(len(events), " total events.")
print("-----------")
print()


while True:
    """
    While loop to continue executing until exit
    """

    try:
        event_amount = len(events)
        if event_amount == 0:
            exit()

        for i in events:
            url = i[2]
            event.create_url(url, i[0], i[1])

        print()

        # Capture printed output in a list
        output_lines = []

        all_data = event.return_all()
        event_count = 1

        current_event_region = None
        current_event_state = None
        prev_event_region = None

        temp_events = []

        links_two = {
            "Costal": None,
            "Midwest": {'Mid West High School Shortcut': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=273',
                        'Mid West Youth Shortcut': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=283'},
            "Mid-Atlantic": {'Mid Atlantic Reional Shortcut Link (ALL)': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=282',
                             'New England Regional Shortcut Link (All)': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=274', },
            "South": {'South High School': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=275',
                      'South Youth': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=284', },
            "Southeast": {'Deep South Events High School': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=289',
                          'Deep South Events Youth': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=290', 'Florida Regional Shortcut Link (All)': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=281',
                          'South East Events High School': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=276',
                          'South East Events Youth': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=285', },
            "West": {'West Regional Shortcut Link (All)': 'https://www.perfectgame.org/Schedule/FeaturedEvents.aspx?fid=277'}
        }


        for event in all_data:

            if current_event_region is not None and current_event_region != str(event["Region"]):
                output_lines.append("")
                output_lines.append("Links")
                output_lines.append("")
                output_lines.append("\n".join(temp_events))
                temp_events = []
                output_lines.append("\n")


                for val in links_two[current_event_region]:
                    output_lines.append(val+": "+links_two[current_event_region][val])
                output_lines.append("\n")
                                    
                    
                    
                # output_lines.append("\n")

                # Here prev events print out

            if current_event_region is None or current_event_region != str(event["Region"]):
                current_event_region = str(event["Region"])
                output_lines.append("-------------------------------------")
                output_lines.append(f"           {current_event_region}      ")
                output_lines.append("-------------------------------------")

            if current_event_state is None or current_event_state != str(event["State"]):
                current_event_state = str(event["State"])
                output_lines.append(f"----- {current_event_state} -----")

            output_lines.append(str(event["Headline/Tournament Name:"]))
            temp_events.append(
                str(event["Headline/Tournament Name:"]) + ": " + str(event["Link for event:"]))
            output_lines.append(str(event["Event Dates:"])[:6].upper() if str(
                event["Event Dates:"])[6] == "-" else str(event["Event Dates:"])[:5].upper())

            output_lines.append(str(list(event["Age Group:"].keys())[
                                0]) + "-" + str(list(event["Age Group:"].keys())[-1])+" | " + str(event["Location:"]))

            output_lines.append("")  # Add a blank line for spacing

        output_lines.append("")
        output_lines.append("Links")
        output_lines.append("")

        output_lines.append("\n".join(temp_events))
        temp_events = []

        output_lines.append("\n")
# AGES: 8U-18U  |  GRAND RAPIDS, MI

        output_lines.append("\n")


        for val in links_two[current_event_region]:
            output_lines.append(val+": "+links_two[current_event_region][val])
        output_lines.append("\n")


        output_lines.append("")
        output_lines.append(
            "-----------------------------------------------------------")



        # Save output to a file
        output_file = "Event_Details.txt"
        with open(output_file, "w") as file:
            file.write("\n".join(output_lines))

        # Automatically open the file using the default text editor
        if os.name == 'nt':  # Windows
            os.startfile(output_file)
        elif os.name == 'posix':  # macOS or Linux
            os.system(f"open {output_file}")  # For macOS
            # Use 'xdg-open' instead of 'open' for Linux

        # Exit for now after region is returned
        exit()

    except Exception as e:
        print(f"An error occurred: {e}")
        exit()
